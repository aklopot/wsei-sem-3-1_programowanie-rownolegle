"""
Moduł do obliczania całek numerycznych
Zawiera klasę IntegralCalculator do obliczania całek metodą prostokątów.
Laboratorium 3: Rozbudowa o różne metody wielowątkowości.
"""

import math
from enum import Enum
from src.validators.input_validator import InputValidator
from src.modules.parallel_integral_calculator import ParallelIntegralCalculator
from src.modules.executor_integral_calculator import ExecutorIntegralCalculator
from src.modules.threadpool_integral_calculator import ThreadPoolIntegralCalculator
from src.modules.background_worker_calculator import BackgroundWorkerCalculator
from src.modules.benchmark_runner import BenchmarkRunner


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
        """
        return 0.5 * x
    
    def function_sin(self, x):
        """
        Funkcja do całkowania: f(x) = sin(x)
        """
        return math.sin(x)
    
    def function_quadratic(self, x, a, b, c):
        """
        Funkcja do całkowania: f(x) = ax² + bx + c
        """
        return a * x**2 + b * x + c
    
    def function_task1_1(self, x):
        """
        Funkcja zadania 1: y = 2x + 2x²
        """
        return 2 * x + 2 * x**2
    
    def function_task1_2(self, x):
        """
        Funkcja zadania 1: y = 2x²
        """
        return 2 * x**2
    
    def function_task1_3(self, x):
        """
        Funkcja zadania 1: y = 2x - 3
        """
        return 2 * x - 3
    
    def _get_exact_integral_linear(self, a, b):
        """f(x) = 1/2 * x"""
        return 0.25 * (b**2 - a**2)
    
    def _get_exact_integral_sin(self, a, b):
        """f(x) = sin(x): -cos(b) + cos(a)"""
        return -math.cos(b) + math.cos(a)
    
    def _get_exact_integral_quadratic(self, x_start, x_end, a, b, c):
        """
        f(x) = ax² + bx + c
        """
        def antiderivative(x):
            return (a / 3) * x**3 + (b / 2) * x**2 + c * x
        
        return antiderivative(x_end) - antiderivative(x_start)
    
    def _print_calculation_header(self, a, b, n, method_description, func_description="f(x) = 1/2 * x"):
        """
        Wyświetl nagłówek obliczeń.
        """
        print(f"\nObliczanie całki funkcji {func_description} na przedziale [{a}, {b}]")
        print(f"Metoda: {method_description}")
        print(f"Liczba elementów: {n}")
    
    def _print_calculation_summary(self, total_area, exact_value):
        """
        Wyświetl podsumowanie obliczeń.
        """
        print("-" * 50)
        print(f"Całkowita suma (aproksymacja): {total_area:.6f}")
        print(f"Dokładna wartość całki:        {exact_value:.6f}")
        print(f"Błąd aproksymacji:             {abs(total_area - exact_value):.6f}")
        
        if exact_value != 0:
            error_percent = abs(total_area - exact_value) / abs(exact_value) * 100
            print(f"Błąd względny:                 {error_percent:.4f}%\n")
        else:
            print(f"Błąd względny:                 N/A (wartość dokładna = 0)\n")
    
    def _calculate_integral_rectangles_generic(self, a, b, n, method, func, func_description, exact_value):
        """
        Oblicz całkę metodą prostokątów dla dowolnej funkcji.
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
    
    def _calculate_integral_trapezoids_simple(self, a, b, n, func):
        """
        Calculate integral using trapezoidal rule without detailed output.
        Returns only the result value.
        
        Args:
            a (float): Start of interval
            b (float): End of interval
            n (int): Number of trapezoids
            func (callable): Function to integrate
            
        Returns:
            float: Calculated integral value
        """
        if n <= 0:
            raise ValueError("Liczba trapezów musi być większa od zera.")
        
        dx = (b - a) / n
        total_area = 0.0
        
        for i in range(n):
            x_start = a + i * dx
            x_end = x_start + dx
            
            f_left = func(x_start)
            f_right = func(x_end)
            
            area = (f_left + f_right) / 2 * dx
            total_area += area
        
        return total_area
    
    def _calculate_integral_trapezoids_generic(self, a, b, n, func, func_description, exact_value):
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
            
            results = []

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
            
            # Calculate exact value: ∫sin(x)dx = -cos(x), from 0 to 2π = -cos(2π) + cos(0) = -1 + 1 = 0
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
    
    def run_task8(self):
        """
        Zadanie 8: Oblicz całkę funkcji y = ax² + bx + c.
        Parametry a, b, c podawane przez użytkownika.
        """
        try:
            print("=" * 80)
            print("ZADANIE 8 - CAŁKA FUNKCJI KWADRATOWEJ y = ax² + bx + c")
            print("=" * 80)
            print()
            
            # Get coefficients from user
            print("Podaj współczynniki funkcji kwadratowej y = ax² + bx + c:")
            a_coef = InputValidator.get_float("\nWspółczynnik a: ")
            b_coef = InputValidator.get_float("Współczynnik b: ")
            c_coef = InputValidator.get_float("Współczynnik c: ")
            
            # Get interval from user
            print("\nPodaj przedział całkowania [x_start, x_end]:")
            x_start = InputValidator.get_float("x_start: ")
            x_end = InputValidator.get_float("x_end: ")
            
            if x_start >= x_end:
                print("Błąd: x_start musi być mniejsze od x_end")
                return
            
            # Get number of elements
            n = InputValidator.get_positive_integer(
                "\nPodaj liczbę elementów do aproksymacji: ",
                "Liczba elementów musi być większa od zera."
            )
            
            print()
            print("=" * 80)
            
            # Display function
            func_str = f"f(x) = {a_coef}x² + {b_coef}x + {c_coef}"
            print(f"Funkcja: {func_str}")
            print(f"Przedział: [{x_start}, {x_end}]")
            print(f"Liczba elementów: {n}")
            
            # Calculate exact value
            exact_value = self._get_exact_integral_quadratic(x_start, x_end, a_coef, b_coef, c_coef)
            print(f"Dokładna wartość całki: {exact_value:.6f}")
            print()
            print("=" * 80)
            print()
            
            # Store results for comparison
            results = []
            
            # Create a lambda function with fixed coefficients
            quad_func = lambda x: self.function_quadratic(x, a_coef, b_coef, c_coef)
            
            # Calculate using rectangles (center method)
            print(f"{'='*80}")
            print(f"METODA: PROSTOKĄTY (ŚRODEK)")
            print(f"{'='*80}")
            rect_result = self._calculate_integral_rectangles_generic(
                x_start, x_end, n, CalculationMethod.CENTER, quad_func, func_str, exact_value
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
                x_start, x_end, n, quad_func, func_str, exact_value
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
            print("PODSUMOWANIE WYNIKÓW - FUNKCJA KWADRATOWA")
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
    
    def run_task1(self):
        """
        Zadanie 1: Oblicz numeryczną wartość całki dla wybranej funkcji
        na trzech przedziałach metodą trapezów (jednowątkowo, synchronicznie).
        
        Funkcje do wyboru:
        1. y = 2x + 2x²
        2. y = 2x²
        3. y = 2x - 3
        
        Przedziały całkowania:
        1. Od -10 do 10
        2. Od -5 do 20
        3. Od -5 do 0
        """
        import time
        
        try:
            print("=" * 80)
            print("ZADANIE 1 - OBLICZANIE CAŁKI NUMERYCZNEJ METODĄ TRAPEZÓW")
            print("=" * 80)
            print("\nWybierz funkcję do całkowania:")
            print("1 - y = 2x + 2x²")
            print("2 - y = 2x²")
            print("3 - y = 2x - 3")
            print()
            
            # Get function choice
            function_choice = InputValidator.get_integer_in_range(
                "Wybierz funkcję (1-3): ",
                1, 3,
                "Wybierz liczbę od 1 do 3."
            )
            
            # Select function based on choice
            functions = {
                1: (self.function_task1_1, "y = 2x + 2x²"),
                2: (self.function_task1_2, "y = 2x²"),
                3: (self.function_task1_3, "y = 2x - 3")
            }
            
            selected_func, func_description = functions[function_choice]
            
            # Define intervals
            intervals = [
                (-10, 10, "Od -10 do 10"),
                (-5, 20, "Od -5 do 20"),
                (-5, 0, "Od -5 do 0")
            ]
            
            # Number of trapezoids (using reasonable default)
            n = 10000
            
            print()
            print("=" * 80)
            print(f"Funkcja: {func_description}")
            print(f"Liczba trapezów: {n}")
            print("Metoda: trapezy")
            print("=" * 80)
            print()
            
            # Start timing
            start_time = time.time()
            
            # Calculate integrals for each interval synchronously
            results = []
            for i, (a, b, interval_desc) in enumerate(intervals, 1):
                print(f"Obliczanie całki dla przedziału {i}: [{a}, {b}] ({interval_desc})...")
                
                # Measure time for this interval
                interval_start_time = time.time()
                result = self._calculate_integral_trapezoids_simple(a, b, n, selected_func)
                interval_end_time = time.time()
                interval_time_ms = (interval_end_time - interval_start_time) * 1000
                
                results.append({
                    'interval': interval_desc,
                    'a': a,
                    'b': b,
                    'result': result,
                    'time_ms': interval_time_ms
                })
                print(f"Wynik: {result:.6f}")
                print(f"Czas obliczeń: {interval_time_ms:.2f} milisekund")
                print()
            
            # End timing
            end_time = time.time()
            total_time_ms = (end_time - start_time) * 1000
            
            # Display summary
            print("=" * 80)
            print("PODSUMOWANIE WYNIKÓW")
            print("=" * 80)
            print(f"\n{'Przedział':<20} {'Wartość całki':<20}")
            print("-" * 80)
            for result in results:
                print(f"[{result['a']:>5}, {result['b']:>5}]         {result['result']:>15.6f}")
            print("-" * 80)
            print(f"\nCałkowity czas obliczeń: {total_time_ms:.2f} milisekund")
            print("=" * 80)
            
        except Exception as e:
            print(f"Błąd: {e}")
    
    def run_task2(self):
        """
        Zadanie 2: Oblicz całkę dla trzech przedziałów równocześnie
        używając wątków (threading). Pokazuje postęp obliczeń na konsoli.
        """
        try:
            print("=" * 80)
            print("ZADANIE 2 - OBLICZANIE CAŁKI RÓWNOLEGŁY (WĄTKI)")
            print("=" * 80)
            print("\nWybierz funkcję do całkowania:")
            print("1 - y = 2x + 2x²")
            print("2 - y = 2x²")
            print("3 - y = 2x - 3")
            print()
            
            function_choice = InputValidator.get_integer_in_range(
                "Wybierz funkcję (1-3): ",
                1, 3,
                "Wybierz liczbę od 1 do 3."
            )
            
            functions = {
                1: (self.function_task1_1, "y = 2x + 2x²"),
                2: (self.function_task1_2, "y = 2x²"),
                3: (self.function_task1_3, "y = 2x - 3")
            }
            
            selected_func, func_description = functions[function_choice]
            
            intervals = [
                (-10, 10, "Od -10 do 10"),
                (-5, 20, "Od -5 do 20"),
                (-5, 0, "Od -5 do 0")
            ]
            
            n = 10000
            
            print()
            print("=" * 80)
            print(f"Funkcja: {func_description}")
            print(f"Liczba trapezów: {n}")
            print("Metoda: trapezy (wielowątkowe)")
            print("=" * 80)
            print()
            
            calculator = ParallelIntegralCalculator(selected_func, n)
            calculator.compute_all(intervals)
        
        except Exception as e:
            print(f"Błąd: {e}")
    
    def run_task3(self):
        """
        Zadanie 3: Wybór metody przetwarzania równoległego.
        1 - threading.Thread (ręczna wielowątkowość)
        2 - concurrent.futures ThreadPoolExecutor (TPL-like)
        """
        try:
            print("=" * 80)
            print("ZADANIE 3 - WYBÓR METODY PRZETWARZANIA")
            print("=" * 80)
            print("\nWybierz metodę przetwarzania równoległego:")
            print("1 - threading.Thread (ręczna wielowątkowość)")
            print("2 - ThreadPoolExecutor (concurrent.futures)")
            print()
            
            method_choice = InputValidator.get_integer_in_range(
                "Wybierz metodę (1-2): ",
                1, 2,
                "Wybierz 1 lub 2."
            )
            
            print("\nWybierz funkcję do całkowania:")
            print("1 - y = 2x + 2x²")
            print("2 - y = 2x²")
            print("3 - y = 2x - 3")
            print()
            
            function_choice = InputValidator.get_integer_in_range(
                "Wybierz funkcję (1-3): ",
                1, 3,
                "Wybierz liczbę od 1 do 3."
            )
            
            functions = {
                1: (self.function_task1_1, "y = 2x + 2x²"),
                2: (self.function_task1_2, "y = 2x²"),
                3: (self.function_task1_3, "y = 2x - 3")
            }
            
            selected_func, func_description = functions[function_choice]
            
            intervals = [
                (-10, 10, "Od -10 do 10"),
                (-5, 20, "Od -5 do 20"),
                (-5, 0, "Od -5 do 0")
            ]
            
            n = 10000
            
            method_name = "threading.Thread" if method_choice == 1 else "ThreadPoolExecutor"
            
            print()
            print("=" * 80)
            print(f"Funkcja: {func_description}")
            print(f"Liczba trapezów: {n}")
            print(f"Metoda równoległości: {method_name}")
            print("=" * 80)
            print()
            
            if method_choice == 1:
                calculator = ParallelIntegralCalculator(selected_func, n)
            else:
                calculator = ExecutorIntegralCalculator(selected_func, n)
            
            calculator.compute_all(intervals)
        
        except Exception as e:
            print(f"Błąd: {e}")
    
    # ==================== LABORATORIUM 3 ====================
    
    def _get_function_choice(self):
        """Pobiera wybór funkcji od użytkownika."""
        print("\nWybierz funkcję do całkowania:")
        print("1 - y = 2x + 2x²")
        print("2 - y = 2x²")
        print("3 - y = 2x - 3")
        print()
        
        function_choice = InputValidator.get_integer_in_range(
            "Wybierz funkcję (1-3): ",
            1, 3,
            "Wybierz liczbę od 1 do 3."
        )
        
        functions = {
            1: (self.function_task1_1, "y = 2x + 2x²"),
            2: (self.function_task1_2, "y = 2x²"),
            3: (self.function_task1_3, "y = 2x - 3")
        }
        
        return functions[function_choice]
    
    def _get_default_intervals(self):
        """Zwraca domyślne przedziały."""
        return [
            (-10, 10, "[-10,10]"),
            (-5, 20, "[-5,20]"),
            (-5, 0, "[-5,0]")
        ]
    
    def run_thread_calculation(self):
        """Lab 3: Obliczanie całki metodą Thread."""
        try:
            print("=" * 60)
            print("OBLICZANIE CAŁKI - Thread")
            print("=" * 60)
            
            selected_func, func_description = self._get_function_choice()
            intervals = self._get_default_intervals()
            n = 10000
            
            print()
            print(f"Funkcja: {func_description}")
            print(f"Liczba trapezów: {n}")
            print()
            
            calculator = ParallelIntegralCalculator(selected_func, n)
            calculator.compute_all(intervals)
        
        except Exception as e:
            print(f"Błąd: {e}")
    
    def run_threadpool_calculation(self):
        """Lab 3: Obliczanie całki metodą ThreadPool."""
        try:
            print("=" * 60)
            print("OBLICZANIE CAŁKI - ThreadPool")
            print("=" * 60)
            
            selected_func, func_description = self._get_function_choice()
            intervals = self._get_default_intervals()
            n = 10000
            
            print()
            print(f"Funkcja: {func_description}")
            print(f"Liczba trapezów: {n}")
            print()
            
            calculator = ThreadPoolIntegralCalculator(selected_func, n)
            calculator.compute_all(intervals)
        
        except Exception as e:
            print(f"Błąd: {e}")
    
    def run_tpl_calculation(self):
        """Lab 3: Obliczanie całki metodą TPL (Executor)."""
        try:
            print("=" * 60)
            print("OBLICZANIE CAŁKI - TPL")
            print("=" * 60)
            
            selected_func, func_description = self._get_function_choice()
            intervals = self._get_default_intervals()
            n = 10000
            
            print()
            print(f"Funkcja: {func_description}")
            print(f"Liczba trapezów: {n}")
            print()
            
            calculator = ExecutorIntegralCalculator(selected_func, n)
            calculator.compute_all(intervals)
        
        except Exception as e:
            print(f"Błąd: {e}")
    
    def run_backgroundworker_calculation(self):
        """Lab 3: Obliczanie całki metodą BackgroundWorker."""
        try:
            print("=" * 60)
            print("OBLICZANIE CAŁKI - BackgroundWorker")
            print("=" * 60)
            
            selected_func, func_description = self._get_function_choice()
            intervals = self._get_default_intervals()
            n = 10000
            
            print()
            print(f"Funkcja: {func_description}")
            print(f"Liczba trapezów: {n}")
            print()
            
            calculator = BackgroundWorkerCalculator(selected_func, n)
            calculator.compute_all(intervals)
        
        except Exception as e:
            print(f"Błąd: {e}")
    
    def run_benchmark(self):
        """Lab 3 - Zadanie 3: Porównanie wszystkich metod."""
        try:
            print("=" * 60)
            print("BENCHMARK - PORÓWNANIE METOD")
            print("=" * 60)
            
            selected_func, func_description = self._get_function_choice()
            n = 10000
            
            print()
            print(f"Funkcja: {func_description}")
            print(f"Liczba trapezów: {n}")
            print()
            
            runner = BenchmarkRunner(selected_func, n)
            results = runner.run_all_benchmarks()
            runner.display_results(results)
        
        except Exception as e:
            print(f"Błąd: {e}")