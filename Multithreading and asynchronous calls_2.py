import threading
import time

class CustomThread(threading.Thread):
    def __init__(self, thread_id):
        super().__init__()
        self.thread_id = thread_id
        self.running = threading.Event()
        self.running.clear()  # Na start wątek jest wstrzymany

    def run(self):
        while True:
            self.running.wait()  # Wątek czeka na sygnał do startu
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                print(f"{letter}{self.thread_id}")
                time.sleep(1)  # Częstotliwość raz na sekundę

# Tworzenie 10 wątków
threads = [CustomThread(i if i != 10 else 0) for i in range(1, 11)]
for t in threads:
    t.start()

# Funkcja sterująca
def control_thread(command, thread_id):
    if command == "start":
        threads[thread_id].running.set()  # Wznawianie wątku
    elif command == "stop":
        threads[thread_id].running.clear()  # Wstrzymywanie wątku

# Przykładowe sterowanie
control_thread("start", 0)  # Uruchomienie wątku nr 0
time.sleep(5)
control_thread("stop", 0)  # Zatrzymanie wątku nr 0
