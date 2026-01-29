import threading
import queue
import time
import os
import sys


class IntegrationWorker(threading.Thread):
    
    def __init__(self, interval_id, a, b, n, func, result_queue):
        super().__init__(daemon=False)
        self.interval_id = interval_id
        self.a = a
        self.b = b
        self.n = n
        self.func = func
        self.result_queue = result_queue
        self.cancel_event = threading.Event()
    
    def run(self):
        try:
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
            
            self.result_queue.put({
                'interval_id': self.interval_id,
                'status': 'completed',
                'result': total_area,
                'progress': 100.0
            })
        
        except Exception as e:
            self.result_queue.put({
                'interval_id': self.interval_id,
                'status': 'error',
                'error': str(e)
            })
    
    def cancel(self):
        self.cancel_event.set()


class ParallelIntegralCalculator:
    
    def __init__(self, func, n):
        self.func = func
        self.n = n
        self.result_queue = queue.Queue()
        self.workers = {}
        self.progress_data = {}
    
    def compute_all(self, intervals):
        print("Uruchamianie wątków dla każdego przedziału...\n")
        
        start_time = time.time()
        
        for idx, (a, b, desc) in enumerate(intervals):
            self.progress_data[idx] = {
                'description': desc,
                'progress': 0.0,
                'status': 'running'
            }
            
            worker = IntegrationWorker(idx, a, b, self.n, self.func, self.result_queue)
            self.workers[idx] = worker
            worker.start()
        
        self._monitor_progress(len(intervals))
        
        for worker in self.workers.values():
            worker.join()
        
        end_time = time.time()
        total_time_ms = (end_time - start_time) * 1000
        
        self._display_summary(intervals, total_time_ms)
    
    def _monitor_progress(self, num_workers):
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
                completed_count += 1
            elif status == 'error':
                self.progress_data[interval_id]['status'] = 'error'
                self.progress_data[interval_id]['error'] = msg['error']
                completed_count += 1
            elif status == 'cancelled':
                self.progress_data[interval_id]['status'] = 'cancelled'
                completed_count += 1
            
            self._display_progress_bars()
    
    def _display_progress_bars(self):
        self._clear_screen()
        print("=" * 80)
        print("POSTĘP OBLICZEŃ")
        print("=" * 80)
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
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
    
    def _display_summary(self, intervals, total_time_ms):
        self._clear_screen()
        print("=" * 80)
        print("WYNIKI OBLICZEŃ")
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
            elif status == 'error':
                error = data['error']
                print(f"[{a:>5}, {b:>5}]     {desc:<20} {'N/A':>18} {status}: {error}")
            else:
                print(f"[{a:>5}, {b:>5}]     {desc:<20} {'N/A':>18} {status}")
        
        print("-" * 80)
        print(f"\nCałkowity czas obliczeń: {total_time_ms:.2f} milisekund")
        print("=" * 80)
        print()

