# oled_display.py

import Adafruit_GPIO.I2C as I2C
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

# Configurar la pantalla OLED
RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

# Crear una imagen en modo 1-bit con la resolución correcta
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

# Función para actualizar la pantalla OLED
def actualizar_pantalla(texto):
    draw.rectangle((0, 0, width, height), outline=0, fill=0)  # Limpiar pantalla
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 12)
    (text_width, text_height) = draw.textsize(texto, font=font)
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), texto, font=font, fill=255)
    disp.image(image)
    disp.display()
