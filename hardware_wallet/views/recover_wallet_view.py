from bitcoin import bip39
import lvgl as lv

from hardware_wallet.constants.view_constants import (
    BUTTON_ACTIVE_STATE,
    BUTTON_DISABLED_STATE
)


class RecoverWalletView():
    RECOVERY_PHRASE_KEYBOARD_MAP = [
        "Bksp", "\n",
        "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "\n",
        "a", "s", "d", "f", "g", "h", "j", "k", "l", "\n",
        "z", "x", "c", "v", "b", "n", "m", ""
    ]
    PASSWORD_KEYBOARD_MAP_LOWER_CASE = [
        "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "\n",
        "a", "s", "d", "f", "g", "h", "j", "k", "l", "\n",
        "_", "-", "z", "x", "c", "v", "b", "n", "m", ".", ",", ":", ""
    ]
    PASSWORD_KEYBOARD_MAP_UPPER_CASE = [
        "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "\n",
        "A", "S", "D", "F", "G", "H", "J", "K", "L", "\n",
        "_", "-", "Z", "X", "C", "V", "B", "N", "N", ".", ",", ":", ""
    ]
    PASSWORD_KEYBOARD_MAP_SPECIAL_CHARS = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "\n",
        "+", "-", "/", "*", "=", "%", "!", "?", "#", "<", ">", "\n",
        "\\", "@", "$", "(", ")", "{", "}", "[", "]", ";", "\"", "'", "",
    ]

    LOWER_CASE_KEYBOARD_SYMBOL = "abc"
    UPPER_CASE_KEYBOARD_SYMBOL = "ABC"
    SPECIAL_CHARS_KEYBOARD_SYMBOL = "1#"

    RECOVERY_PHRASE_LENGTHS = [12, 15, 18, 21, 24]

    def __init__(self, controller):
        self.controller = controller
        self.recovery_phrase = []
        self.autocompleted = False
        self.recovery_phrase_target_length = None
        self.recovery_phrase = []

        self.show_phrase_length_selection()

    ############################## Subviews ###################################

    def show_phrase_length_selection(self):
        self.screen = lv.obj()

        self.recovery_phrase_length_screen_label = lv.label(
            self.screen)
        self.recovery_phrase_length_screen_label.set_text(
            "How many words are in\n your recovery phrase?")
        self.recovery_phrase_length_screen_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -300)

        self.recovery_phrase_length_roller = lv.roller(self.screen)
        recovery_phrase_length_options_str = "\n".join(
            str(phrase_length) for phrase_length in self.RECOVERY_PHRASE_LENGTHS
        )
        self.recovery_phrase_length_roller.set_options(
            recovery_phrase_length_options_str, 0)
        self.recovery_phrase_length_roller.set_fix_width(True)
        self.recovery_phrase_length_roller.set_selected(2, 0)
        self.recovery_phrase_length_roller.set_size(200, 200)
        self.recovery_phrase_length_roller.align(
            self.screen, lv.ALIGN.CENTER, 0, -75)
        self.recovery_phrase_length_roller.set_visible_row_count(5)

        self.confirm_phrase_length_button = lv.btn(self.screen)
        self.confirm_phrase_length_button.set_size(125, 60)
        self.confirm_phrase_length_button.align(
            self.screen, lv.ALIGN.CENTER, 0, 100)
        self.confirm_phrase_length_button.set_event_cb(
            self.handle_confirm_phrase_length_button)
        self.confirm_phrase_length_button_label = lv.label(
            self.confirm_phrase_length_button)
        self.confirm_phrase_length_button_label.set_text("Ok")

        lv.scr_load(self.screen)

    def show_phrase_input(self):
        self.phrase_input_length = 0

        self.screen = lv.obj()

        self.recovery_phrase_length_screen_label = lv.label(
            self.screen)
        self.recovery_phrase_length_screen_label.set_text(
            "Recovery phrase word {page_number}/{recovery_phrase_target_length}".format(
                page_number=len(self.recovery_phrase) + 1,
                recovery_phrase_target_length=self.recovery_phrase_target_length
            )
        )
        self.recovery_phrase_length_screen_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -350)

        self.recovery_phrase_input = lv.ta(self.screen)
        self.recovery_phrase_input.set_one_line(True)
        self.recovery_phrase_input.set_text("")
        self.recovery_phrase_input.set_max_length(16)
        self.recovery_phrase_input.align(self.screen, lv.ALIGN.CENTER, 0, -275)
        self.recovery_phrase_input.set_event_cb(
            self.handle_recovery_phrase_input_change)
        # need to keep track of this for the autocomplete
        self.autocompleted = False
        self.phrase_input_length = 0

        self.prev_recovery_phrase_word_button = lv.btn(self.screen)
        self.prev_recovery_phrase_word_button.set_size(125, 60)
        self.prev_recovery_phrase_word_button_label = lv.label(
            self.prev_recovery_phrase_word_button)
        self.prev_recovery_phrase_word_button_label.set_text("Back")
        self.prev_recovery_phrase_word_button.align(
            self.screen, lv.ALIGN.CENTER, -100, -150)
        self.prev_recovery_phrase_word_button.set_event_cb(
            self.handle_previous_recovery_phrase_word_button
        )

        self.next_recovery_phrase_word_button = lv.btn(self.screen)
        self.next_recovery_phrase_word_button.set_size(125, 60)
        self.next_recovery_phrase_word_button_label = lv.label(
            self.next_recovery_phrase_word_button)
        self.next_recovery_phrase_word_button_label.set_text("Next")
        self.next_recovery_phrase_word_button.align(
            self.screen, lv.ALIGN.CENTER, 100, -150)
        self.next_recovery_phrase_word_button.set_state(BUTTON_DISABLED_STATE)
        self.next_recovery_phrase_word_button.set_event_cb(
            self.handle_next_recovery_phrase_word_button)

        self.keyboard = lv.kb(self.screen)
        self.keyboard.set_map(self.RECOVERY_PHRASE_KEYBOARD_MAP)
        self.keyboard.set_ta(self.recovery_phrase_input)

        lv.scr_load(self.screen)

    def show_password_input(self):
        self.screen = lv.obj()
        self.wallet_paddword_screen_label = lv.label(
            self.screen)
        self.wallet_paddword_screen_label.set_text(
            "   Enter your recovery\nphrase password (if any)")
        self.wallet_paddword_screen_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -350)

        self.password_input = lv.ta(self.screen)
        self.password_input.set_one_line(True)
        self.password_input.set_text("")
        self.password_input.align(self.screen, lv.ALIGN.CENTER, 0, -275)

        self.password_back_button = lv.btn(self.screen)
        self.password_back_button.set_size(125, 60)
        self.password_back_button_label = lv.label(
            self.password_back_button)
        self.password_back_button_label.set_text("Back")
        self.password_back_button.align(
            self.screen, lv.ALIGN.CENTER, -100, -150)
        self.password_back_button.set_event_cb(
            self.handle_password_back_button
        )

        self.password_finish_button = lv.btn(self.screen)
        self.password_finish_button.set_size(150, 60)
        self.password_finish_button_label = lv.label(
            self.password_finish_button)
        self.password_finish_button_label.set_text("Finish")
        self.password_finish_button.align(
            self.screen, lv.ALIGN.CENTER, 100, -150)
        self.password_finish_button.set_event_cb(
            self.handle_password_finish_button
        )

        self.toggle_keyboard_button = lv.btn(self.screen)
        self.toggle_keyboard_button.set_size(230, 100)
        self.toggle_keyboard_button_label = lv.label(
            self.toggle_keyboard_button)
        self.toggle_keyboard_button_label.set_text(
            self.UPPER_CASE_KEYBOARD_SYMBOL)
        self.toggle_keyboard_button.align(
            self.screen, lv.ALIGN.CENTER, -118, 50)
        self.toggle_keyboard_button.set_event_cb(
            self.handle_toggle_password_keyboard_button
        )

        self.backspace_button = lv.btn(self.screen)
        self.backspace_button.set_size(230, 100)
        self.backspace_button_label = lv.label(self.backspace_button)
        self.backspace_button_label.set_text("Bksp")
        self.backspace_button.align(
            self.screen, lv.ALIGN.CENTER, 118, 50)
        self.backspace_button.set_event_cb(
            self.handle_password_backspace_button
        )

        self.keyboard = lv.kb(self.screen)
        self.keyboard.set_height(300)
        self.keyboard.align(self.screen, lv.ALIGN.IN_BOTTOM_MID, 0, 0)
        self.keyboard.set_map(self.PASSWORD_KEYBOARD_MAP_LOWER_CASE)
        self.keyboard.set_ta(self.password_input)

        lv.scr_load(self.screen)

    def show_recovery_failed(self):
        self.screen = lv.obj()

        self.recovery_failed_label = lv.label(
            self.screen)
        self.recovery_failed_label.set_text(
            "Recovery phrase is invalid")
        self.recovery_failed_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -200)

        self.acknowledge_recovery_failed_button = lv.btn(self.screen)
        self.acknowledge_recovery_failed_button.set_size(125, 60)
        self.acknowledge_recovery_failed_button_label = lv.label(
            self.acknowledge_recovery_failed_button)
        self.acknowledge_recovery_failed_button_label.set_text("Okay")
        self.acknowledge_recovery_failed_button.align(
            self.screen, lv.ALIGN.CENTER, 0, 0)
        self.acknowledge_recovery_failed_button.set_event_cb(
            self.handle_acknowledge_recovery_failed_button
        )

        lv.scr_load(self.screen)

    def show_recovery_succeeded(self):
        self.screen = lv.obj()
        self.recovery_succeeded_label = lv.label(self.screen)
        self.recovery_succeeded_label.set_text(
            "Wallet successfully\n    recovered")
        self.recovery_succeeded_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -200)

        lv.scr_load(self.screen)

    ############################## Handlers ###################################

    def handle_confirm_phrase_length_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            scroller_idx = self.recovery_phrase_length_roller.get_selected()
            self.recovery_phrase_target_length = self.RECOVERY_PHRASE_LENGTHS[scroller_idx]
            self.show_phrase_input()

    def handle_next_recovery_phrase_word_button(self, obj, event):
        if event == lv.EVENT.RELEASED and obj.get_state() != BUTTON_DISABLED_STATE:
            self.recovery_phrase.append(self.recovery_phrase_input.get_text())
            if len(self.recovery_phrase) == self.recovery_phrase_target_length:
                recovery_phrase = " ".join(self.recovery_phrase)
                if bip39.mnemonic_is_valid(recovery_phrase):
                    self.show_password_input()
                else:
                    self.show_recovery_failed()
            else:
                self.show_phrase_input()

    def handle_previous_recovery_phrase_word_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            if len(self.recovery_phrase) == 0:
                self.show_phrase_length_selection()
            else:
                self.recovery_phrase.pop()
                self.show_phrase_input()

    def handle_recovery_phrase_input_change(self, obj, event):
        if event == lv.EVENT.VALUE_CHANGED:
            recovery_phrase_input = self.recovery_phrase_input.get_text()
            prev_length = self.phrase_input_length
            current_length = len(recovery_phrase_input)
            self.phrase_input_length = current_length
            # Short-circuit handler when autocompleting to prevent infintie loop
            if self.autocompleted:
                return

            # We don't want to autocomplete if user is backspacing
            if current_length > prev_length:
                # If current word is valid, prevent addition
                if recovery_phrase_input[:-1] in bip39.WORDLIST:
                    self.autocompleted = True
                    self.recovery_phrase_input.del_char()
                    self.next_recovery_phrase_word_button.set_state(0)
                # Autcomplete if there is only 1 valid BIP39 word for this input
                candidates = bip39.find_candidates(recovery_phrase_input)
                if len(candidates) == 1:
                    self.autocompleted = True
                    self.recovery_phrase_input.set_text(candidates[0])
                    self.next_recovery_phrase_word_button.set_state(0)

            if self.recovery_phrase_input.get_text() in bip39.WORDLIST:
                self.next_recovery_phrase_word_button.set_state(
                    BUTTON_ACTIVE_STATE)
            else:
                self.next_recovery_phrase_word_button.set_state(
                    BUTTON_DISABLED_STATE)

            self.autocompleted = False

    def handle_password_back_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            self.recovery_phrase.pop()
            self.show_phrase_input()

    def handle_password_finish_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            recovery_phrase = " ".join(self.recovery_phrase)
            password = self.password_input.get_text()
            self.show_recovery_succeeded()
            self.controller.save_wallet(recovery_phrase, password, True)

    def handle_password_backspace_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            current_text = self.password_input.get_text()
            self.password_input.set_text(current_text[:-1])

    def handle_toggle_password_keyboard_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            keyboard_type = self.toggle_keyboard_button_label.get_text()
            if keyboard_type == self.UPPER_CASE_KEYBOARD_SYMBOL:
                self.toggle_keyboard_button_label.set_text(
                    self.SPECIAL_CHARS_KEYBOARD_SYMBOL)
                self.keyboard.set_map(self.PASSWORD_KEYBOARD_MAP_UPPER_CASE)
            elif keyboard_type == self.SPECIAL_CHARS_KEYBOARD_SYMBOL:
                self.toggle_keyboard_button_label.set_text(
                    self.LOWER_CASE_KEYBOARD_SYMBOL)
                self.keyboard.set_map(self.PASSWORD_KEYBOARD_MAP_SPECIAL_CHARS)
            elif keyboard_type == self.LOWER_CASE_KEYBOARD_SYMBOL:
                self.toggle_keyboard_button_label.set_text(
                    self.UPPER_CASE_KEYBOARD_SYMBOL
                )
                self.keyboard.set_map(self.PASSWORD_KEYBOARD_MAP_LOWER_CASE)

    def handle_acknowledge_recovery_failed_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            from hardware_wallet.views.init_wallet_view import InitWalletView
            InitWalletView(self.controller)
