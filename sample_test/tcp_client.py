import socket
import re

def parse_message(message: str) -> bytes:
    parts = re.split(r'\((0x[0-9A-Fa-f]+)\)', message)

    result = bytearray()

    for part in parts:
        if part.startswith("0x"):
            value = int(part, 16)

            if not 0 <= value <= 255:
                raise ValueError(f"Value out of byte range: {part}")

            result.append(value)
        else:
            result.extend(part.encode('utf-8'))

    return bytes(result)


host = '127.0.0.1'
port = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print(f"[*] Connected to server at {host}:{port}")

while True:
    message = input("Enter a message: ")
    # Send data without calling client_socket.recv()
    message = parse_message(message)
    client_socket.sendall(message)
    print(f"Sent: {message}")

client_socket.close()
print("[*] Client closed connection.")