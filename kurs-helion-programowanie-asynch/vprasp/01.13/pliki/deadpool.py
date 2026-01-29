import threading
import time
from random import uniform


class Philosopher(threading.Thread):
    def __init__(self, name, left_stick, right_stick):
        super().__init__(name=name)
        self.left_stick = left_stick
        self.right_stick = right_stick

    def run(self):
        print(f"Filozof {self.name} zaczął rozmyślać.")
        while True:
            time.sleep(uniform(1, 7))
            print(f"Filozof {self.name} skończył rozmyślać.")
            self.left_stick.acquire()
            time.sleep(uniform(1, 7))
            try:
                print(f"Filozof {self.name} zdobył lewy sztuciec.")
                self.right_stick.acquire()
                time.sleep(uniform(1, 7))
                try:
                    print(f"Filozof {self.name} je.")
                    time.sleep(uniform(1, 7))
                finally:
                    self.right_stick.release()
                    print(f"Filozof {self.name} opuścił prawy sztuciec.")
            finally:
                self.left_stick.release()
                print(f"Filozof {self.name} opuścił lewy sztuciec.")


stick1 = threading.RLock()
stick2 = threading.RLock()
stick3 = threading.RLock()
stick4 = threading.RLock()
stick5 = threading.RLock()

philosopher1 = Philosopher("Arystoteles", stick1, stick2)
philosopher2 = Philosopher("Platon", stick2, stick3)
philosopher3 = Philosopher("Sokrates", stick3, stick4)
philosopher4 = Philosopher("Kartezjusz", stick4, stick5)
philosopher5 = Philosopher("Karl Marks", stick5, stick1)

philosopher1.start()
philosopher2.start()
philosopher3.start()
philosopher4.start()
philosopher5.start()

philosopher1.join()
philosopher2.join()
philosopher3.join()
philosopher4.join()
philosopher5.join()
