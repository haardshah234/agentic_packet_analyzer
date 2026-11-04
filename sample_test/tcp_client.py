import socket

host = '127.0.0.1'
port = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print(f"[*] Connected to server at {host}:{port}")

message = "Hello, server! Fire-and-forget message."
# Send data without calling client_socket.recv()
client_socket.sendall(message.encode('utf-8'))
print(f"Sent: {message}")

client_socket.close()
print("[*] Client closed connection.")