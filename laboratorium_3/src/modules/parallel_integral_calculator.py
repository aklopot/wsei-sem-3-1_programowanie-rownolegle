"""
Moduł do obliczania całek metodą threading.Thread.
Odpowiednik klasy Thread z C#.
"""

import threading
import queue
import time
import os
import sys
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


class IntegrationWorker(threading.Thread):
    """Wątek roboczy obliczający całkę dla jednego przedziału."""
    
    def __init__(self, interval_id: int, a: float, b: float, n: int, 
                 func: Callable[[float], float], result_queue: queue.Queue, 
                 desc: str = ""):
        super().__init__(daemon=False)
        self.interval_id = interval_id
        self.a = a
        self.b = b
        self.n = n
        self.func = func
        self.result_queue = result_queue
        self.cancel_event = threading.Event()
        self.desc = desc
    
    def run(self):
        """Wykonuje obliczenia całki."""
        try:
            start_time = time.time()
            dx = (self.b - self.a) / self.n
            total_area = 0.0
            
            for i in range(self.n):
                if self.cancel_event.is_set():
                    self.result_queue.put({
                        'interval_id': self.interval_id,
                        'status': 'cancelled',
                        'progress': i / self.n * 100
                    })
                    return
                
                x_start = self.a + i * dx
                x_end = x_start + dx
                f_left = self.func(x_start)
                f_right = self.func(x_end)
                area = (f_left + f_right) / 2 * dx
                total_area += area
                
                time.sleep(0.00001)
                
                if i % max(1, self.n // 50) == 0:
                    progress = (i + 1) / self.n * 100
                    self.result_queue.put({
                        'interval_id': self.interval_id,
                        'status': 'progress',
                        'progress': progress
                    })
            
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            
            self.result_queue.put({
                'interval_id': self.interval_id,
                'status': 'completed',
                'result': total_area,
                'progress': 100.0,
                'start_time': start_time,
                'end_time': end_time,
                'duration_ms': duration_ms,
                'description': self.desc
            })
        
        except Exception as e:
            self.result_queue.put({
                'interval_id': self.interval_id,
                'status': 'error',
                'error': str(e)
            })
    
    def cancel(self):
        """Anuluje obliczenia."""
        self.cancel_event.set()


class ParallelIntegralCalculator:
    """Kalkulator używający threading.Thread do obliczeń równoległych."""
    
    def __init__(self, func: Callable[[float], float], n: int):
        """Inicjalizacja kalkulatora."""
        self.func = func
        self.n = n
        self.result_queue = queue.Queue()
        self.workers = {}
        self.progress_data = {}
    
    def compute_all(self, intervals: List[Tuple[float, float, str]], silent: bool = False) -> TimingResult:
        """Oblicza całki dla wszystkich przedziałów."""
        if not silent:
            print("Uruchamianie wątków...\n")
        
        start_time = time.time()
        
        for idx, (a, b, desc) in enumerate(intervals):
            self.progress_data[idx] = {
                'description': desc,
                'progress': 0.0,
                'status': 'running'
            }
            worker = IntegrationWorker(idx, a, b, self.n, self.func, self.result_queue, desc)
            self.workers[idx] = worker
            worker.start()
        
        self._monitor_progress(len(intervals), silent)
        
        for worker in self.workers.values():
            worker.join()
        
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
            self._display_summary(intervals, timing_result)
        
        return timing_result
    
    def _monitor_progress(self, num_workers: int, silent: bool = False):
        """Monitoruje postęp wątków."""
        completed_count = 0
        
        while completed_count < num_workers:
            try:
                msg = self.result_queue.get(timeout=1)
            except queue.Empty:
                continue
            
            interval_id = msg['interval_id']
            status = msg['status']
            
            if status == 'progress':
                self.progress_data[interval_id]['progress'] = msg['progress']
            elif status == 'completed':
                self.progress_data[interval_id]['status'] = 'completed'
                self.progress_data[interval_id]['result'] = msg['result']
                self.progress_data[interval_id]['progress'] = 100.0
                self.progress_data[interval_id]['start_time'] = msg.get('start_time')
                self.progress_data[interval_id]['end_time'] = msg.get('end_time')
                self.progress_data[interval_id]['duration_ms'] = msg.get('duration_ms')
                completed_count += 1
            elif status == 'error':
                self.progress_data[interval_id]['status'] = 'error'
                self.progress_data[interval_id]['error'] = msg['error']
                completed_count += 1
            elif status == 'cancelled':
                self.progress_data[interval_id]['status'] = 'cancelled'
                completed_count += 1
            
            if not silent:
                self._display_progress_bars()
    
    def _display_progress_bars(self):
        """Wyświetla paski postępu."""
        self._clear_screen()
        print("=" * 60)
        print("POSTĘP OBLICZEŃ (Thread)")
        print("=" * 60)
        print()
        
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
        print("WYNIKI (Thread)")
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
