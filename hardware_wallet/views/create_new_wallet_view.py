import lvgl as lv


class CreateNewWalletView():
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

    def __init__(self, controller):
        self.controller = controller
        self.recovery_phrase = self.controller.generate_new_wallet()
        self.password = None
        self.recovery_phrase_page_number = None

        self.show_set_password()

    ############################## Subviews ###################################

    def show_set_password(self):
        self.screen = lv.obj()

        self.create_password_screen_label = lv.label(
            self.screen)
        self.create_password_screen_label.set_text(
            "Set a password (optional)")
        self.create_password_screen_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -360)

        self.password_input = lv.ta(self.screen)
        self.password_input.set_one_line(True)
        self.password_input.set_text("")
        self.password_input.align(self.screen, lv.ALIGN.CENTER, 0, -285)

        self.submit_password_button = lv.btn(self.screen)
        self.submit_password_button.set_size(125, 60)
        self.submit_password_button.align(
            self.screen, lv.ALIGN.CENTER, 0, -220)
        self.submit_password_button.set_event_cb(
            self.handle_submit_password_button)
        self.submit_password_button_label = lv.label(
            self.submit_password_button)
        self.submit_password_button_label.set_text("Set")

        self.password_tips_label = lv.label(
            self.screen)
        self.password_tips_label.set_text(
            "-Avoid common passwords\n"
            "-Use at least 11 characters\n"
            "-Use letters, numbers and\nspecial characters"
        )
        self.password_tips_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -90)

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

    def show_recovery_phrase_warning(self):
        self.screen = lv.obj()
        self.recovery_phrase_header_label = lv.label(
            self.screen)
        self.recovery_phrase_header_label.set_text(
            "WRITE DOWN YOUR\nRECOVERY PHRASE!")
        self.recovery_phrase_header_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -300)

        self.recovery_phrase_instruction_label = lv.label(
            self.screen)
        self.recovery_phrase_instruction_label.set_text(
            "If you lose your wallet,\nyou can recover it on any\n computer "
            "ONLY with BOTH:\n\n1)Your recovery phrase\n2)Your password")
        self.recovery_phrase_instruction_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -85)

        self.show_recovery_phrase_button = lv.btn(self.screen)
        self.show_recovery_phrase_button.set_size(400, 100)
        self.show_recovery_phrase_button.align(
            self.screen, lv.ALIGN.CENTER, 0, 150)
        self.show_recovery_phrase_button.set_event_cb(
            self.handle_show_recovery_phrase_button)
        self.show_recovery_phrase_button_label = lv.label(
            self.show_recovery_phrase_button)
        self.show_recovery_phrase_button_label.set_text("Show recovery phrase")

        lv.scr_load(self.screen)

    def show_recovery_phrase(self):
        self.screen = lv.obj()

        self.recovery_phrase_header_label = lv.label(self.screen)
        recovery_phrase_word_index = self.recovery_phrase_page_number - 1
        recovery_phrase_header_label_text = "Recovery phrase " \
            "{page_number}/{total_pages}:".format(
                page_number=self.recovery_phrase_page_number,
                total_pages=len(self.recovery_phrase)
            )
        self.recovery_phrase_header_label.set_text(
            recovery_phrase_header_label_text
        )
        self.recovery_phrase_header_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -300)

        self.recovery_phrase_word_label = lv.label(self.screen)
        self.recovery_phrase_word_label.set_text(
            self.recovery_phrase[recovery_phrase_word_index])
        self.recovery_phrase_word_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -150)

        if self.recovery_phrase_page_number != 1:
            self.prev_recovery_phrase_word_button = lv.btn(self.screen)
            self.prev_recovery_phrase_word_button.set_size(125, 60)
            self.prev_recovery_phrase_word_button_label = lv.label(
                self.prev_recovery_phrase_word_button)
            self.prev_recovery_phrase_word_button_label.set_text("Back")
            self.prev_recovery_phrase_word_button.align(
                self.screen, lv.ALIGN.CENTER, -100, 0)
            self.prev_recovery_phrase_word_button.set_event_cb(
                self.handle_previous_recovery_phrase_word_button
            )

        if self.recovery_phrase_page_number != len(self.recovery_phrase):
            self.next_recovery_phrase_word_button = lv.btn(self.screen)
            self.next_recovery_phrase_word_button.set_size(125, 60)
            self.next_recovery_phrase_word_button_label = lv.label(
                self.next_recovery_phrase_word_button)
            self.next_recovery_phrase_word_button_label.set_text("Next")
            self.next_recovery_phrase_word_button.align(
                self.screen, lv.ALIGN.CENTER, 100, 0)
            self.next_recovery_phrase_word_button.set_event_cb(
                self.handle_next_recovery_phrase_word_button)
        else:
            self.finish_recovery_phrase_button = lv.btn(self.screen)
            self.finish_recovery_phrase_button.set_size(150, 60)
            self.finish_recovery_phrase_button.align(
                self.screen, lv.ALIGN.CENTER, 100, 0)
            self.finish_recovery_phrase_button_label = lv.label(
                self.finish_recovery_phrase_button)
            self.finish_recovery_phrase_button_label.set_text("Finish")
            self.finish_recovery_phrase_button.set_event_cb(
                self.handle_finish_recovery_phrase_button)
        lv.scr_load(self.screen)

    def show_init_wallet_succeeded(self):
        self.screen = lv.obj()
        self.recovery_succeeded_label = lv.label(self.screen)
        self.recovery_succeeded_label.set_text(
            "Wallet successfully\n     created")
        self.recovery_succeeded_label.align(
            self.screen, lv.ALIGN.CENTER, 0, -200)

        lv.scr_load(self.screen)

    ############################## Handlers ###################################

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

    def handle_password_backspace_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            current_text = self.password_input.get_text()
            self.password_input.set_text(current_text[:-1])

    def handle_submit_password_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            self.password = self.password_input.get_text()
            self.recovery_phrase = self.controller.generate_new_wallet()
            self.recovery_phrase_page_number = 1
            self.show_recovery_phrase_warning()

    def handle_show_recovery_phrase_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            self.recovery_phrase_page_number = 1
            self.show_recovery_phrase()

    def handle_previous_recovery_phrase_word_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            self.recovery_phrase_page_number -= 1
            self.show_recovery_phrase()

    def handle_next_recovery_phrase_word_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            self.recovery_phrase_page_number += 1
            self.show_recovery_phrase()

    def handle_finish_recovery_phrase_button(self, obj, event):
        if event == lv.EVENT.RELEASED:
            recovery_phrase = " ".join(self.recovery_phrase)
            self.controller.save_wallet(recovery_phrase, self.password, False)
            self.show_init_wallet_succeeded()
