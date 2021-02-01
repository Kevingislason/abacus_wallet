from bitcoin.bip32 import parse_path, path_to_str
from bitcoin.networks import NETWORKS

from hardware_wallet.utils.bip32_utils import (
    derive_address_from_keypath,
    get_keypath_by_network,
    get_address_type_keypath
)
from hardware_wallet.constants.hd_key_path_constants import (
    CHANGE_KEYPATH,
    FIRST_ACCOUNT_KEYPATH
)


class PSBTValidator:
    def __init__(self, psbt, master_xpriv, network):
        self.psbt = psbt
        self.master_xpriv = master_xpriv
        self.network = network

    def validate(self):
        if not self.validate_psbt_shape_is_standard():
            return False
        if self.psbt.change_output_scope:
            return self.validate_change_output()
        return True

    def validate_psbt_shape_is_standard(self):
        if len(self.psbt.tx.vout) == 1 and len(self.psbt.tx.vout) == 1:
            return True
        elif len(self.psbt.outputs) == 2 and len(self.psbt.tx.vout) == 2:
            change_output_scopes = [
                output for output in self.psbt.outputs
                if output.bip32_derivations
            ]
            return len(change_output_scopes) == 1
        else:
            return False

    def validate_change_output(self):
        return (
            self.validate_change_output_scope_matches_change_spend() and
            self.validate_change_keypath_is_standard() and
            self.validate_change_address_is_mine()
        )

    def validate_change_output_scope_matches_change_spend(self):
        change_address_in_output_scope = derive_address_from_keypath(
            self.psbt.change_keypath,
            self.psbt.change_pubkey,
            self.network
        )
        for output in self.psbt.tx.vout:
            change_address_in_tx = output.script_pubkey.address(
                NETWORKS[self.network])
            if change_address_in_tx == change_address_in_output_scope:
                return True
        return False

    def validate_change_keypath_is_standard(self):
        address_type_keypath = get_address_type_keypath(
            self.psbt.input_keypaths[0])
        expected_change_base_keypath = "{address_type_keypath}/{network_keypath}/{account_keypath}/{change_keypath}".format(
            address_type_keypath=address_type_keypath,
            network_keypath=get_keypath_by_network(self.network),
            account_keypath=FIRST_ACCOUNT_KEYPATH,
            change_keypath=CHANGE_KEYPATH
        )
        actual_base_change_keypath = path_to_str(
            parse_path(self.psbt.change_keypath)[:-1]
        )
        return actual_base_change_keypath == expected_change_base_keypath

    def validate_change_address_is_mine(self):
        change_pubkey_in_output_scope = self.psbt.change_pubkey
        change_pubkey_derived_from_path = self.master_xpriv.derive(
            self.psbt.change_keypath).to_public().key
        return change_pubkey_in_output_scope == change_pubkey_derived_from_path
