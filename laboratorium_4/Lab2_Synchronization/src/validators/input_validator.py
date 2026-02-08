"""
Moduł walidacji danych wejściowych.
Zawiera klasę InputValidator do walidacji danych wprowadzanych przez użytkownika.
"""


class InputValidator:
    """
    Klasa odpowiedzialna za walidację i pobieranie danych wejściowych od użytkownika.
    """

    @staticmethod
    def get_integer(message, error_message=None, validation_func=None):
        """Pobiera prawidłową liczbę całkowitą od użytkownika."""
        if error_message is None:
            error_message = "Nieprawidłowe dane. Wprowadź prawidłową liczbę całkowitą."

        while True:
            try:
                value = int(input(message))

                if validation_func is not None:
                    validation_func(value)

                return value

            except ValueError:
                print(f"Błąd: {error_message}")
            except Exception as e:
                print(f"Błąd: {e}")
