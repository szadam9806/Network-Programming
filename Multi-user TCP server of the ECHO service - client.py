import socket


def start_client(server_host, server_port):
    """Uruchamia klienta TCP łączącego się z serwerem Echo."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_host, server_port))
        print(f"Połączono z {server_host}:{server_port}")

        while True:
            message = input("Wpisz wiadomość (lub 'exit' aby zakończyć): ")
            if message.lower() == "exit":
                break

            client.sendall(message.encode())
            response = client.recv(1024)
            print(f"[ECHO] Odpowiedź serwera: {response.decode()}")

    except ConnectionRefusedError:
        print("[ERROR] Nie można połączyć się z serwerem.")
    finally:
        client.close()
        print("Połączenie zamknięte.")


if __name__ == "__main__":
    SERVER_HOST = "127.0.0.1"  # Zmień na odpowiedni adres IP serwera
    SERVER_PORT = 7  # Ten sam port co w serwerze
    start_client(SERVER_HOST, SERVER_PORT)