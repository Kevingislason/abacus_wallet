import lvgl as lv

from hardware_wallet.utils.ui_utils import (
    format_address,
    format_money,
    get_currency_label
)


class SignTxView():
    def __init__(self, controller, psbt):
        self.controller = controller
        self.psbt = psbt
        self.show_sign_transaction()

    def show_sign_transaction(self):
        self.screen = lv.obj()
        self.sign_tx_header_label = lv.label(
            self.screen)
        self.sign_tx_header_label.set_text("INCOMING TRANSACTION")
        self.sign_tx_header_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -360)

        self.main_spend_amount_label = lv.label(self.screen)
        main_spend_amount = format_money(self.psbt.spend_output.value)
        main_spend_amount_text = "1) Send {amount} {currency_label}\n to receiving address:".format(
            amount=main_spend_amount, currency_label=get_currency_label("test")
        )
        self.main_spend_amount_label.set_text(main_spend_amount_text)
        self.main_spend_amount_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -260)

        self.main_spend_address_label = lv.label(self.screen)
        main_spend_address_text = format_address(self.psbt.spend_address)
        self.main_spend_address_label.set_text(main_spend_address_text)
        self.main_spend_address_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -185)

        self.fee_label = lv.label(self.screen)
        fee_amount = format_money(self.psbt.fee_amount)
        fee_text = "2) Pay {amount} {currency_label}\n  as a transaction fee".format(
            amount=fee_amount, currency_label=get_currency_label(
                self.controller.network)
        )
        self.fee_label.set_text(fee_text)
        self.fee_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -80)

        if self.psbt.change_output:
            self.change_spend_amount_label = lv.label(self.screen)
            change_spend_amount = format_money(self.psbt.change_output.value)
            change_spend_amount_text = "3) Send {amount} {currency_label} to  \n    your change address:".format(
                amount=change_spend_amount, currency_label=get_currency_label(
                    self.controller .network)
            )
            self.change_spend_amount_label.set_text(change_spend_amount_text)
            self.change_spend_amount_label.align(
                self.screen, lv.ALIGN.CENTER, 0, 30)

            self.change_address_label = lv.label(self.screen)
            change_address_text = format_address(self.psbt.change_address)
            self.change_address_label.set_text(change_address_text)
            self.change_address_label.align(
                self.screen, lv.ALIGN.CENTER, 0, 100)

            self.change_address_bip_label = lv.label(self.screen)
            change_address_bip_text = "BIP32: {path}".format(
                path=self.psbt.change_keypath)
            self.change_address_bip_label.set_text(change_address_bip_text)
            self.change_address_bip_label.align(
                self.screen, lv.ALIGN.CENTER, 0, 160)

        self.reject_transaction_button = lv.btn(self.screen)
        self.reject_transaction_button.set_size(200, 100)
        self.reject_transaction_button.align(
            self.screen,  lv.ALIGN.CENTER, -120, 280)
        self.reject_transaction_button_label = lv.label(
            self.reject_transaction_button)
        self.reject_transaction_button_label.set_text("Reject")
        self.reject_transaction_button.set_event_cb(
            self.handle_reject_transaction)

        self.sign_transaction_button = lv.btn(self.screen)
        self.sign_transaction_button.set_size(200, 100)
        self.sign_transaction_button.align(
            self.screen,  lv.ALIGN.CENTER, 120, 280)
        self.sign_transaction_button_label = lv.label(
            self.sign_transaction_button)
        self.sign_transaction_button_label.set_text("Sign")
        self.sign_transaction_button.set_event_cb(self.handle_sign_transaction)

        lv.scr_load(self.screen)

    def handle_sign_transaction(self, obj, event):
        if event == lv.EVENT.RELEASED:
            self.controller.sign_transaction(self.psbt)

    def handle_reject_transaction(self, obj, event):
        if event == lv.EVENT.RELEASED:
            self.controller.reject_transaction()
