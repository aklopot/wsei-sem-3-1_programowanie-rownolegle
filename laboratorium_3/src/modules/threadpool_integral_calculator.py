"""
Moduł do obliczania całek metodą multiprocessing.pool.ThreadPool.
Odpowiednik klasy ThreadPool z C#.
"""

import time
import os
import sys
from multiprocessing.pool import ThreadPool
from dataclasses import dataclass
from typing import List, Callable, Tuple, Optional


@dataclass
class ThreadTiming:
    """Dane czasowe dla pojedynczego wątku."""
    interval_id: int
    interval_desc: str
    start_time: float
    end_time: float
    duration_ms: float
    result: Optional[float] = None


@dataclass
class TimingResult:
    """Wyniki czasowe obliczeń."""
    total_time_ms: float
    thread_times: List[ThreadTiming]
    results: List[float]


class ThreadPoolIntegralCalculator:
    """Kalkulator używający ThreadPool do obliczeń równoległych."""
    
    def __init__(self, func: Callable[[float], float], n: int, num_workers: int = 3):
        """Inicjalizacja kalkulatora."""
        self.func = func
        self.n = n
        self.num_workers = num_workers
        self.progress_data = {}
    
    def _calculate_integral_trapezoids(self, args: Tuple[int, float, float, str]) -> dict:
        """Oblicza całkę metodą trapezów dla jednego przedziału."""
        interval_id, a, b, desc = args
        start_time = time.time()
        
        dx = (b - a) / self.n
        total_area = 0.0
        
        for i in range(self.n):
            x_start = a + i * dx
            x_end = x_start + dx
            f_left = self.func(x_start)
            f_right = self.func(x_end)
            area = (f_left + f_right) / 2 * dx
            total_area += area
            
            if i % max(1, self.n // 50) == 0:
                time.sleep(0.00001)
        
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000
        
        return {
            'interval_id': interval_id,
            'description': desc,
            'a': a,
            'b': b,
            'result': total_area,
            'start_time': start_time,
            'end_time': end_time,
            'duration_ms': duration_ms
        }
    
    def compute_all(self, intervals: List[Tuple[float, float, str]], silent: bool = False) -> TimingResult:
        """Oblicza całki dla wszystkich przedziałów."""
        if not silent:
            print("Uruchamianie ThreadPool...\n")
        
        overall_start = time.time()
        
        args_list = [(idx, a, b, desc) for idx, (a, b, desc) in enumerate(intervals)]
        
        with ThreadPool(processes=self.num_workers) as pool:
            results = pool.map(self._calculate_integral_trapezoids, args_list)
        
        overall_end = time.time()
        total_time_ms = (overall_end - overall_start) * 1000
        
        thread_timings = []
        result_values = []
        
        for res in sorted(results, key=lambda x: x['interval_id']):
            thread_timings.append(ThreadTiming(
                interval_id=res['interval_id'],
                interval_desc=res['description'],
                start_time=res['start_time'],
                end_time=res['end_time'],
                duration_ms=res['duration_ms'],
                result=res['result']
            ))
            result_values.append(res['result'])
        
        timing_result = TimingResult(
            total_time_ms=total_time_ms,
            thread_times=thread_timings,
            results=result_values
        )
        
        if not silent:
            self._display_summary(intervals, timing_result)
        
        return timing_result
    
    def _clear_screen(self):
        """Czyści ekran."""
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
    
    def _display_summary(self, intervals: List[Tuple[float, float, str]], timing: TimingResult):
        """Wyświetla podsumowanie wyników."""
        self._clear_screen()
        print("=" * 60)
        print("WYNIKI (ThreadPool)")
        print("=" * 60)
        print()
        
        print(f"{'Przedział':<15} {'Wartość':<18} {'Czas':<12}")
        print("-" * 50)
        
        for tt in timing.thread_times:
            idx = tt.interval_id
            a, b, desc = intervals[idx]
            print(f"[{a:>3},{b:>3}]       {tt.result:>14.6f}   {tt.duration_ms:>8.2f} ms")
        
        print("-" * 50)
        print(f"\nCzas całkowity: {timing.total_time_ms:.2f} ms")
        print("=" * 60)
        print()
