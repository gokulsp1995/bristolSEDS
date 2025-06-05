import socket
import cv2
import numpy as np
import struct
import time
print(cv2.__version__)
qr = cv2.QRCodeDetector()
print("Detector works:", qr is not None)

pi_ip = '192.168.133.29'  
port = 8485

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((pi_ip, port))
print("[CLIENT] Connected to Pi")

data_buffer = b""
payload_size = struct.calcsize(">L")

# QR Code Detector
qr_detector = cv2.QRCodeDetector()
detected_qr_data = set()  # To store unique QR codes

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

        # Detect QR code
        data, bbox, _ = qr_detector.detectAndDecode(frame)
        if data:
            if data not in detected_qr_data:
                print(f"[QR] New QR Code Detected: {data}")
                detected_qr_data.add(data)
                # Optional: write to file
                with open("qr_log.txt", "a") as f:
                    f.write(data + "\n")

            # Draw bounding box if QR detected
            if bbox is not None:
                bbox = bbox.astype(int)
                for i in range(len(bbox[0])):
                    pt1 = tuple(bbox[0][i])
                    pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
                cv2.putText(frame, data, (bbox[0][0][0], bbox[0][0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Show frame
        cv2.imshow("Live Stream", frame)

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        print(f"[CLIENT] Frame latency: {latency_ms:.2f} ms")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    client_socket.close()
    cv2.destroyAllWindows()
