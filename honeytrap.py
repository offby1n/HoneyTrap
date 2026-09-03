import socket
from time import strftime
import threading

class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def bind(self):
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen()

    def accept(self):
        return self.sock.accept()

def save(data):
    try:
        with open("honeytrap.log", "r") as f:
            lines = f.readlines()
            if len(lines) >= 10:
                lines = lines[1:]  
    except FileNotFoundError:
        lines = []
    with open("honeytrap.log", "w") as f:
        f.writelines(lines)
        f.write(f"{strftime('%Y-%m-%d %H:%M:%S')} - {data}\n")

def handle_connection(conn, addr):
    banner = "SSH-2.0-OpenSSH_9.6\n"
    conn.sendall(banner.encode())
    data = conn.recv(1024)
    try:
        decode_data = data.decode()
    except UnicodeDecodeError:
        decode_data = data.decode('utf-8', errors='replace')
    print(f"Connection from {addr}")
    print(f"Received data: {decode_data}")
    save(f"Connection from {addr} - Data: {decode_data}")

def connection_acceptor(server):
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_connection, args=(conn, addr))
        thread.start()
        
def main():
    try:
        server = TCPServer('localhost', 8080)
        server.bind()
        server.listen()
        print(f"Listening on {server.host}:{server.port}")
        connection_acceptor(server)
    except Exception as e:
        server.sock.close()
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Server shutting down.")
        server.sock.close()

if __name__ == "__main__":
    main()