import threading
from time import sleep

def hello():
    print("Hello World!!")
thread = threading.Thread(target=hello)
thread.start()
sleep(5)
thread.join()
print("Wątek zakończony.")
