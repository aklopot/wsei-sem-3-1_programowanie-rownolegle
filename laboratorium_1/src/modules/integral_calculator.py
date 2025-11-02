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
        print(f"Metoda: prostokąty z lewym brzegiem")
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
            
            # Wartość funkcji w lewym brzegu prostokąta
            f_x = self.function_1(x_start)
            
            # Pole prostokąta (używając reguły lewego brzegu)
            area = f_x * dx
            total_area += area
            
            # Wyświetl obliczenia (tylko pierwsze 10 i ostatnie, jeśli jest więcej)
            if i < 10 or i >= n - 1:
                print(f"{i+1:<6} [{x_start:.4f}, {x_end:.4f}] {f_x:.4f}     {area:.6f}")
            elif i == 10 and n > 11:
                print(f"... ({n - 11} wierszy pominięto) ...")
        
        # Dokładna wartość całki dla porównania (∫(1/2 * x) dx = 1/4 * x²)
        exact_value = 0.25 * (b**2 - a**2)
        print("-" * 50)
        print(f"Całkowita suma (aproksymacja): {total_area:.6f}")
        print(f"Dokładna wartość całki:        {exact_value:.6f}")
        print(f"Błąd aproksymacji:             {abs(total_area - exact_value):.6f}")
        print(f"Błąd względny:                 {abs(total_area - exact_value) / exact_value * 100:.4f}%\n")
        
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
            self.calculate_integral_rectangles(a, b, n)
            
        except Exception as e:
            print(f"Błąd: {e}")
    
    def run_task4(self):
        """
        Zadanie 4: Analiza wpływu liczby elementów na dokładność.
        Porównuje dokładność dla różnych liczb prostokątów (n=3, 7, 13).
        """
        print("=" * 60)
        print("ZADANIE 4 - WPŁYW LICZBY ELEMENTÓW NA DOKŁADNOŚĆ")
        print("=" * 60)
        print()
        
        # Test with different numbers of rectangles
        test_values = [3, 7, 13]
        
        # Define interval
        a = 0
        b = 2
        
        print("Funkcja: f(x) = 1/2 * x")
        print(f"Przedział: [{a}, {b}]")
        print("Metoda: prostokąty z lewym brzegiem")
        
        # Calculate exact value
        exact_value = 0.25 * (b**2 - a**2)
        print(f"Dokładna wartość całki: {exact_value:.6f}")
        print()
        print("=" * 60)
        print()
        
        # Store results for comparison
        results = []
        
        # Calculate for each test value
        for n in test_values:
            print(f"{'='*60}")
            print(f"TEST DLA n = {n} PROSTOKĄTÓW")
            print(f"{'='*60}")
            result = self.calculate_integral_rectangles(a, b, n)
            results.append({
                'n': n,
                'value': result,
                'error': abs(result - exact_value),
                'error_percent': abs(result - exact_value) / exact_value * 100
            })
            print()
        
        # Display summary
        print("=" * 60)
        print("PODSUMOWANIE WYNIKÓW")
        print("=" * 60)
        print(f"\n{'n':<10} {'Wartość':<15} {'Błąd bezwzgl.':<15} {'Błąd wzgl.':<15}")
        print("-" * 60)
        for result in results:
            print(f"{result['n']:<10} {result['value']:<15.6f} "
                  f"{result['error']:<15.6f} {result['error_percent']:<15.4f}%")
        print("-" * 60)
        print(f"Dokładna wartość: {exact_value:.6f}")
        print()
