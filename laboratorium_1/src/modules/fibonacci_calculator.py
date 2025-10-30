"""
Moduł kalkulatora liczb Fibonacciego
Zawiera klasę FibonacciCalculator do obliczania ciągu Fibonacciego.
"""

from src.validators.input_validator import InputValidator


class FibonacciCalculator:
    """
    Klasa odpowiedzialna za obliczanie ciągu Fibonacciego.
    """
    
    def __init__(self):
        """Inicjalizacja kalkulatora Fibonacciego."""
        pass
    
    def display_fibonacci_range(self, start_index, count):
        """
        Wyświetl ciąg Fibonacciego zaczynając od start_index dla count elementów.
        
        Args:
            start_index (int): Indeks początkowy w ciągu Fibonacciego
            count (int): Liczba elementów do wyświetlenia
        """
        prev_value = 0  # Poprzednia liczba
        curr_value = 1  # Aktualna liczba
        
        # Przejdź do start_index
        for i in range(start_index):
            prev_value, curr_value = curr_value, prev_value + curr_value
        
        print("Ciąg Fibonacciego:")
        for i in range(count):
            index = start_index + i
            
            if index == 0:
                print(f"F[0] = 0")
                prev_value, curr_value = 0, 1
            elif index == 1:
                print(f"F[1] = 1")
                prev_value, curr_value = 1, 1
            else:
                print(f"F[{index}] = {curr_value}")
                prev_value, curr_value = curr_value, prev_value + curr_value
    
    def run_task1(self):
        """
        Zadanie 1: Pobierz dane i wyświetl pierwsze n elementów ciągu Fibonacciego.
        """
        try:
            n = InputValidator.get_positive_integer(
                "\nPodaj liczbę elementów ciągu Fibonacciego: ",
                "Liczba elementów musi być większa od zera."
            )
            
            # Wyświetl elementy od indeksu 0
            self.display_fibonacci_range(0, n)
            
        except Exception as e:
            print(f"Błąd: {e}")
    
    def run_task2(self):
        """
        Zadanie 2: Pobierz dane i wyświetl fragment ciągu od określonego indeksu.
        """
        try:
            start_index = InputValidator.get_non_negative_integer(
                "\nPodaj indeks początkowy (L1): ",
                "Indeks początkowy nie może być ujemny."
            )
            count = InputValidator.get_positive_integer(
                "Podaj liczbę elementów do wyświetlenia (L2): ",
                "Liczba elementów musi być większa od zera."
            )
            
            self.display_fibonacci_range(start_index, count)
            
        except Exception as e:
            print(f"Błąd: {e}")
