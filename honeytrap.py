import socket

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen()

    def accept(self):
        return self.sock.accept()

C = TCPServer('localhost', 8080)
C.bind()
C.listen()
while True:
    conn, addr = C.accept()
    data = conn.recv(1024)
    decode_data = data.decode()
    print(f"Received data: {data}")
    print(f"Connection from {addr}")
