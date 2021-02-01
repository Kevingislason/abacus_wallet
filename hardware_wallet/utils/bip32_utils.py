from bitcoin.bip32 import parse_path, path_to_str
from bitcoin.networks import NETWORKS
from bitcoin.script import p2pkh, p2wpkh, p2sh

from hardware_wallet.constants.hd_key_path_constants import (
    MAINNET_KEYPATH,
    TESTNET_KEYPATH,
    BIP_44_KEYPATH,
    BIP_49_KEYPATH,
    BIP_84_KEYPATH
)
from hardware_wallet.constants.network_constants import (
    MAINNET,
    TESTNET
)


def get_keypath_by_network(network: str):
    if network == MAINNET:
        return MAINNET_KEYPATH
    elif network == TESTNET:
        return TESTNET_KEYPATH
    else:
        raise Exception("Invalid network")


def get_address_type_keypath(keypath: str):
    return path_to_str(parse_path(keypath)[:1])


def derive_address_from_keypath(keypath, address_pubkey, network):
    address_type_keypath = get_address_type_keypath(keypath)
    if address_type_keypath == BIP_44_KEYPATH:
        return p2pkh(address_pubkey).address(NETWORKS[network])
    elif address_type_keypath == BIP_49_KEYPATH:
        redeem_script = p2wpkh(address_pubkey)
        return p2sh(redeem_script).address(NETWORKS[network])
    elif address_type_keypath == BIP_84_KEYPATH:
        return p2wpkh(address_pubkey).address(NETWORKS[network])
    else:
        raise Exception("Invalid keypath")
