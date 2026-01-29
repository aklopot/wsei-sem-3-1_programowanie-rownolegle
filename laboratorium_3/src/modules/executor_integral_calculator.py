import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class ExecutorIntegrationTask:
    
    def __init__(self, interval_id, a, b, n, func, cancel_event, progress_callback):
        self.interval_id = interval_id
        self.a = a
        self.b = b
        self.n = n
        self.func = func
        self.cancel_event = cancel_event
        self.progress_callback = progress_callback
    
    def execute(self):
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
        
        return {
            'interval_id': self.interval_id,
            'status': 'completed',
            'result': total_area,
            'progress': 100.0
        }


class ExecutorIntegralCalculator:
    
    def __init__(self, func, n):
        self.func = func
        self.n = n
        self.cancel_event = threading.Event()
        self.progress_data = {}
        self.lock = threading.Lock()
    
    def compute_all(self, intervals):
        print("Uruchamianie zadań przez ThreadPoolExecutor...\n")
        
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
                self.cancel_event, self._update_progress
            )
            tasks.append(task)
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(task.execute): task for task in tasks}
            
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
        
        end_time = time.time()
        total_time_ms = (end_time - start_time) * 1000
        
        time.sleep(0.1)
        self._display_summary(intervals, total_time_ms)
    
    def _update_progress(self, interval_id, progress):
        with self.lock:
            self.progress_data[interval_id]['progress'] = progress
    
    def _monitor_display(self, num_intervals):
        while True:
            with self.lock:
                completed = sum(1 for d in self.progress_data.values() if d['status'] == 'completed')
                if completed >= num_intervals:
                    break
            self._display_progress_bars()
            time.sleep(0.05)
    
    def _display_progress_bars(self):
        self._clear_screen()
        print("=" * 80)
        print("POSTĘP OBLICZEŃ (ThreadPoolExecutor)")
        print("=" * 80)
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
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
    
    def _display_summary(self, intervals, total_time_ms):
        self._clear_screen()
        print("=" * 80)
        print("WYNIKI OBLICZEŃ (ThreadPoolExecutor)")
        print("=" * 80)
        print()
        
        print(f"{'Przedział':<20} {'Opis':<20} {'Wartość całki':<20} {'Status':<15}")
        print("-" * 80)
        
        for idx, (a, b, desc) in enumerate(intervals):
            data = self.progress_data[idx]
            status = data['status']
            
            if status == 'completed':
                result = data['result']
                print(f"[{a:>5}, {b:>5}]     {desc:<20} {result:>18.6f}  {status}")
            else:
                print(f"[{a:>5}, {b:>5}]     {desc:<20} {'N/A':>18} {status}")
        
        print("-" * 80)
        print(f"\nCałkowity czas obliczeń: {total_time_ms:.2f} milisekund")
        print("=" * 80)
        print()

