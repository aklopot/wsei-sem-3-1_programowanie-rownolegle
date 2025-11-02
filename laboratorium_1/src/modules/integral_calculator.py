"""
Moduł do obliczania całek numerycznych
Zawiera klasę IntegralCalculator do obliczania całek metodą prostokątów.
"""

import math
from enum import Enum
from src.validators.input_validator import InputValidator


class CalculationMethod(Enum):
    """Enum representing different methods for calculating integral using rectangles."""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


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
    
    def function_sin(self, x):
        """
        Funkcja do całkowania: f(x) = sin(x)
        
        Args:
            x (float): Wartość wejściowa
        Returns:
            float: Wartość funkcji dla x
        """
        return math.sin(x)
    
    def _get_exact_integral_linear(self, a, b):
        """Calculate exact integral for f(x) = 1/2 * x"""
        return 0.25 * (b**2 - a**2)
    
    def _get_exact_integral_sin(self, a, b):
        """Calculate exact integral for f(x) = sin(x): -cos(b) + cos(a)"""
        return -math.cos(b) + math.cos(a)
    
    def _print_calculation_header(self, a, b, n, method_description, func_description="f(x) = 1/2 * x"):
        """
        Helper method to print calculation header.
        
        Args:
            a (float): Left boundary
            b (float): Right boundary
            n (int): Number of elements
            method_description (str): Description of the method
            func_description (str): Description of the function being integrated
        """
        print(f"\nObliczanie całki funkcji {func_description} na przedziale [{a}, {b}]")
        print(f"Metoda: {method_description}")
        print(f"Liczba elementów: {n}")
    
    def _print_calculation_summary(self, total_area, exact_value):
        """
        Helper method to print calculation summary.
        
        Args:
            total_area (float): Calculated integral value
            exact_value (float): Exact integral value
        """
        print("-" * 50)
        print(f"Całkowita suma (aproksymacja): {total_area:.6f}")
        print(f"Dokładna wartość całki:        {exact_value:.6f}")
        print(f"Błąd aproksymacji:             {abs(total_area - exact_value):.6f}")
        print(f"Błąd względny:                 {abs(total_area - exact_value) / exact_value * 100:.4f}%\n")
    
    def _calculate_integral_rectangles_generic(self, a, b, n, method, func, func_description, exact_value):
        """
        Generic method to calculate integral using rectangles for any function.
        
        Args:
            a (float): Left boundary
            b (float): Right boundary
            n (int): Number of rectangles
            method (CalculationMethod): Calculation method (LEFT, CENTER, RIGHT)
            func (callable): Function to integrate
            func_description (str): Description of the function
            exact_value (float): Exact value of the integral
        
        Returns:
            float: Approximated integral value
        """
        if n <= 0:
            raise ValueError("Liczba prostokątów musi być większa od zera.")
        
        dx = (b - a) / n
        total_area = 0.0
        
        method_names = {
            CalculationMethod.LEFT: "prostokąty z lewym brzegiem",
            CalculationMethod.CENTER: "prostokąty ze środkiem",
            CalculationMethod.RIGHT: "prostokąty z prawym brzegiem"
        }
        
        self._print_calculation_header(a, b, n, method_names[method], func_description)
        print(f"Szerokość prostokąta (dx): {dx:.4f}")
        
        print("\nObliczenia dla poszczególnych prostokątów:")
        print(f"{'Lp.':<6} {'Przedział x':<20} {'f(x)':<10} {'Pole':<10}")
        print("-" * 50)
        
        for i in range(n):
            x_start = a + i * dx
            x_end = x_start + dx
            
            if method == CalculationMethod.LEFT:
                x_eval = x_start
            elif method == CalculationMethod.CENTER:
                x_eval = (x_start + x_end) / 2
            elif method == CalculationMethod.RIGHT:
                x_eval = x_end
            else:
                raise ValueError(f"Unknown calculation method: {method}")
            
            f_x = func(x_eval)
            area = f_x * dx
            total_area += area
            
            if i < 10 or i >= n - 1:
                print(f"{i+1:<6} [{x_start:.4f}, {x_end:.4f}] {f_x:.4f}     {area:.6f}")
            elif i == 10 and n > 11:
                print(f"... ({n - 11} wierszy pominięto) ...")
        
        self._print_calculation_summary(total_area, exact_value)
        return total_area
    
    def _calculate_integral_trapezoids_generic(self, a, b, n, func, func_description, exact_value):
        """
        Generic method to calculate integral using trapezoids for any function.
        
        Args:
            a (float): Left boundary
            b (float): Right boundary
            n (int): Number of trapezoids
            func (callable): Function to integrate
            func_description (str): Description of the function
            exact_value (float): Exact value of the integral
        
        Returns:
            float: Approximated integral value
        """
        if n <= 0:
            raise ValueError("Liczba trapezów musi być większa od zera.")
        
        dx = (b - a) / n
        total_area = 0.0
        
        self._print_calculation_header(a, b, n, "trapezy", func_description)
        print(f"Szerokość podstawy (dx): {dx:.4f}")
        
        print("\nObliczenia dla poszczególnych trapezów:")
        print(f"{'Lp.':<6} {'Przedział x':<20} {'f(x_l), f(x_r)':<20} {'Pole':<10}")
        print("-" * 60)
        
        for i in range(n):
            x_start = a + i * dx
            x_end = x_start + dx
            
            f_left = func(x_start)
            f_right = func(x_end)
            
            area = (f_left + f_right) / 2 * dx
            total_area += area
            
            if i < 10 or i >= n - 1:
                print(f"{i+1:<6} [{x_start:.4f}, {x_end:.4f}] "
                      f"{f_left:.4f}, {f_right:.4f}   {area:.6f}")
            elif i == 10 and n > 11:
                print(f"... ({n - 11} wierszy pominięto) ...")
        
        self._print_calculation_summary(total_area, exact_value)
        return total_area
    
    def calculate_integral_rectangles(self, a, b, n, method=CalculationMethod.LEFT):
        """
        Oblicz całkę metodą prostokątów dla funkcji f(x) = 1/2 * x.
        
        Args:
            a (float): Lewa granica przedziału
            b (float): Prawa granica przedziału
            n (int): Liczba prostokątów (podział)
            method (CalculationMethod): Metoda obliczania (LEFT, CENTER, RIGHT)
        
        Returns:
            float: Przybliżona wartość całki
        """
        exact_value = self._get_exact_integral_linear(a, b)
        return self._calculate_integral_rectangles_generic(
            a, b, n, method, self.function_1, "f(x) = 1/2 * x", exact_value
        )
    
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
    
    def run_task5(self):
        """
        Zadanie 5: Porównanie dokładności różnych metod obliczania całki.
        Porównuje wyniki dla trzech metod: lewej, środka i prawej krawędzi.
        """
        try:
            # Pobierz liczbę prostokątów od użytkownika
            n = InputValidator.get_positive_integer(
                "\nPodaj liczbę prostokątów (elementów) do aproksymacji: ",
                "Liczba prostokątów musi być większa od zera."
            )
            
            print("=" * 80)
            print("ZADANIE 5 - PORÓWNANIE METOD OBLICZANIA CAŁKI")
            print("=" * 80)
            print()
            
            # Define interval
            a = 0
            b = 2
            
            print("Funkcja: f(x) = 1/2 * x")
            print(f"Przedział: [{a}, {b}]")
            print(f"Liczba prostokątów: {n}")
            
            # Calculate exact value
            exact_value = 0.25 * (b**2 - a**2)
            print(f"Dokładna wartość całki: {exact_value:.6f}")
            print()
            print("=" * 80)
            print()
            
            # Store results for comparison
            results = []
            
            # Define methods to test
            methods = [
                (CalculationMethod.LEFT, "Lewa krawędź"),
                (CalculationMethod.CENTER, "Środek"),
                (CalculationMethod.RIGHT, "Prawa krawędź")
            ]
            
            # Calculate for each method
            for method, method_name in methods:
                print(f"{'='*80}")
                print(f"METODA: {method_name.upper()}")
                print(f"{'='*80}")
                result = self.calculate_integral_rectangles(a, b, n, method=method)
                results.append({
                    'method': method_name,
                    'value': result,
                    'error': abs(result - exact_value),
                    'error_percent': abs(result - exact_value) / exact_value * 100
                })
                print()
            
            # Display summary
            print("=" * 80)
            print("PODSUMOWANIE WYNIKÓW - PORÓWNANIE METOD")
            print("=" * 80)
            print(f"\n{'Metoda':<20} {'Wartość':<15} {'Błąd bezwzgl.':<15} {'Błąd wzgl.':<15}")
            print("-" * 80)
            for result in results:
                print(f"{result['method']:<20} {result['value']:<15.6f} "
                      f"{result['error']:<15.6f} {result['error_percent']:<15.4f}%")
            print("-" * 80)
            print(f"Dokładna wartość: {exact_value:.6f}")
            print()
            
        except Exception as e:
            print(f"Błąd: {e}")
    
    def calculate_integral_trapezoids(self, a, b, n):
        """
        Oblicz całkę metodą trapezów dla funkcji f(x) = 1/2 * x.
        
        Args:
            a (float): Lewa granica przedziału
            b (float): Prawa granica przedziału
            n (int): Liczba trapezów (podział)
        
        Returns:
            float: Przybliżona wartość całki
        """
        exact_value = self._get_exact_integral_linear(a, b)
        return self._calculate_integral_trapezoids_generic(
            a, b, n, self.function_1, "f(x) = 1/2 * x", exact_value
        )
    
    def run_task6(self):
        """
        Zadanie 6: Porównanie metody prostokątów i trapezów.
        Analizuje wpływ zmiany elementu aproksymującego (prostokąt -> trapez).
        """
        try:
            # Pobierz liczbę elementów od użytkownika
            n = InputValidator.get_positive_integer(
                "\nPodaj liczbę elementów do aproksymacji: ",
                "Liczba elementów musi być większa od zera."
            )
            
            print("=" * 80)
            print("ZADANIE 6 - PORÓWNANIE PROSTOKĄTÓW I TRAPEZÓW")
            print("=" * 80)
            print()
            
            # Define interval
            a = 0
            b = 2
            
            print("Funkcja: f(x) = 1/2 * x")
            print(f"Przedział: [{a}, {b}]")
            print(f"Liczba elementów: {n}")
            
            # Calculate exact value
            exact_value = 0.25 * (b**2 - a**2)
            print(f"Dokładna wartość całki: {exact_value:.6f}")
            print()
            print("=" * 80)
            print()
            
            # Store results for comparison
            results = []
            
            # Calculate using rectangles (left edge method)
            print(f"{'='*80}")
            print(f"METODA: PROSTOKĄTY (LEWA KRAWĘDŹ)")
            print(f"{'='*80}")
            rect_result = self.calculate_integral_rectangles(a, b, n, method=CalculationMethod.LEFT)
            results.append({
                'method': 'Prostokąty',
                'value': rect_result,
                'error': abs(rect_result - exact_value),
                'error_percent': abs(rect_result - exact_value) / exact_value * 100
            })
            print()
            
            # Calculate using trapezoids
            print(f"{'='*80}")
            print(f"METODA: TRAPEZY")
            print(f"{'='*80}")
            trap_result = self.calculate_integral_trapezoids(a, b, n)
            results.append({
                'method': 'Trapezy',
                'value': trap_result,
                'error': abs(trap_result - exact_value),
                'error_percent': abs(trap_result - exact_value) / exact_value * 100
            })
            print()
            
            # Display summary
            print("=" * 80)
            print("PODSUMOWANIE WYNIKÓW - PROSTOKĄTY VS TRAPEZY")
            print("=" * 80)
            print(f"\n{'Metoda':<20} {'Wartość':<15} {'Błąd bezwzgl.':<15} {'Błąd wzgl.':<15}")
            print("-" * 80)
            for result in results:
                print(f"{result['method']:<20} {result['value']:<15.6f} "
                      f"{result['error']:<15.6f} {result['error_percent']:<15.4f}%")
            print("-" * 80)
            print(f"Dokładna wartość: {exact_value:.6f}")
            print()
            
        except Exception as e:
            print(f"Błąd: {e}")
    
    def run_task7(self):
        """
        Zadanie 7: Oblicz całkę funkcji y=sin(x) na przedziale [0, 2π].
        Porównuje wyniki dla metody prostokątów i trapezów.
        """
        try:
            # Pobierz liczbę elementów od użytkownika
            n = InputValidator.get_positive_integer(
                "\nPodaj liczbę elementów do aproksymacji: ",
                "Liczba elementów musi być większa od zera."
            )
            
            print("=" * 80)
            print("ZADANIE 7 - CAŁKA FUNKCJI y=sin(x)")
            print("=" * 80)
            print()
            
            # Define interval [0, 2π]
            a = 0
            b = 2 * math.pi
            
            print("Funkcja: f(x) = sin(x)")
            print(f"Przedział: [0, 2π] = [0, {b:.4f}]")
            print(f"Liczba elementów: {n}")
            
            # Calculate exact value: ∫sin(x)dx = -cos(x), from 0 to 2π
            exact_value = self._get_exact_integral_sin(a, b)
            print(f"Dokładna wartość całki: {exact_value:.6f}")
            print()
            print("=" * 80)
            print()
            
            # Store results for comparison
            results = []
            
            # Calculate using rectangles (center method - best for sin)
            print(f"{'='*80}")
            print(f"METODA: PROSTOKĄTY (ŚRODEK)")
            print(f"{'='*80}")
            rect_result = self._calculate_integral_rectangles_generic(
                a, b, n, CalculationMethod.CENTER, self.function_sin, "f(x) = sin(x)", exact_value
            )
            results.append({
                'method': 'Prostokąty (środek)',
                'value': rect_result,
                'error': abs(rect_result - exact_value),
                'error_percent': abs(rect_result - exact_value) / abs(exact_value) * 100 if exact_value != 0 else 0
            })
            print()
            
            # Calculate using trapezoids
            print(f"{'='*80}")
            print(f"METODA: TRAPEZY")
            print(f"{'='*80}")
            trap_result = self._calculate_integral_trapezoids_generic(
                a, b, n, self.function_sin, "f(x) = sin(x)", exact_value
            )
            results.append({
                'method': 'Trapezy',
                'value': trap_result,
                'error': abs(trap_result - exact_value),
                'error_percent': abs(trap_result - exact_value) / abs(exact_value) * 100 if exact_value != 0 else 0
            })
            print()
            
            # Display summary
            print("=" * 80)
            print("PODSUMOWANIE WYNIKÓW - CAŁKA sin(x)")
            print("=" * 80)
            print(f"\n{'Metoda':<25} {'Wartość':<15} {'Błąd bezwzgl.':<15} {'Błąd wzgl.':<15}")
            print("-" * 80)
            for result in results:
                print(f"{result['method']:<25} {result['value']:<15.6f} "
                      f"{result['error']:<15.6f} {result['error_percent']:<15.4f}%")
            print("-" * 80)
            print(f"Dokładna wartość: {exact_value:.6f}")
            print()
            
        except Exception as e:
            print(f"Błąd: {e}")
