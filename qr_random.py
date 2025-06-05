import qrcode
import os

# List of test strings to encode
qr_strings = [
    "OPTISORT_001",
    "NUCLEAR_TEST_42",
    "ROVER_QR_SCAN",
    "ZONE_ALPHA",
    "QR_DATA_123"
]

# Define save directory (change as needed)
save_dir = "C:/Users/gokul/Desktop/qr_output"
os.makedirs(save_dir, exist_ok=True)

# Loop to create and save QR code images
for i, data in enumerate(qr_strings):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    filename = f"qr_{i+1}_{data}.png"
    filepath = os.path.join(save_dir, filename)

    img.save(filepath)
    print(f"✅ Saved QR code: {filepath}")
