"""
Moduł menu programu.
"""

from src.validators.input_validator import InputValidator


class Menu:
    """Klasa zarządzająca menu głównym programu."""

    def __init__(self, title="GŁÓWNE MENU"):
        self.title = title
        self.options = {}

    def add_option(self, key, description, handler, display_order):
        self.options[key] = {'description': description, 'handler': handler, 'display_order': display_order}

    def _display_menu(self):
        print("\n" + "=" * 60)
        print(f"          {self.title}")
        print("=" * 60)
        for key, opt in sorted(self.options.items(), key=lambda x: x[1]['display_order']):
            print(f"{key} - {opt['description']}")
        print("=" * 60)

    @staticmethod
    def pause_screen():
        input("\nNaciśnij Enter, aby powrócić do menu...")

    def show(self):
        while True:
            self._display_menu()
            try:
                available = ", ".join(sorted(self.options.keys()))
                choice = str(InputValidator.get_integer(
                    "Wybierz opcję: ",
                    f"Nieprawidłowa opcja. Możesz wybrać: {available}.",
                    lambda v: (_ for _ in ()).throw(ValueError()) if str(v) not in self.options else None
                ))
                self.options[choice]['handler']()
                if choice != '0':
                    self.pause_screen()
            except KeyboardInterrupt:
                print("\n\nProgram przerwany przez użytkownika.")
                break
            except SystemExit:
                break
            except Exception as e:
                print(f"Błąd: {e}")

    def exit(self):
        print(f"\nDziękuję za korzystanie z programu!")
        exit()
