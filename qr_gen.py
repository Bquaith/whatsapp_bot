import qrcode
import base64
import io
from PIL import Image
from pyzbar.pyzbar import decode

def generate_qr_code(data):
    # Создаем QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,  # Размер одного квадрата QR-кода
        border=1,    # Граница вокруг QR-кода
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr.print_ascii()

def decode_qr_from_base64(base64_string):
    # Декодируем Base64 в байты
    image_data = base64.b64decode(base64_string)
    
    # Открываем изображение с помощью PIL
    image = Image.open(io.BytesIO(image_data))
    
    # Декодируем QR-код
    decoded_objects = decode(image)
    
    # Возвращаем данные из QR-кода
    return [obj.data.decode('utf-8') for obj in decoded_objects][0]