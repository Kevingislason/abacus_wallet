
from bitcoin.bip32 import parse_path, path_to_str
from bitcoin.networks import NETWORKS
from bitcoin.psbt import PSBT as _PSBT

from hardware_wallet.utils.bip32_utils import (
    derive_address_from_keypath
)
from hardware_wallet.utils.psbt_utils import (
    get_non_witness_utxo_value
)


class PSBT(_PSBT):
    def differentiate_change_from_spend_outputs(self, network):
        if len(self.tx.vout) == 1:
            self.spend_output = self.tx.vout[0]
            self.spend_address = self.spend_output.script_pubkey.address(
                NETWORKS[network])
            self.change_output = None
            self.change_address = None
            return

        for output in self.tx.vout:
            address = output.script_pubkey.address(NETWORKS[network])
            change_address = derive_address_from_keypath(
                self.change_keypath, self.change_pubkey, network)
            if address == change_address:
                self.change_output = output
                self.change_address = output.script_pubkey.address(
                    NETWORKS[network])
            else:
                self.spend_output = output
                self.spend_address = output.script_pubkey.address(
                    NETWORKS[network])

    # Display properties

    @property
    def fee_amount(self):
        non_fee_amount = self.spend_output.value
        if self.change_output:
            non_fee_amount += self.change_output.value

        total_input_amount = 0
        for input_scope in self.inputs:
            if input_scope.witness_utxo:
                total_input_amount += input_scope.witness_utxo.value
            elif input_scope.non_witness_utxo:
                total_input_amount += get_non_witness_utxo_value(
                    self.tx, input_scope.non_witness_utxo)

        return total_input_amount - non_fee_amount

    @property
    def change_keypath(self):
        if not self.change_output_scope:
            return None
        _, keypath = next(
            iter(self.change_output_scope.bip32_derivations.items()))
        return path_to_str(keypath.derivation)

    # Convenience properties

    @property
    def input_keypaths(self):
        keypaths = []
        for input_scope in self.inputs:
            _, keypath = next(iter(input_scope.bip32_derivations.items()))
            keypaths.append(path_to_str(keypath.derivation))
        return keypaths

    @property
    def change_output_scope(self):
        return [output_scope for output_scope in self.outputs if output_scope.bip32_derivations][0]

    @property
    def change_pubkey(self):
        return next(iter(self.change_output_scope.bip32_derivations))
