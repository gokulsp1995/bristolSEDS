import socket
import json
import time

pi_ip_address = '192.168.133.29'
PORT = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((pi_ip_address, PORT))
print("[CLIENT] Connected to Pi")

try:
    for i in range(12):  
        command = {
            "action": "MOVE_FORWARD",
            "time": i       
                   }
        message = json.dumps(command)
        client_socket.sendall(message.encode('utf-8'))

        response = client_socket.recv(1024)
        decoded = response.decode('utf-8')
        data = json.loads(decoded)
        print(f"[CLIENT] Received: {decoded}")
        print(f"[CLIENT] Battery: {data['battery']}, Status: {data['status']}")
        time.sleep(2)

finally:
    client_socket.close()