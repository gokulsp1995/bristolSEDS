import socket
import cv2
import numpy as np
import struct
import time

pi_ip = '192.168.253.29'  # Replace with your Pi's IP
port = 8485

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((pi_ip, port))
print("[CLIENT] Connected to Pi")

data_buffer = b""
payload_size = struct.calcsize(">L")

try:
    while True:
        start_time = time.time()

        # Receive frame length
        while len(data_buffer) < payload_size:
            data_buffer += client_socket.recv(4096)
        packed_msg_size = data_buffer[:payload_size]
        data_buffer = data_buffer[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        # Receive full frame data
        while len(data_buffer) < msg_size:
            data_buffer += client_socket.recv(4096)
        frame_data = data_buffer[:msg_size]
        data_buffer = data_buffer[msg_size:]

        # Decode and show frame
        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("Live Stream", frame)

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        print(f"[CLIENT] Frame latency: {latency_ms:.2f} ms")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    client_socket.close()
    cv2.destroyAllWindows()
