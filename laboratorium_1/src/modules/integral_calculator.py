"""
Moduł do obliczania całek numerycznych
Zawiera klasę IntegralCalculator do obliczania całek metodą prostokątów.
"""

from src.validators.input_validator import InputValidator


class IntegralCalculator:
    """
    Klasa odpowiedzialna za obliczanie całek numerycznych metodą prostokątów.
    """
    
    def __init__(self):
        """Inicjalizacja kalkulatora całek."""
        pass
    
    def function_1(self, x):
        """
        Funkcja do całkowania: f(x) = 1/2 * x
        
        Args:
            x (float): Wartość wejściowa
        Returns:
            float: Wartość funkcji dla x
        """
        return 0.5 * x
    
    def calculate_integral_rectangles(self, a, b, n):
        """
        Oblicz całkę metodą prostokątów.
        
        Args:
            a (float): Lewa granica przedziału
            b (float): Prawa granica przedziału
            n (int): Liczba prostokątów (podział)
        
        Returns:
            float: Przybliżona wartość całki
        """
        if n <= 0:
            raise ValueError("Liczba prostokątów musi być większa od zera.")
        
        # Oblicz szerokość każdego prostokąta
        dx = (b - a) / n
        
        # Suma pól prostokątów
        total_area = 0.0
        
        # Wyświetl obliczenia
        print(f"\nObliczanie całki funkcji f(x) = 1/2 * x na przedziale [{a}, {b}]")
        print(f"Liczba prostokątów: {n}")
        print(f"Szerokość prostokąta (dx): {dx:.4f}")
        print("\nObliczenia dla poszczególnych prostokątów:")
        print(f"{'Lp.':<6} {'Przedział x':<20} {'f(x)':<10} {'Pole':<10}")
        print("-" * 50)
        
        # Oblicz każdy prostokąt
        for i in range(n):
            # Lewa granica bieżącego prostokąta
            x_start = a + i * dx
            # Prawa granica bieżącego prostokąta
            x_end = x_start + dx
            # Punkt środkowy prostokąta
            x_mid = (x_start + x_end) / 2
            
            # Wartość funkcji w punkcie środkowym
            f_x = self.function_1(x_mid)
            
            # Pole prostokąta (używając reguły punktu środkowego)
            area = f_x * dx
            total_area += area
            
            # Wyświetl obliczenia (tylko pierwsze 10 i ostatnie, jeśli jest więcej)
            if i < 10 or i >= n - 1:
                print(f"{i+1:<6} [{x_start:.4f}, {x_end:.4f}] {f_x:.4f}     {area:.6f}")
            elif i == 10 and n > 12:
                print(f"... ({n - 12} wierszy pominięto) ...")
        
        print("-" * 50)
        print(f"Całkowita suma (całka przybliżona): {total_area:.6f}\n")
        
        return total_area
    
    def run_task3(self):
        """
        Zadanie 3: Oblicz numeryczną wartość całki metodą prostokątów.
        """
        try:
            # Pobierz liczbę prostokątów od użytkownika
            n = InputValidator.get_positive_integer(
                "\nPodaj liczbę prostokątów (elementów) do aproksymacji: ",
                "Liczba prostokątów musi być większa od zera."
            )
            
            # Oblicz całkę na przedziale [0, 2]
            a = 0
            b = 2
            result = self.calculate_integral_rectangles(a, b, n)
            
            # Wyświetl wynik
            print(f"Przybliżona wartość całki: {result:.6f}")
            
        except Exception as e:
            print(f"Błąd: {e}")
