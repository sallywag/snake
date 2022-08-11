import pygame


class InputManager:

    def __init__(self):
        self._pressed_keys_and_buttons = set()
        self._held_keys_and_buttons = set()
        self._released_keys_and_buttons = set()
        self.cursor_location = None
        self.quit = False

    def pressed(self, key_or_button) -> bool:
        return key_or_button in self._pressed_keys_and_buttons

    def held(self, key_or_button) -> bool:
        return key_or_button in self._held_keys_and_buttons

    def released(self, key_or_button) -> bool:
        return key_or_button in self._released_keys_and_buttons

    def process_input(self) -> None:
        self._released_keys_and_buttons.clear()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                event_key_or_button = event.key
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                or event.type == pygame.MOUSEBUTTONUP
            ):
                event_key_or_button = event.button

            if event.type == pygame.MOUSEMOTION:
                self.cursor_location = event.pos

            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event_key_or_button in self._pressed_keys_and_buttons:
                    self._held_keys_and_buttons.add(event_key_or_button)
                    self._pressed_keys_and_buttons.remove(event_key_or_button)
                elif event_key_or_button not in self._held_keys_and_buttons:
                    self._pressed_keys_and_buttons.add(event_key_or_button)

            elif event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                if event_key_or_button in self._pressed_keys_and_buttons:
                    self._pressed_keys_and_buttons.remove(event_key_or_button)
                elif event_key_or_button in self._held_keys_and_buttons:
                    self._held_keys_and_buttons.remove(event_key_or_button)
                self._released_keys_and_buttons.add(event_key_or_button)

            elif event.type == pygame.QUIT:
                self.quit = True
