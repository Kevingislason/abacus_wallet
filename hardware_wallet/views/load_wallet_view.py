import lvgl as lv

from hardware_wallet.views.recover_wallet_view import RecoverWalletView
from hardware_wallet.constants.view_constants import (
    BUTTON_ACTIVE_STATE,
    BUTTON_DISABLED_STATE
)


class LoadWalletView(RecoverWalletView):
    def __init__(self, controller):
        self.controller = controller
        self.recovery_phrase = []
        self.autocompleted = False
        self.recovery_phrase_target_length = controller.recovery_phrase_length
        self.show_phrase_input()

    def show_phrase_input(self):
        super().show_phrase_input()
        if len(self.recovery_phrase) == 0:
            self.prev_recovery_phrase_word_button.set_state(
                BUTTON_DISABLED_STATE)
            lv.scr_load(self.screen)

    def show_phrase_length_selection(self):
        pass

    def handle_password_finish_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            recovery_phrase = " ".join(self.recovery_phrase)
            password = self.password_input.get_text()
            if self.controller.load_wallet(recovery_phrase, password):
                self.show_recovery_succeeded()
            else:
                self.show_recovery_failed()

    def handle_acknowledge_recovery_failed_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            self.recovery_phrase = []
            self.show_phrase_input()

    def handle_acknowledge_recovery_failed_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            self.recovery_phrase = []
            self.show_phrase_input()
