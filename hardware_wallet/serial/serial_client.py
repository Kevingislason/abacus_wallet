import uos
import pyb
import binascii
import json
import time
import sys

from bitcoin.bip32 import HDKey, parse_path

from hardware_wallet.classes.psbt import PSBT


class IncomingMessageHeader:
    REQUEST_INIT_WALLET = "init wallet"
    REQUEST_LOAD_WALLET = "load wallet"
    REQUEST_SIGN_TRANSACTION = "sign transaction"
    REQUEST_SHOW_ADDRESS = "show address"


class OutgoingMessageHeader:
    INIT_WALLET_SUCCESS = "init wallet success"
    LOAD_WALLET_SUCCESS = "load wallet success"
    SIGN_TRANSACTION_RESULT = "sign transaction result"


class SerialClient():
    def __init__(self, controller):
        self.controller = controller

    def read(self):
        while True:
            data = sys.stdin.readline()
            if data:
                message = json.loads(data)
                self.dispatch_message(message)
            time.sleep(0.1)

    def dispatch_message(self, json):
        header = json["header"]
        payload = json["payload"]

        if header == IncomingMessageHeader.REQUEST_INIT_WALLET:
            network = json["payload"]["network"]
            self.controller.handle_init_wallet_request(network)

        elif header == IncomingMessageHeader.REQUEST_SIGN_TRANSACTION:
            psbt_bytes = binascii.unhexlify(payload["psbt"])
            psbt = PSBT.parse(psbt_bytes)
            self.controller.handle_sign_transaction_request(psbt)

        elif header == IncomingMessageHeader.REQUEST_SHOW_ADDRESS:
            key_path = payload["key_path"]
            self.controller.handle_show_address_request(key_path)

        elif header == IncomingMessageHeader.REQUEST_LOAD_WALLET:
            wallet_xpub = HDKey.parse(
                binascii.unhexlify(payload["wallet_xpub"])
            )
            wallet_keypath = payload["wallet_keypath"]
            network = payload["network"]
            recovery_phrase_length = payload["recovery_phrase_length"]
            self.controller.handle_load_wallet_request(
                wallet_xpub,
                wallet_keypath,
                network,
                recovery_phrase_length
            )

    # todo: would be more elegant to have array of "candidate_wallets"

    @staticmethod
    def write_init_wallet_success(xpub_keypath_tuples, master_fingerprint, recovery_phrase_length):
        message = {
            "header": OutgoingMessageHeader.INIT_WALLET_SUCCESS,
            "payload": {
                "wallet_xpubs": [
                    xpub.to_base58() for xpub, _ in xpub_keypath_tuples
                ],
                "key_paths": {
                    xpub.to_base58(): key_path for xpub, key_path in xpub_keypath_tuples
                },
                "master_fingerprint": binascii.hexlify(master_fingerprint).decode('utf8'),
                "recovery_phrase_length": recovery_phrase_length
            }
        }
        sys.stdout.write(json.dumps(message))

    @staticmethod
    def write_load_wallet_success():
        message = {"header": OutgoingMessageHeader.LOAD_WALLET_SUCCESS}
        sys.stdout.write(json.dumps(message))

    @staticmethod
    def write_sign_transaction_failure():
        message = {
            "header": OutgoingMessageHeader.SIGN_TRANSACTION_RESULT,
            "payload": {
                "success": False
            }
        }
        sys.stdout.write(json.dumps(message))

    @staticmethod
    def write_sign_transaction_success(psbt: PSBT):
        message = {
            "header": OutgoingMessageHeader.SIGN_TRANSACTION_RESULT,
            "payload": {
                "success": True,
                "psbt":  binascii.hexlify(psbt.serialize()).decode('utf8')
            }
        }
        sys.stdout.write(json.dumps(message))
