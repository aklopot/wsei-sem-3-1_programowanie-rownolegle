"""
Moduł do obliczania całek metodą BackgroundWorker.
Symulacja wzorca BackgroundWorker z C# używając threading.
"""

import threading
import time
import os
import sys
from dataclasses import dataclass
from typing import List, Callable, Tuple, Optional, Any
from queue import Queue


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


class BackgroundWorker:
    """Symulacja klasy BackgroundWorker z C#."""
    
    def __init__(self):
        """Inicjalizacja."""
        self._worker_thread: Optional[threading.Thread] = None
        self._cancel_event = threading.Event()
        self._is_busy = False
        self.on_do_work: Optional[Callable[[Any], Any]] = None
        self.on_progress_changed: Optional[Callable[[int, Any], None]] = None
        self.on_run_worker_completed: Optional[Callable[[Any, Optional[Exception]], None]] = None
        self._result = None
        self._error: Optional[Exception] = None
    
    @property
    def is_busy(self) -> bool:
        """Czy worker jest zajęty."""
        return self._is_busy
    
    @property
    def cancellation_pending(self) -> bool:
        """Czy żądano anulowania."""
        return self._cancel_event.is_set()
    
    def report_progress(self, percent: int, user_state: Any = None):
        """Raportuje postęp."""
        if self.on_progress_changed:
            self.on_progress_changed(percent, user_state)
    
    def run_worker_async(self, argument: Any = None):
        """Uruchamia pracę w tle."""
        if self._is_busy:
            raise RuntimeError("Worker jest zajęty")
        
        self._is_busy = True
        self._cancel_event.clear()
        self._result = None
        self._error = None
        
        def worker_thread_func():
            try:
                if self.on_do_work:
                    self._result = self.on_do_work(argument)
            except Exception as e:
                self._error = e
            finally:
                self._is_busy = False
                if self.on_run_worker_completed:
                    self.on_run_worker_completed(self._result, self._error)
        
        self._worker_thread = threading.Thread(target=worker_thread_func, daemon=True)
        self._worker_thread.start()
    
    def cancel_async(self):
        """Anuluje pracę."""
        self._cancel_event.set()
    
    def wait_for_completion(self, timeout: Optional[float] = None):
        """Czeka na zakończenie."""
        if self._worker_thread:
            self._worker_thread.join(timeout=timeout)


class BackgroundWorkerCalculator:
    """Kalkulator używający wzorca BackgroundWorker."""
    
    def __init__(self, func: Callable[[float], float], n: int):
        """Inicjalizacja kalkulatora."""
        self.func = func
        self.n = n
        self.progress_data = {}
        self.workers: List[BackgroundWorker] = []
        self.timing_data = {}
        self.results_queue = Queue()
        self.lock = threading.Lock()
    
    def _create_do_work_handler(self, interval_id: int, a: float, b: float, desc: str):
        """Tworzy handler do_work dla przedziału."""
        def do_work(worker: BackgroundWorker):
            start_time = time.time()
            dx = (b - a) / self.n
            total_area = 0.0
            
            for i in range(self.n):
                if worker.cancellation_pending:
                    return None
                
                x_start = a + i * dx
                x_end = x_start + dx
                f_left = self.func(x_start)
                f_right = self.func(x_end)
                area = (f_left + f_right) / 2 * dx
                total_area += area
                
                time.sleep(0.00001)
                
                if i % max(1, self.n // 50) == 0:
                    progress = int((i + 1) / self.n * 100)
                    worker.report_progress(progress, {'interval_id': interval_id})
            
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
        
        return do_work
    
    def _on_progress_changed(self, percent: int, user_state: Any):
        """Obsługuje aktualizację postępu."""
        if user_state and 'interval_id' in user_state:
            interval_id = user_state['interval_id']
            with self.lock:
                self.progress_data[interval_id]['progress'] = percent
    
    def _on_completed(self, result: Any, error: Optional[Exception]):
        """Obsługuje zakończenie pracy."""
        if error:
            self.results_queue.put({'error': str(error)})
        elif result:
            self.results_queue.put(result)
    
    def compute_all(self, intervals: List[Tuple[float, float, str]], silent: bool = False) -> TimingResult:
        """Oblicza całki dla wszystkich przedziałów."""
        if not silent:
            print("Uruchamianie BackgroundWorker...\n")
        
        overall_start = time.time()
        
        for idx, (a, b, desc) in enumerate(intervals):
            self.progress_data[idx] = {
                'description': desc,
                'progress': 0,
                'status': 'running'
            }
        
        self.workers = []
        for idx, (a, b, desc) in enumerate(intervals):
            worker = BackgroundWorker()
            do_work_handler = self._create_do_work_handler(idx, a, b, desc)
            worker.on_do_work = lambda arg, w=worker, h=do_work_handler: h(w)
            worker.on_progress_changed = self._on_progress_changed
            worker.on_run_worker_completed = self._on_completed
            self.workers.append(worker)
            worker.run_worker_async()
        
        if not silent:
            self._monitor_progress(len(intervals))
        
        for worker in self.workers:
            worker.wait_for_completion()
        
        overall_end = time.time()
        total_time_ms = (overall_end - overall_start) * 1000
        
        results = []
        while not self.results_queue.empty():
            results.append(self.results_queue.get())
        
        thread_timings = []
        result_values = []
        
        for res in sorted(results, key=lambda x: x.get('interval_id', 0)):
            if 'error' not in res:
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
    
    def _monitor_progress(self, num_workers: int):
        """Monitoruje postęp workerów."""
        while True:
            with self.lock:
                completed = sum(1 for w in self.workers if not w.is_busy)
                if completed >= num_workers:
                    break
            self._display_progress_bars()
            time.sleep(0.05)
    
    def _display_progress_bars(self):
        """Wyświetla paski postępu."""
        self._clear_screen()
        print("=" * 60)
        print("POSTĘP OBLICZEŃ (BGWorker)")
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
                print(f"[{bar}] {progress}% - {status}")
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
        print("WYNIKI (BGWorker)")
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
