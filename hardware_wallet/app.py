import sys
import display

import lvgl as lv

from hardware_wallet.controller import Controller
from hardware_wallet.views.init_wallet_view import InitWalletView


class App():
    def __init__(self):
        self.init_ui()
        self.controller = Controller()

    def init_ui(self):
        display.init()
        theme = lv.theme_material_init(210, lv.font_roboto_mono_28)
        lv.theme_set_current(theme)
