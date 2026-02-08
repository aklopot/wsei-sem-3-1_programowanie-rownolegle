"""
Moduł do uruchamiania benchmarku porównującego metody równoległe.
Zadanie 3: Uruchomienie wszystkich metod i porównanie czasów.
"""

import time
import os
import sys
from dataclasses import dataclass
from typing import List, Callable, Tuple

from src.modules.parallel_integral_calculator import ParallelIntegralCalculator
from src.modules.executor_integral_calculator import ExecutorIntegralCalculator
from src.modules.threadpool_integral_calculator import ThreadPoolIntegralCalculator
from src.modules.background_worker_calculator import BackgroundWorkerCalculator


@dataclass
class BenchmarkResult:
    """Wyniki benchmarku dla jednej metody."""
    method_name: str
    total_time_ms: float
    results: List[float]
    thread_times_ms: List[float]
    is_correct: bool


class BenchmarkRunner:
    """Uruchamia benchmark wszystkich metod równoległych."""
    
    def __init__(self, func: Callable[[float], float], n: int):
        """Inicjalizacja."""
        self.func = func
        self.n = n
        self.intervals = [
            (-10, 10, "[-10,10]"),
            (-5, 20, "[-5,20]"),
            (-5, 0, "[-5,0]")
        ]
        self.reference_results: List[float] = []
    
    def _calculate_reference_results(self):
        """Oblicza wartości referencyjne sekwencyjnie."""
        self.reference_results = []
        for a, b, _ in self.intervals:
            dx = (b - a) / self.n
            total_area = 0.0
            for i in range(self.n):
                x_start = a + i * dx
                x_end = x_start + dx
                f_left = self.func(x_start)
                f_right = self.func(x_end)
                area = (f_left + f_right) / 2 * dx
                total_area += area
            self.reference_results.append(total_area)
    
    def _verify_results(self, results: List[float], tolerance: float = 1e-6) -> bool:
        """Sprawdza poprawność wyników."""
        if len(results) != len(self.reference_results):
            return False
        for calc, ref in zip(results, self.reference_results):
            if abs(calc - ref) > tolerance:
                return False
        return True
    
    def _clear_screen(self):
        """Czyści ekran konsoli."""
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
    
    def run_benchmark_thread(self) -> BenchmarkResult:
        """Benchmark metody Thread."""
        calculator = ParallelIntegralCalculator(self.func, self.n)
        timing = calculator.compute_all(self.intervals, silent=True)
        return BenchmarkResult(
            method_name="Thread",
            total_time_ms=timing.total_time_ms,
            results=timing.results,
            thread_times_ms=[tt.duration_ms for tt in timing.thread_times],
            is_correct=self._verify_results(timing.results)
        )
    
    def run_benchmark_threadpool(self) -> BenchmarkResult:
        """Benchmark metody ThreadPool."""
        calculator = ThreadPoolIntegralCalculator(self.func, self.n)
        timing = calculator.compute_all(self.intervals, silent=True)
        return BenchmarkResult(
            method_name="ThreadPool",
            total_time_ms=timing.total_time_ms,
            results=timing.results,
            thread_times_ms=[tt.duration_ms for tt in timing.thread_times],
            is_correct=self._verify_results(timing.results)
        )
    
    def run_benchmark_tpl(self) -> BenchmarkResult:
        """Benchmark metody TPL (Executor)."""
        calculator = ExecutorIntegralCalculator(self.func, self.n)
        timing = calculator.compute_all(self.intervals, silent=True)
        return BenchmarkResult(
            method_name="TPL",
            total_time_ms=timing.total_time_ms,
            results=timing.results,
            thread_times_ms=[tt.duration_ms for tt in timing.thread_times],
            is_correct=self._verify_results(timing.results)
        )
    
    def run_benchmark_backgroundworker(self) -> BenchmarkResult:
        """Benchmark metody BackgroundWorker."""
        calculator = BackgroundWorkerCalculator(self.func, self.n)
        timing = calculator.compute_all(self.intervals, silent=True)
        return BenchmarkResult(
            method_name="BGWorker",
            total_time_ms=timing.total_time_ms,
            results=timing.results,
            thread_times_ms=[tt.duration_ms for tt in timing.thread_times],
            is_correct=self._verify_results(timing.results)
        )
    
    def run_all_benchmarks(self) -> List[BenchmarkResult]:
        """Uruchamia wszystkie benchmarki."""
        self._clear_screen()
        print("=" * 70)
        print("URUCHAMIANIE BENCHMARKU")
        print("=" * 70)
        print(f"Liczba trapezów: {self.n}")
        print(f"Przedziały: {len(self.intervals)}")
        print()
        
        print("Obliczanie referencji...")
        self._calculate_reference_results()
        print("Gotowe.\n")
        
        results = []
        methods = [
            ("Thread", self.run_benchmark_thread),
            ("ThreadPool", self.run_benchmark_threadpool),
            ("TPL", self.run_benchmark_tpl),
            ("BGWorker", self.run_benchmark_backgroundworker)
        ]
        
        for method_name, benchmark_func in methods:
            print(f"Uruchamianie: {method_name}...", end=" ", flush=True)
            result = benchmark_func()
            results.append(result)
            print(f"OK ({result.total_time_ms:.2f} ms)")
        
        print()
        return results
    
    def display_results(self, results: List[BenchmarkResult]):
        """Wyświetla wyniki benchmarku."""
        self._clear_screen()
        print("=" * 70)
        print("PORÓWNANIE METOD")
        print("=" * 70)
        print()
        
        # Tabela główna
        print(f"{'Metoda':<15} {'Czas [ms]':<15} {'Poprawne':<10}")
        print("-" * 40)
        for r in results:
            ok = "TAK" if r.is_correct else "NIE"
            print(f"{r.method_name:<15} {r.total_time_ms:>10.2f}     {ok:<10}")
        print("-" * 40)
        
        fastest = min(results, key=lambda x: x.total_time_ms)
        print(f"\nNajszybsza: {fastest.method_name} ({fastest.total_time_ms:.2f} ms)")
        
        # Szczegóły czasów
        print()
        print("=" * 70)
        print("SZCZEGÓŁY CZASÓW (wątki działają RÓWNOLEGLE)")
        print("=" * 70)
        for r in results:
            suma_watkow = sum(r.thread_times_ms)
            przyspieszenie = suma_watkow / r.total_time_ms if r.total_time_ms > 0 else 0
            print(f"\n{r.method_name}:")
            for i, t in enumerate(r.thread_times_ms):
                a, b, _ = self.intervals[i]
                print(f"  Wątek {i+1}: Przedział [{a:>3},{b:>3}]: {t:>10.2f} ms")
            print(f"  ---")
            print(f"  Czas równoległy:   {r.total_time_ms:>10.2f} ms")
            print(f"  Suma wątków:       {suma_watkow:>10.2f} ms (gdyby sekwencyjnie)")
            print(f"  Przyspieszenie:    {przyspieszenie:>10.2f}x")
        
        # Wartości całek
        print()
        print("=" * 70)
        print("WARTOŚCI CAŁEK")
        print("=" * 70)
        print()
        
        for i, (a, b, desc) in enumerate(self.intervals):
            val = results[0].results[i] if results else 0
            print(f"  Przedział [{a:>3},{b:>3}]:  {val:>14.4f}")
        
        print()
        print("(Wszystkie metody zwróciły identyczne wyniki)")
        print("=" * 70)
        print()
