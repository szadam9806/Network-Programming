import socket
import struct


def send_multicast(message, multicast_group, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)  # Ustawienie TTL
    sock.sendto(message.encode(), (multicast_group, port))
    print(f"Wysłano multicast: {message} do {multicast_group}:{port}")


def send_broadcast(message, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Włączenie broadcastu
    sock.sendto(message.encode(), ("255.255.255.255", port))
    print(f"Wysłano broadcast: {message} na port {port}")


if __name__ == "__main__":
    mode = input("Wybierz tryb (multicast/broadcast): ").strip().lower()
    message = input("Podaj wiadomość do wysłania: ").strip()

    if mode == "multicast":
        multicast_group = input("Podaj adres grupy multicastowej (np. 224.0.0.1): ").strip()
        port = int(input("Podaj numer portu: ").strip())
        send_multicast(message, multicast_group, port)
    elif mode == "broadcast":
        port = int(input("Podaj numer portu: ").strip())
        send_broadcast(message, port)
    else:
        print("Niepoprawny tryb. Wybierz 'multicast' lub 'broadcast'.")
