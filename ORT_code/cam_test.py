import cv2
from pyzbar.pyzbar import decode

def scan_qr_code_webcam():
    """
    Scans for QR codes using the webcam and prints the decoded data.
    """
    cap = cv2.VideoCapture(1)  # 0 for default webcam

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Scanning for QR codes... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        # Decode QR codes in the frame
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            print("QR Code Data:", obj.data.decode('utf-8'))
            # Draw a bounding box around the QR code
            points = obj.polygon
            if len(points) == 4:
                # Convert points to a list of tuples (x, y)
                pts = [(p.x, p.y) for p in points]
                for i in range(4):
                    cv2.line(frame, pts[i], pts[(i + 1) % 4], (0, 255, 0), 3)

        # Display the frame
        cv2.imshow('QR Code Scanner', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_qr_code_webcam()