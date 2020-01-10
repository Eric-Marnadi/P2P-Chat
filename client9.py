import socket, threading, pickle

class Node:
    def __init__(self, listen_port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_port = listen_port
        self.peers = {}
        self.super_node = 1
    def receive(self):
        self.server.bind(('127.0.0.1', self.listen_port))
        while(True):
            self.server.listen(5)
            conn, addr = self.server.accept()
            message = conn.recv(1024)
            if(message):
                message = pickle.loads(message)
                if(message['data'] == "peers"):
                    for i in message['peers']:
                        self.peers[i] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.peers[i].connect(('127.0.0.1', i))
                elif(message['recipient'] == self.listen_port):
                    if (len(self.peers) < 3 and message['sender'] not in self.peers):
                        self.peers[message['sender']] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.peers[message['sender']].connect(('127.0.0.1', message['sender']))
                    print()
                    print(message['data'])
                else:
                    self.send_message(message)
    def init_connect(self):
        self.client.connect(('127.0.0.1', self.super_node))
        message = {'data' : "join", 'sender': self.listen_port, 'recipient':1}
        self.client.send(pickle.dumps(message))
    def connect(self):
        v = input("")
        while(True):
            port = int(input("What port do you want to send a message to: "))
            data = input("To " + str(port) + ":")
            message = {'data': data, 'sender': self.listen_port, 'recipient': port, 'steps' : 3}
            self.send_message(message)
    def send_message(self, message):
        if(message['recipient'] in self.peers):
            print("Sending message to " + str(message['recipient']))
            self.peers[message['recipient']].send(pickle.dumps(message))
        else:
            for peer in self.peers:
                self.peers[peer].send(pickle.dumps(message))

if __name__ == "__main__":
    node = Node(9)
    node.init_connect()
    t1 = threading.Thread(target=node.receive, args=())
    t2 = threading.Thread(target=node.connect, args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()
