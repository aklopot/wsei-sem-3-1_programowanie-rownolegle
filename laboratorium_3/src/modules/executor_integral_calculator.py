"""
Moduł do obliczania całek metodą ThreadPoolExecutor.
Odpowiednik TPL (Task Parallel Library) z C#.
"""

import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
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


class ExecutorIntegrationTask:
    """Zadanie dla ThreadPoolExecutor."""
    
    def __init__(self, interval_id: int, a: float, b: float, n: int,
                 func: Callable[[float], float], cancel_event: threading.Event,
                 progress_callback: Callable[[int, float], None], desc: str = ""):
        self.interval_id = interval_id
        self.a = a
        self.b = b
        self.n = n
        self.func = func
        self.cancel_event = cancel_event
        self.progress_callback = progress_callback
        self.desc = desc
    
    def execute(self) -> dict:
        """Wykonuje obliczenia całki."""
        start_time = time.time()
        dx = (self.b - self.a) / self.n
        total_area = 0.0
        
        for i in range(self.n):
            if self.cancel_event.is_set():
                return {
                    'interval_id': self.interval_id,
                    'status': 'cancelled',
                    'progress': i / self.n * 100
                }
            
            x_start = self.a + i * dx
            x_end = x_start + dx
            f_left = self.func(x_start)
            f_right = self.func(x_end)
            area = (f_left + f_right) / 2 * dx
            total_area += area
            
            time.sleep(0.00001)
            
            if i % max(1, self.n // 50) == 0:
                progress = (i + 1) / self.n * 100
                self.progress_callback(self.interval_id, progress)
        
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000
        
        return {
            'interval_id': self.interval_id,
            'status': 'completed',
            'result': total_area,
            'progress': 100.0,
            'start_time': start_time,
            'end_time': end_time,
            'duration_ms': duration_ms,
            'description': self.desc
        }


class ExecutorIntegralCalculator:
    """Kalkulator używający ThreadPoolExecutor (TPL) do obliczeń równoległych."""
    
    def __init__(self, func: Callable[[float], float], n: int):
        """Inicjalizacja kalkulatora."""
        self.func = func
        self.n = n
        self.cancel_event = threading.Event()
        self.progress_data = {}
        self.lock = threading.Lock()
    
    def compute_all(self, intervals: List[Tuple[float, float, str]], silent: bool = False) -> TimingResult:
        """Oblicza całki dla wszystkich przedziałów."""
        if not silent:
            print("Uruchamianie TPL (Executor)...\n")
        
        start_time = time.time()
        
        for idx, (a, b, desc) in enumerate(intervals):
            self.progress_data[idx] = {
                'description': desc,
                'progress': 0.0,
                'status': 'running'
            }
        
        tasks = []
        for idx, (a, b, desc) in enumerate(intervals):
            task = ExecutorIntegrationTask(
                idx, a, b, self.n, self.func,
                self.cancel_event, self._update_progress, desc
            )
            tasks.append(task)
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(task.execute): task for task in tasks}
            
            if not silent:
                monitor_thread = threading.Thread(
                    target=self._monitor_display,
                    args=(len(intervals),),
                    daemon=True
                )
                monitor_thread.start()
            
            for future in as_completed(futures):
                result = future.result()
                interval_id = result['interval_id']
                
                with self.lock:
                    self.progress_data[interval_id]['status'] = result['status']
                    self.progress_data[interval_id]['progress'] = result['progress']
                    if 'result' in result:
                        self.progress_data[interval_id]['result'] = result['result']
                    if 'start_time' in result:
                        self.progress_data[interval_id]['start_time'] = result['start_time']
                        self.progress_data[interval_id]['end_time'] = result['end_time']
                        self.progress_data[interval_id]['duration_ms'] = result['duration_ms']
        
        end_time = time.time()
        total_time_ms = (end_time - start_time) * 1000
        
        thread_timings = []
        result_values = []
        
        for idx in sorted(self.progress_data.keys()):
            data = self.progress_data[idx]
            if data['status'] == 'completed':
                thread_timings.append(ThreadTiming(
                    interval_id=idx,
                    interval_desc=data['description'],
                    start_time=data.get('start_time', 0),
                    end_time=data.get('end_time', 0),
                    duration_ms=data.get('duration_ms', 0),
                    result=data['result']
                ))
                result_values.append(data['result'])
        
        timing_result = TimingResult(
            total_time_ms=total_time_ms,
            thread_times=thread_timings,
            results=result_values
        )
        
        if not silent:
            time.sleep(0.1)
            self._display_summary(intervals, timing_result)
        
        return timing_result
    
    def _update_progress(self, interval_id: int, progress: float):
        """Aktualizuje postęp dla danego przedziału."""
        with self.lock:
            self.progress_data[interval_id]['progress'] = progress
    
    def _monitor_display(self, num_intervals: int):
        """Monitoruje i wyświetla postęp."""
        while True:
            with self.lock:
                completed = sum(1 for d in self.progress_data.values() if d['status'] == 'completed')
                if completed >= num_intervals:
                    break
            self._display_progress_bars()
            time.sleep(0.05)
    
    def _display_progress_bars(self):
        """Wyświetla paski postępu."""
        self._clear_screen()
        print("=" * 60)
        print("POSTĘP OBLICZEŃ (TPL)")
        print("=" * 60)
        print()
        
        with self.lock:
            for idx in sorted(self.progress_data.keys()):
                data = self.progress_data[idx]
                desc = data['description']
                progress = data['progress']
                status = data['status']
                
                bar_length = 20
                filled = int(bar_length * progress / 100)
                bar = '*' * filled + ' ' * (bar_length - filled)
                
                print(f"Przedział {idx + 1}: {desc}")
                print(f"[{bar}] {progress:.1f}% - {status}")
                print()
    
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
        print("WYNIKI (TPL)")
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
