import threading
import time

lock = threading.Lock()

class SyncThread(threading.Thread):
    def __init__(self, thread_id):
        super().__init__()
        self.thread_id = thread_id

    def run(self):
        while True:
            with lock:  # Sekcja krytyczna
                for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    print(f"{letter}{self.thread_id}")
                    time.sleep(1)

# Tworzenie i uruchamianie wątków
threads = [SyncThread(i if i != 10 else 0) for i in range(1, 11)]
for t in threads:
    t.start()
