"""
Moduł walidacji danych wejściowych.
"""


class InputValidator:
    """Klasa do walidacji i pobierania danych wejściowych od użytkownika."""

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
