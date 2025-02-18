import re
import qrcode

def generate_qr_code(data: str):
    """Crate qr code and print in terminal"""
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr.print_ascii()

def is_phone_number(text: str) -> bool:
    """
    Проверяет, является ли переданный текст номером телефона.
    Поддерживает российский формат +7XXXXXXXXXX, 8XXXXXXXXXX, а также международные форматы.
    """
    pattern = re.compile(r'^(\+\d{1,3})?[-.\s]?(\d{1,4})?[-.\s]?(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{2})[-.\s]?(\d{2})$')
    return bool(pattern.match(text))