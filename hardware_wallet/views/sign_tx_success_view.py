import lvgl as lv


class SignTxSuccessView():
    def __init__(self):
        self.show_sign_tx_success()

    def show_sign_tx_success(self):
        self.screen = lv.obj()
        self.rejected_tx_label = lv.label(
            self.screen)
        self.rejected_tx_label.set_text(
            "Successfully signed\n    transaction")
        self.rejected_tx_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -200)
        lv.scr_load(self.screen)
