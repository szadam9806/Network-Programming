import socket
import threading

# Konfiguracja serwera
HOST = "0.0.0.0"  # Nasłuchiwanie na wszystkich interfejsach
PORT = 7  # Domyślny port Echo
MAX_CONNECTIONS = 3  # Maksymalna liczba jednoczesnych klientów

# Lista aktywnych połączeń
active_connections = []
lock = threading.Lock()


def handle_client(client_socket, address):
    """Obsługa pojedynczego klienta."""
    with lock:
        if len(active_connections) >= MAX_CONNECTIONS:
            client_socket.sendall(b"Serwer zajety. Sprobuj ponownie pozniej.\n")
            client_socket.close()
            return
        active_connections.append(client_socket)

    print(f"[INFO] Połączono z {address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"[ECHO] {address} -> {data.decode().strip()}")
            client_socket.sendall(data)  # Odesłanie wiadomości do klienta
    except ConnectionResetError:
        print(f"[ERROR] Połączenie z {address} przerwane.")
    finally:
        with lock:
            active_connections.remove(client_socket)
        client_socket.close()
        print(f"[INFO] Rozłączono {address}")


def start_server():
    """Uruchamia serwer TCP."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNECTIONS)
    print(f"[INFO] Serwer nasłuchuje na {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
        print(f"[INFO] Aktywni klienci: {len(active_connections)}")


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n[INFO] Serwer zamykany...")