#https://quickstarts.postman.com/guide/websockets-python/index.html?index=..%2F..index#1
import asyncio
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
import websockets

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("WebSocket Chat - Klient")
        window_width = 500
        window_height = 350
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.master.minsize(450, 300)

        # Nick
        self.nickname = simpledialog.askstring("Nickname", "Podaj swój nick:")
        if not self.nickname:
            messagebox.showerror("Błąd", "Musisz podać nick!")
            self.master.destroy()
            return

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=3)
        self.master.grid_columnconfigure(1, weight=1)

        self.chat_frame = tk.Frame(self.master)
        self.chat_frame.grid(row=0, column=0, sticky="nsew")

        # Lista aktywnych
        self.users_frame = tk.Frame(self.master)
        self.users_frame.grid(row=0, column=1, sticky="nsew")

        # Okno czatu
        self.chat_area = tk.Text(self.chat_frame, state='disabled', wrap='word', height=12)
        self.chat_area.pack(padx=5, pady=5, fill='both', expand=True)

        # wyrównaie prawo lewo
        self.chat_area.tag_configure("left", justify='left')
        self.chat_area.tag_configure("right", justify='right')

        # Wysyłka
        self.entry_frame = tk.Frame(self.chat_frame)
        self.entry_frame.pack(fill='x', padx=5, pady=5)

        self.msg_entry = tk.Entry(self.entry_frame)
        self.msg_entry.pack(side='left', fill='x', expand=True)
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.entry_frame, text="Wyślij", command=self.send_message, width=8)
        self.send_button.pack(side='right', padx=(5, 0))

        # Nagłówek aktywnych
        self.user_list_label = tk.Label(self.users_frame, text="Użytkownicy online:", font=('Arial', 9, 'bold'))
        self.user_list_label.pack(pady=(5, 0), padx=5)

        self.user_list_box = tk.Listbox(self.users_frame)
        self.user_list_box.pack(padx=5, pady=5, fill='both', expand=True)

        # Zamknięcie
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Połączenie WebSocket
        self.ws = None
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_async_loop, daemon=True).start()

    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.run_client())

    async def run_client(self):
        try:
            self.ws = await websockets.connect('ws://localhost:8765')
            await self.ws.send(self.nickname)
            await self.receive_messages()
        except Exception as e:
            self.show_message(f"Błąd połączenia: {e}", "left")
            messagebox.showerror("Błąd", f"Nie udało się połączyć z serwerem.\n{e}")
            self.master.quit()

    async def receive_messages(self):
        try:
            async for message in self.ws:
                if message.startswith("LISTA_UZYTKOWNIKOW:"):
                    users = message.split(":", 1)[1].split(",")
                    self.update_user_list(users)
                elif message.startswith("HISTORIA:"):
                    history_message = message.split(":", 1)[1]
                    sender = history_message.split(":", 1)[0]
                    align = "right" if sender == self.nickname else "left"
                    self.show_message(history_message, align)
                else:
                    sender = message.split(":", 1)[0]
                    align = "right" if sender == self.nickname else "left"
                    self.show_message(message, align)
        except websockets.exceptions.ConnectionClosed:
            self.show_message("Połączenie z serwerem zostało zamknięte.", "left")

    def send_message(self, event=None):
        message = self.msg_entry.get()
        if message and self.ws:
            asyncio.run_coroutine_threadsafe(self.ws.send(message), self.loop)
            self.msg_entry.delete(0, tk.END)

    def show_message(self, message, alignment):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n", alignment)
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

    def update_user_list(self, users):
        self.user_list_box.delete(0, tk.END)
        for user in users:
            self.user_list_box.insert(tk.END, user)

    def on_close(self):
        if self.ws:
            asyncio.run_coroutine_threadsafe(self.ws.close(), self.loop)
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
