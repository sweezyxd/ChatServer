import socket
import time
from threading import Thread

server = socket.socket()
host = '192.168.11.110'
port = 8080
try:
    server.bind((host, port))
except socket.error as e:
    print(str(e))
print('Server is listening...')
server.listen(5)
userarr, namearr = [], []


class Clnt:
    def __init__(self, client, name, obj):
        self.rcv = None
        self.obj = obj
        self.data = None
        self.on = True
        self.client = client
        self.name = name
        self.main()
        
    def main(self):
        if self.on:
            self.rcv = Thread(target=self.receive)
            self.rcv.start()

    def send(self, text):
        try:
            self.client.send(text)
        except ConnectionResetError:
            sendtoall(self.end())

    def end(self):
        namearr.remove(self.name)
        userarr.remove(globals()[self.obj])
        self.on = False
        del globals()[self.obj]
        print("User disconnected: " + self.name)
        return (str(self.name) + " has disconnected.").encode()

    def receive(self):
        try:
            while self.on:
                data = self.client.recv(1024)
                command = data.decode().replace(self.name+": ","",1)
                print(len(data.decode()) - len(self.name) - 2)
                if len(data.decode()) - len(self.name) - 2 <= 0:
                    data = self.end()
                if command == '/help':
                    self.client.send(b"List of commands:\n")
                    self.client.send(b"/stop   -> Stops the connection\n/list  -> Shows current users connected\n")
                    data = b''
                if command == '/stop':
                    data = self.end()
                if command == '/list':
                    self.client.send(b"Users connected list:\n")
                    for name in namearr:
                        data = b''
                        self.client.send((name + "\n").encode())
                sendtoall(data)
        except ConnectionResetError:
            sendtoall(self.end())


def main():
    users = 0
    while True:
        Client, address = server.accept()
        users += 1
        time.sleep(1)
        if len(userarr) > 0:
            Client.send(' '.join(namearr).encode())
        if len(userarr) == 0:
            Client.send('Empty'.encode())
        globals()["Clnt" + str(users)] = Clnt(Client, Client.recv(1024).decode(), "Clnt" + str(users))
        userarr.append(globals()["Clnt" + str(users)])
        namearr.append(str(globals()["Clnt" + str(users)].name))
        sendtoall((str(globals()["Clnt" + str(users)].name) + " has connected.").encode())
        print("User connected: " + globals()["Clnt" + str(users)].name)
        time.sleep(1)


def sendtoall(s):
    for user in userarr:
        user.send(s)


start = Thread(target=main)
if __name__ == '__main__':
    main()
