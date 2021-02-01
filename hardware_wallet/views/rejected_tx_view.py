import lvgl as lv


class RejectedTxMessage:
    INVALID = "Received unusual or invalid transaction; rejected"
    FAILED_SIGN = "Failed to sign transaction"
    REJECTED_BY_USER = "Transaction rejected"


class RejectedTXView():
    def __init__(self, message):
        self.show_rejected_tx(message)

    def show_rejected_tx(self, message):
        self.screen = lv.obj()
        self.rejected_tx_label = lv.label(
            self.screen)
        self.rejected_tx_label.set_text(message)
        self.rejected_tx_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -200)
        lv.scr_load(self.screen)
