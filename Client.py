import socket
import sys
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import time


def ShowWin():
    global st, win, text
    win = tk.Tk()
    win.config(width=800, height=600)
    win.title("Client")
    win.resizable(False,False)
    st = scrolledtext.ScrolledText(win, width=100)
    st.config(state=tk.DISABLED)
    text = tk.Text(win, width=50, height=1)


class Client:
    def __init__(self):
        self.NameList = None
        self.data = None
        self.on = True
        self.client_socket = None
        self.username = None
        self.port = None
        self.host = None
        self.datasend = None
        self.client_program()

    def client_program(self):
        self.host = input("Host Address: ")
        self.port = int(input("Port: "))
        self.username = input("Username: ")
        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))
        snd = Thread(target=self.Send)
        rcv = Thread(target=self.Receive)
        snd.start()
        rcv.start()
        ShowWin()
        st.pack()
        text.pack()
        win.mainloop()

    def Send(self):
        Incorrect = False
        self.NameList = self.client_socket.recv(1024)
        print(self.NameList.decode())
        if self.username in self.NameList.decode().split() and self.NameList.decode() != "Empty":
            Incorrect = True
        while Incorrect:
            print("Incorrect Data Provided, Try again...")
            self.username = input("Username: ")
            if self.username not in self.NameList.decode().split():
                break
        time.sleep(2)
        self.client_socket.send(self.username.encode())
        while self.on:
            time.sleep(0.1)  # IMPORTANT: to not make tk freeze and crash
            self.datasend = text.get(1.0, "end")
            if "\n\n" in self.datasend and True in [char.isprintable() for char in self.datasend]:
                text.delete(1.0, "end")
                print((self.username+": "+''.join(self.datasend.splitlines())).encode())
                self.client_socket.send((self.username+": "+''.join(self.datasend.splitlines())).encode())
                if ''.join(self.datasend.splitlines()) == "/stop":
                    self.on = False
                    win.destroy()
                    quit()
                    break
        sys.exit()

    def Receive(self):
        while self.on:
            self.data = self.client_socket.recv(1024)
            ShowText(self.data.decode())
            if not self.data:
                pass


def ShowText(s):
    st.see('end')
    st.config(state=tk.NORMAL)
    st.insert(tk.END, s + "\n")
    st.config(state=tk.DISABLED)
    st.pack()


if __name__ == '__main__':
    Client()
