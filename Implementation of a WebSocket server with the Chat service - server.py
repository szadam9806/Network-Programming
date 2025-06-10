#https://quickstarts.postman.com/guide/websockets-python/index.html?index=..%2F..index#1
import asyncio
import websockets

connected_clients = {}
chat_history = []

def log_message(message):
    with open("server_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")

async def chat_handler(websocket):
    try:
        nickname = await websocket.recv()
        client_ip = websocket.remote_address[0]
        connected_clients[websocket] = (nickname, client_ip)
        join_message = f"{nickname} ({client_ip}) dołączył do czatu."
        print(join_message)
        log_message(join_message)
        await send_chat_history(websocket)
        await broadcast(f"{nickname} dołączył do czatu!")
        await send_user_list()

        async for message in websocket:
            full_message = f"{nickname}: {message}"
            print(full_message)
            chat_history.append(full_message)
            log_message(full_message)
            await broadcast(full_message)

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if websocket in connected_clients:
            nickname = connected_clients.pop(websocket)[0]
            leave_message = f"{nickname} opuścił czat."
            print(leave_message)
            chat_history.append(leave_message)
            log_message(leave_message)
            await broadcast(f"{nickname} opuścił czat.")
            await send_user_list()

async def send_chat_history(websocket):
    for message in chat_history:
        await websocket.send(f"HISTORIA:{message}")

async def broadcast(message):
    if connected_clients:
        log_message(f"[Broadcast] {message}")
        await asyncio.gather(*[client.send(message) for client in connected_clients])

async def send_user_list():
    user_list = "LISTA_UZYTKOWNIKOW:" + ",".join(nick for nick, _ in connected_clients.values())
    await asyncio.gather(*[client.send(user_list) for client in connected_clients])

async def main():
    async with websockets.serve(chat_handler, "localhost", 8765):
        print("Serwer WebSocket działa na ws://localhost:8765")
        log_message("=== Serwer uruchomiony ===")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
