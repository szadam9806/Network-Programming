import socket

HOST = "0.0.0.0"
PORT = 7

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Serwer nasłuchuje na {HOST} na porcie {PORT}...")

try:
    while True:
        try:
            client_socket, client_addr = server_socket.accept()
            print(f"Połączono z {client_addr}")

            while True:
                data = client_socket.recv(1024)
                if not data:
                    print(f"Klient {client_addr[0]}:{client_addr[1]} zakończył połączenie.")
                    break
                print(f"Odebrano: {data.decode()}")
                client_socket.sendall(data)
        except ConnectionError as e:
            print(f"Błąd połączenia: {e}")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")
        client_socket.close()
except Exception as e:
    print(f"Błąd serwera: {e}")

server_socket.close()
print("Serwer zamknięty.")