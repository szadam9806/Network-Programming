import socket
import struct


def receive_multicast(multicast_group, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))

    group = socket.inet_aton(multicast_group)
    mreq = struct.pack("4sL", group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Oczekiwanie na multicast na {multicast_group}:{port}...")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Odebrano multicast od {addr}: {data.decode()}")


def receive_broadcast(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))

    print(f"Oczekiwanie na broadcast na porcie {port}...")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Odebrano broadcast od {addr}: {data.decode()}")


if __name__ == "__main__":
    mode = input("Wybierz tryb (multicast/broadcast): ").strip().lower()

    if mode == "multicast":
        multicast_group = input("Podaj adres grupy multicastowej (np. 224.0.0.1): ").strip()
        port = int(input("Podaj numer portu: ").strip())
        receive_multicast(multicast_group, port)
    elif mode == "broadcast":
        port = int(input("Podaj numer portu: ").strip())
        receive_broadcast(port)
    else:
        print("Niepoprawny tryb. Wybierz 'multicast' lub 'broadcast'.")
