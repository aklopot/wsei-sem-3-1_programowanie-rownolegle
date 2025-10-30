"""
Moduł do walidacji i pobierania danych wejściowych
Zawiera klasę InputValidator do walidacji i pobierania danych wprowadzanych przez użytkownika.
"""


class InputValidator:
    """
    Klasa odpowiedzialna za walidację i pobieranie danych wejściowych od użytkownika.
    Dostarcza metody do pobierania zwalidowanych liczb całkowitych, zmiennoprzecinkowych oraz niestandardowych typów danych.
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
    
    @staticmethod
    def get_positive_integer(message, error_message=None):
        """
        Pobiera prawidłową dodatnią liczbę całkowitą (> 0) od użytkownika.
        """
        if error_message is None:
            error_message = "Liczba musi być większa od zera."
        
        def validate_positive(value):
            if value <= 0:
                raise ValueError(error_message)
        
        return InputValidator.get_integer(message, error_message, validate_positive)
    
    @staticmethod
    def get_non_negative_integer(message, error_message=None):
        """
        Pobiera prawidłową nieujemną liczbę całkowitą (>= 0) od użytkownika.
        """
        if error_message is None:
            error_message = "Liczba musi być większa lub równa zero."
        
        def validate_non_negative(value):
            if value < 0:
                raise ValueError(error_message)
        
        return InputValidator.get_integer(message, error_message, validate_non_negative)
    
    @staticmethod
    def get_integer_in_range(message, min_value, max_value, error_message=None):
        """
        Pobiera prawidłową liczbę całkowitą z określonego zakresu od użytkownika.
        """
        if error_message is None:
            error_message = f"Liczba musi być między {min_value} a {max_value}."
        
        def validate_range(value):
            if not (min_value <= value <= max_value):
                raise ValueError(error_message)
        
        return InputValidator.get_integer(message, error_message, validate_range)
    
    @staticmethod
    def get_float(message, error_message=None, validation_func=None):
        """
        Pobiera prawidłową liczbę zmiennoprzecinkową od użytkownika.
        """
        if error_message is None:
            error_message = "Nieprawidłowe dane. Wprowadź prawidłową liczbę."
        
        while True:
            try:
                value = float(input(message))
                
                if validation_func is not None:
                    validation_func(value)
                
                return value
                
            except ValueError:
                print(f"Błąd: {error_message}")
            except Exception as e:
                print(f"Błąd: {e}")
    
    @staticmethod
    def get_positive_float(message, error_message=None):
        """
        Pobiera prawidłową dodatnią liczbę zmiennoprzecinkową (> 0) od użytkownika.
        
        Args:
            message (str): Komunikat do wyświetlenia
            error_message (str, optional): Komunikat błędu przy nieprawidłowych danych
        Returns:
            float: Prawidłowa dodatnia liczba zmiennoprzecinkowa
        """
        if error_message is None:
            error_message = "Liczba musi być większa od zera."
        
        def validate_positive(value):
            if value <= 0:
                raise ValueError(error_message)
        
        return InputValidator.get_float(message, error_message, validate_positive)
    
    @staticmethod
    def get_yes_no(message, error_message=None):
        """
        Pobiera odpowiedź tak/nie od użytkownika.
        """
        if error_message is None:
            error_message = "Odpowiedz 'tak' lub 'nie'."
        
        while True:
            answer = input(message).strip().lower()
            
            if answer in ['tak', 't', 'yes', 'y', '1']:
                return True
            elif answer in ['nie', 'n', 'no', '0']:
                return False
            else:
                print(f"Error: {error_message}")
