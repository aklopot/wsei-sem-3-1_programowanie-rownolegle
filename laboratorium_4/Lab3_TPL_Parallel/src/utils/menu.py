"""
Moduł menu programu.
Zawiera klasę Menu do zarządzania opcjami menu głównego.
"""

from src.validators.input_validator import InputValidator


class Menu:
    """
    Klasa odpowiedzialna za zarządzanie menu głównym programu.
    Umożliwia dodawanie i wykonywanie różnych opcji menu.
    """

    def __init__(self, title="GŁÓWNE MENU"):
        self.title = title
        self.options = {}

    def add_option(self, key, description, handler, display_order):
        """Dodaje opcję do menu."""
        self.options[key] = {
            'description': description,
            'handler': handler,
            'display_order': display_order
        }

    def _display_menu(self):
        """Wyświetla menu na ekranie."""
        print("\n" + "=" * 60)
        print(f"          {self.title}")
        print("=" * 60)
        sorted_options = sorted(self.options.items(), key=lambda x: x[1]['display_order'])
        for key, option in sorted_options:
            print(f"{key} - {option['description']}")
        print("=" * 60)

    @staticmethod
    def pause_screen():
        """Zatrzymuje ekran i czeka na naciśnięcie Enter."""
        input("\nNaciśnij Enter, aby powrócić do menu...")

    def show(self):
        """Wyświetla menu i rozpoczyna interakcję z użytkownikiem."""
        while True:
            self._display_menu()
            try:
                available_options = ", ".join(sorted(self.options.keys()))
                choice_int = InputValidator.get_integer(
                    "Wybierz opcję: ",
                    f"Nieprawidłowa opcja. Możesz wybrać: {available_options}.",
                    self._validate_menu_choice
                )
                choice = str(choice_int)
                handler = self.options[choice]['handler']
                handler()
                if choice != '0':
                    self.pause_screen()
            except KeyboardInterrupt:
                print("\n\nProgram przerwany przez użytkownika.")
                break
            except SystemExit:
                break
            except Exception as e:
                print(f"Błąd: {e}")

    def _validate_menu_choice(self, value):
        """Waliduje wybór opcji menu."""
        if str(value) not in self.options:
            raise ValueError()

    def exit(self):
        """Wyjście z programu."""
        print(f"\nDziękuję za korzystanie z programu!")
        exit()
