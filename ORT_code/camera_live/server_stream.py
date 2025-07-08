import socket
import cv2
import struct
import time

# QR detection setup
qr_detector = cv2.QRCodeDetector()
detected_qr_codes = set()  # Store unique QR data

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Socket setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 8485))  # Bind to all available interfaces
server_socket.listen(1)
print("[SERVER] Waiting for client connection...")
conn, addr = server_socket.accept()
print(f"[SERVER] Connected to {addr}")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # --- QR CODE SCAN ---
        qr_data, bbox, _ = qr_detector.detectAndDecode(frame)
        if qr_data:
            if qr_data not in detected_qr_codes:
                detected_qr_codes.add(qr_data)
                print(f"[QR] Detected: {qr_data}")
                with open("qr_log.txt", "a") as f:
                    f.write(f"{time.ctime()} - {qr_data}\n")

        # --- Encode and send frame ---
        _, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()
        size = len(data)

        # Send size and data
        conn.sendall(struct.pack(">L", size))
        conn.sendall(data)

finally:
    cap.release()
    conn.close()
    server_socket.close()