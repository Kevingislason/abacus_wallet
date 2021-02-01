import sys
import os

from bitcoin.bip39 import mnemonic_from_bytes, mnemonic_to_seed
from bitcoin.bip32 import HDKey, parse_path
from bitcoin.hashes import hash160
from bitcoin.networks import NETWORKS
import hashlib
import pyb

from hardware_wallet.classes.psbt import PSBT
from hardware_wallet.classes.psbt_validator import PSBTValidator
from hardware_wallet.constants.hd_key_path_constants import (
    BIP_44_KEYPATH,
    BIP_49_KEYPATH,
    BIP_84_KEYPATH,
    MAINNET_KEYPATH,
    TESTNET_KEYPATH,
    FIRST_ACCOUNT_KEYPATH
)
from hardware_wallet.constants.network_constants import MAINNET, TESTNET
from hardware_wallet.serial.serial_client import SerialClient
from hardware_wallet.utils.bip32_utils import (
    get_keypath_by_network,
    derive_address_from_keypath
)
from hardware_wallet.views.address_view import AddressView
from hardware_wallet.views.init_wallet_view import InitWalletView
from hardware_wallet.views.load_wallet_view import LoadWalletView
from hardware_wallet.views.recover_wallet_view import RecoverWalletView
from hardware_wallet.views.rejected_tx_view import RejectedTXView, RejectedTxMessage
from hardware_wallet.views.sign_tx_view import SignTxView
from hardware_wallet.views.sign_tx_success_view import SignTxSuccessView


class Controller():

    def __init__(self):
        self.network = None
        self.master_xpriv = None

        self.wallet_xpub = None
        self.wallet_keypath = None
        self.recovery_phrase_length = None

        self.serial_client = SerialClient(self)
        self.serial_client.read()

    def generate_new_wallet(self) -> str:
        # Get entropy from hardware rng and environmental entropy
        rng_entropy = os.urandom(64)
        adc = pyb.ADC("A0")
        env_entropy = bytes(adc.read() % 256 for i in range(2048))
        entropy = hashlib.sha256(rng_entropy + env_entropy).digest()[:16]
        recovery_phrase = mnemonic_from_bytes(entropy)
        return recovery_phrase.split(" ")

    def save_wallet(self, recovery_phrase: str, password: str, was_recovered: bool):
        seed = mnemonic_to_seed(recovery_phrase, password)
        self.master_xpriv = HDKey.from_seed(
            seed, NETWORKS[self.network]["xprv"])
        self.master_xpub = self.master_xpriv.to_public()
        wallet_xpubs = self.derive_wallet_xpubs(was_recovered)
        master_fingerprint = self.master_xpub.child(0).fingerprint
        self.serial_client.write_init_wallet_success(
            wallet_xpubs, master_fingerprint, len(recovery_phrase.split())
        )

    def load_wallet(self, recovery_phrase: str, password: str) -> bool:
        seed = mnemonic_to_seed(recovery_phrase, password)
        master_xpriv = HDKey.from_seed(
            seed, NETWORKS[self.network]["xprv"])
        wallet_xpub = master_xpriv.derive(self.wallet_keypath).to_public()
        if wallet_xpub == self.wallet_xpub:
            self.master_xpriv = master_xpriv
            self.serial_client.write_load_wallet_success()
            return True
        return False

    def derive_wallet_xpubs(self, was_recovered: bool):
        xpub_keypath_tuples = []
        if was_recovered:
            address_type_keypaths = [BIP_44_KEYPATH,
                                     BIP_49_KEYPATH,
                                     BIP_84_KEYPATH]
        else:
            address_type_keypaths = [BIP_84_KEYPATH]
        network_keypath = get_keypath_by_network(self.network)
        for address_type_keypath in address_type_keypaths:
            path_str = "{address_type_keypath}/{network_keypath}/{account_keypath}".format(
                address_type_keypath=address_type_keypath,
                network_keypath=network_keypath,
                account_keypath=FIRST_ACCOUNT_KEYPATH
            )
            path = parse_path(path_str)
            xpub = self.master_xpriv.derive(path).to_public()
            xpub_keypath_tuples.append((xpub, path_str))

        return xpub_keypath_tuples

    def sign_transaction(self, psbt: PSBT):
        signatures_added = psbt.sign_with(self.master_xpriv)
        success = signatures_added == len(psbt.inputs)
        if success:
            SignTxSuccessView()
            self.serial_client.write_sign_transaction_success(psbt)
        else:
            RejectedTXView(RejectedTxMessage.INVALID)
            self.serial_client.write_sign_transaction_failure()

    def reject_transaction(self):
        RejectedTXView(RejectedTxMessage.REJECTED_BY_USER)
        self.serial_client.write_sign_transaction_failure()

    # Serial event handlers

    def handle_init_wallet_request(self, network: str):
        self.network = network
        InitWalletView(self)

    def handle_load_wallet_request(
        self,
        wallet_xpub,
        wallet_keypath,
        network: str,
        recovery_phrase_length: int
    ):
        if self.master_xpriv:
            self.serial_client.write_load_wallet_success()
        else:
            self.network = network
            self.wallet_xpub = wallet_xpub
            self.wallet_keypath = wallet_keypath
            self.recovery_phrase_length = recovery_phrase_length
            LoadWalletView(self)

    def handle_show_address_request(self, key_path):
        if self.master_xpriv:
            address = derive_address_from_keypath(
                key_path,
                self.master_xpriv.derive(key_path).to_public(),
                self.network
            )
            AddressView(address, key_path)

    def handle_sign_transaction_request(self, psbt: PSBT):
        if self.master_xpriv:
            if PSBTValidator(psbt, self.master_xpriv, self.network).validate():
                psbt.differentiate_change_from_spend_outputs(self.network)
                SignTxView(self, psbt)
            else:
                RejectedTXView(RejectedTxMessage.INVALID)
                self.serial_client.write_sign_transaction_failure()
