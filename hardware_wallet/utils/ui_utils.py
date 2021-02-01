import lvgl as lv

from hardware_wallet.constants.money_constants import (
    SATOSHIS_PER_BTC,
    MAINNET_CURRENCY_LABEL,
    TESTNET_CURRENCY_LABEL
)
from hardware_wallet.constants.network_constants import (
    MAINNET,
    TESTNET
)


def format_address(address: str):
    address_string_midpoint = len(address) // 2
    address_first_half = address[:address_string_midpoint]
    address_second_half = address[address_string_midpoint:]
    return "{address_first_half}\n{address_second_half}".format(
        address_first_half=address_first_half, address_second_half=address_second_half
    )


def format_money(satoshis: int):
    return "{0:.9f}".format(satoshis / SATOSHIS_PER_BTC).rstrip('0').rstrip('.')


def get_currency_label(network: str):
    if network == MAINNET:
        return MAINNET_CURRENCY_LABEL
    elif network == TESTNET:
        return TESTNET_CURRENCY_LABEL
