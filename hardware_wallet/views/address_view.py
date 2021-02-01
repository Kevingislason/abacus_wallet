import lvgl as lv
from lvqr import QRCode

from hardware_wallet.utils.ui_utils import format_address


class AddressView():
    def __init__(self, address, path):
        self.address = address
        self.path = path
        self.show_address()

    def show_address(self):
        self.screen = lv.obj()

        self.qr = QRCode(self.screen)
        self.qr.set_size(400)
        self.qr.align(self.screen, lv.ALIGN.CENTER, 0, -100)
        self.qr.set_text(self.address)

        self.address_label = lv.label(self.screen)
        address_text = format_address(self.address)
        self.address_label.set_text(address_text)
        self.address_label.align(self.screen, lv.ALIGN.CENTER, 0, 150)

        self.path_label = lv.label(self.screen)
        self.path_label.set_text("BIP32: " + self.path)
        self.path_label.align(self.screen, lv.ALIGN.CENTER, 0, 250)

        lv.scr_load(self.screen)
