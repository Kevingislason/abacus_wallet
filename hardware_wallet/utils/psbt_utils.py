def get_non_witness_utxo_value(current_tx, input_parent_tx):
    input_parent_txid = input_parent_tx.txid()
    for input in current_tx.vin:
        if input.txid == input_parent_txid:
            utxo = input_parent_tx.vout[input.vout]
            return utxo.value
