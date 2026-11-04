import socket

IP = "127.0.0.1"
PORT = 5001
ADDR = (IP, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(1)

print(f"Server is listening... on {ADDR}")

while True:
    conn, addr = server.accept()
    print("Connected by", addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode()}")

    conn.close()
    print("Client disconnected.")