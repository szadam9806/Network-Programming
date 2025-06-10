import socket

try:
    HOST = input("Podaj adres serwera: ") or "127.0.0.1"
    PORT = int(input("Podaj port serwera: ") or 7)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Połączono z {HOST} na porcie {PORT}")

    while True:
        msg = input("Wpisz wiadomość (lub 'exit' aby zakończyć): ")
        if msg.lower() == "exit":
            break

        try:
            client_socket.sendall(msg.encode())
            data = client_socket.recv(1024)
            print(f"Odpowiedź serwera: {data.decode()}")
        except ConnectionResetError:
            print("Połączenie zostało zerwane przez serwer.")
            break
        except BrokenPipeError:
            print("Serwer zakończył połączenie.")
            break
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")
            break
except ValueError:
    print("Błąd: Nieprawidłowy numer portu.")
except socket.gaierror:
    print("Błąd: Nie można przetworzyć adresu hosta.")

client_socket.close()