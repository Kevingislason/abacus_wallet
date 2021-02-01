import display
import lvgl as lv

from hardware_wallet.views.recover_wallet_view import RecoverWalletView
from hardware_wallet.views.create_new_wallet_view import CreateNewWalletView


class InitWalletView():
    def __init__(self, controller):
        self.controller = controller
        self.show_recovery_method_selection()

    def show_recovery_method_selection(self):
        self.screen = lv.obj()
        self.generate_new_wallet_button = lv.btn(self.screen)
        self.generate_new_wallet_button.set_size(350, 100)
        self.generate_new_wallet_button.align(
            lv.scr_act(), lv.ALIGN.CENTER, 0, -150)
        self.generate_new_wallet_label = lv.label(
            self.generate_new_wallet_button)
        self.generate_new_wallet_label.set_text("Generate New Wallet")
        self.generate_new_wallet_button.set_event_cb(
            self.handle_generate_new_wallet_button)

        self.recover_wallet_button = lv.btn(self.screen)
        self.recover_wallet_button.set_size(420, 100)
        self.recover_wallet_button.align(lv.scr_act(), lv.ALIGN.CENTER, 0, 150)
        self.recover_wallet_label = lv.label(
            self.recover_wallet_button)
        self.recover_wallet_label.set_text("Recover Existing Wallet")
        self.recover_wallet_button.set_event_cb(
            self.handle_recover_wallet_button)
        lv.scr_load(self.screen)

    def handle_generate_new_wallet_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            CreateNewWalletView(self.controller)

    def handle_recover_wallet_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            RecoverWalletView(self.controller)
