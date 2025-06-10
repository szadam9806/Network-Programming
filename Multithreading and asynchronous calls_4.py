import asyncio

async def print_letters(thread_id):
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print(f"{letter}{thread_id}")
        await asyncio.sleep(1)  # Asynchroniczne opóźnienie

async def main():
    tasks = {i: asyncio.create_task(print_letters(i if i != 10 else 0)) for i in range(1, 11)}

    # Symulacja użytkownika usuwającego zadanie
    await asyncio.sleep(5)  # Po 5 sekundach usuwamy zadanie nr 1
    tasks[1].cancel()

    await asyncio.sleep(10)  # Po 10 sekundach kończymy wszystko

# Uruchomienie asynchronicznej pętli
asyncio.run(main())
