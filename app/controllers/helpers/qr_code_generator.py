from io import BytesIO
from qrcode import QRCode
from base64 import b64encode

def get_b64_encoded_qr_code(data):
    qr = QRCode(version=1, box_size=10, border=3)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered)
    return b64encode(buffered.getvalue()).decode("utf-8")