import socket, pickle, random

class SuperNode:
    def __init__(self, listen_port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_port = listen_port
        self.peers = []
    def receive(self):
        self.server.bind(('127.0.0.1', self.listen_port))
        while(True):
            self.server.listen(10)
            conn, addr = self.server.accept()
            message = conn.recv(1024)
            if(message):
                message = pickle.loads(message)
                if(message['data'] == "join"):
                    self.peers.append(message['sender'])
                    self.send_peers(message['sender'])
                elif(message['recipient'] == self.listen_port):
                    print()
                    print(message['data'])
                else:
                    self.send_message(message)
    def send_peers(self, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', port))
        peers = []
        if(len(self.peers) > 2):
            for i in range(3):
                peer = random.choice(self.peers)
                if(peer != port):
                    peers.append(peer)
        message = {'data' : 'peers', 'peers' : peers, 'recipient' : port}
        client.send(pickle.dumps(message))
        client.close()
    def send_message(self, message):
        print("Sending message to " + str(message['recipient']))
        if (message['recipient'] in self.peers):
            self.peers[message['recipient']].send(pickle.dumps(message))
            print("sent directly")
        else:
            for peer in self.peers:
                self.peers[peer].send(pickle.dumps(message))


if __name__ == "__main__":
    node = SuperNode(1)
    node.receive()
