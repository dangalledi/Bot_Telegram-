# oled_display.py

import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# Configurar la pantalla OLED a través de I2C
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

# Limpiar la pantalla
oled.fill(0)
oled.show()

# Crear una imagen en modo 1-bit con la resolución correcta
width = oled.width
height = oled.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

# Función para actualizar la pantalla OLED
def actualizar_pantalla(texto):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)  # Limpiar pantalla
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 12)
    bbox = draw.textbbox((0, 0), texto, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), texto, font=font, fill=255)
    oled.image(image)
    oled.show()
