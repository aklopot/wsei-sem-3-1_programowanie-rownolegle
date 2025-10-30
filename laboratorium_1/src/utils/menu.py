"""
Moduł menu programu
Zawiera klasę Menu do zarządzania opcjami menu głównego.
"""

from src.validators.input_validator import InputValidator


class Menu:
    """
    Klasa odpowiedzialna za zarządzanie menu głównym programu.
    Umożliwia dodawanie i wykonywanie różnych opcji menu.
    """
    
    def __init__(self, title="GŁÓWNE MENU"):
        """
        Inicjalizacja menu.
        
        Args:
            title (str): Tytuł menu
        """
        self.title = title
        self.options = {}
    
    def add_option(self, key, description, handler, display_order):
        """
        Dodaj opcję do menu.
        
        Args:
            key (str): Klucz opcji (np. "1", "2")
            description (str): Opis opcji wyświetlany w menu
            handler (callable): Funkcja/metoda do wykonania po wyborze opcji
            display_order (int): Kolejność wyświetlania (mniejsza liczba = wyżej w menu)
        """
        self.options[key] = {
            'description': description,
            'handler': handler,
            'display_order': display_order
        }
    
    def _display_menu(self):
        """Wyświetl menu na ekranie."""
        print("\n" + "="*60)
        print(f"          {self.title}")
        print("="*60)
        
        # Wyświetl opcje posortowane według kolejności wyświetlania
        sorted_options = sorted(self.options.items(), key=lambda x: x[1]['display_order'])
        for key, option in sorted_options:
            print(f"{key} - {option['description']}")
        
        print("="*60)
    
    def show(self):
        """
        Wyświetl menu i rozpocznij interakcję z użytkownikiem.
        Pozwala wybierać opcje w pętli do czasu wyboru wyjścia.
        """
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
                handler() # Wykonaj handler dla wybranej opcji
                    
            except KeyboardInterrupt:
                print("\n\nProgram przerwany przez użytkownika.")
                break
            except SystemExit:
                break
            except Exception as e:
                print(f"Błąd: {e}")
    
    def _validate_menu_choice(self, value):
        choice_str = str(value)
        if choice_str not in self.options:
            raise ValueError()
    
    def exit(self):
        """
        Wyjście z programu z komunikatem pożegnalnym.
        """
        print(f"\nDziękuję za korzystanie z programu!")
        exit()
