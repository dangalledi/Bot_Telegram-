## Documentación del Bot de Telegram para la Raspberry Pi

### Descripción General

Este bot de Telegram permite administrar una Raspberry Pi, incluyendo el estado del servidor de Minecraft y otros comandos del sistema. Además, utiliza una pantalla OLED para mostrar información relevante.

### Estructura del Proyecto

```
my_bot/
├── bot.py
├── config.py
├── handlers/
│   ├── __init__.py
│   ├── admin_handler.py
│   ├── basic_commands.py
│   ├── minecraft_handler.py
│   ├── system_commands.py
├── oled_display.py
└── utils.py
```

### Archivos y Funcionalidades

#### 1. `config.py`

Contiene configuraciones y constantes globales.

```python
# config.py

TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = "userId"
```

#### 2. `oled_display.py`

Configura y gestiona la pantalla OLED.

```python
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
```

#### 3. `utils.py`

Funciones auxiliares para llamadas al sistema y obtención de la dirección IP.

```python
# utils.py

import os

def llamadaSistema(entrada):
    salida = ""  # Creamos variable vacía
    f = os.popen(entrada)  # Llamada al sistema
    for i in f.readlines():  # Leemos caracter a caracter sobre la línea devuelta por la llamada al sistema
        salida += i  # Insertamos cada uno de los caracteres en nuestra variable
    salida = salida[:-1]  # Truncamos el caracter fin de línea '\n'
    return salida  # Devolvemos la respuesta al comando ejecutado

def obtener_ip():
    return llamadaSistema("hostname -I").strip()
```

#### 4. `handlers/admin_handler.py`

Manejador del comando `/admin`.

```python
# handlers/admin_handler.py

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID
from oled_display import actualizar_pantalla

def admin(bot, message):
    username = message.from_user.username
    print(f"admin -> El mensaje fue enviado por el usuario con nombre de usuario: {username}")
    if message.from_user.id == ADMIN_ID:  # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        bot.send_message(message.chat.id, "Elige un comando para ejecutar:", reply_markup=gen_markup_admin())
        actualizar_pantalla("Acceso admin")
    else:
        mensaje = (f"Oye {username} tu no eres admin ! ¬¬")
        bot.reply_to(message, mensaje)
        actualizar_pantalla("Acceso denegado")

def gen_markup_admin():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("reiniciar", callback_data="reiniciar"),
        InlineKeyboardButton("red_conectada", callback_data="red_conectada"),
        InlineKeyboardButton("ip", callback_data="ip"),
        InlineKeyboardButton("status", callback_data="status"),
        InlineKeyboardButton("pwd", callback_data="pwd"),
        InlineKeyboardButton("ls", callback_data="ls")
    )
    return markup
```

#### 5. `handlers/basic_commands.py`

Manejadores de comandos básicos como `/start`, `/ping`, y `/fecha`.

```python
# handlers/basic_commands.py

from oled_display import actualizar_pantalla
from utils import obtener_ip

def start(bot, message):
    mensaje = """
    ¡Bienvenido al Bot de Patana que administra esta Raspberry Pi! 🎮🖥️

    PatanaBot está diseñado para ayudarte con el servidor de Minecraft directamente desde la Raspberry Pi. Aquí puedes controlar el estado del servidor y consultar el estado del server.

    🔹 **Comandos disponibles**:
    - /minecraft - Enciande/Apaga o revisa el estado del servidor de Minecraft.
    - /logs - Muestra los últimos registros del servidor.
    - /usuarios_activos - Consulta los usuarios activos en el server  
    - /tp <nombre_usuario <x> <y> <z> ó /tp <nombre_usuario> -> te lleva a la casa de la Ale y Dani

    Para ver todos los comandos y sus descripciones, usa el comando /comandos.

    Si necesitas ayuda o tienes alguna pregunta, no dudes en usar el comando /comandos.

    🔹 **Conéctate a nuestra red privada**:
    Para conectarte a nuestra red privada de ZeroTier, sigue estos pasos:
    1. Descarga e instala ZeroTier One en tu dispositivo. -> https://download.zerotier.com/dist/ZeroTier%20One.msi
    2. Abre la aplicación y busca la opción "Join New Network".
    3. Ingresa el ID de la red: `0cccb752f7b9181f`.
    4. Avísame cuando te hayas unido y te aceptaré en nuestra red. 😊
    5. Luego de agregarte a la red, ingresa al server de Minecraft 172.24.9.41:25565 y ¡Listo!
    
    ¡Comienza a jugar Minecraft ahora y asegúrate de que todo funcione!
    
    """
    bot.reply_to(message, mensaje)  # Respondemos al comando con el mensaje
    print('start')
    actualizar_pantalla("Bot iniciado")
    reset_pantalla_timer()

def ping(bot, message):
    bot.reply_to(message, "Still alive and kicking!")
    print('ping')
    actualizar_pantalla("Ping recibido")
    reset_pantalla_timer()

def fecha(bot, message):
    from utils import llamadaSistema
    fecha = llamadaSistema("date")  # Llamada al sistema
    bot.reply_to(message, fecha)  # Respondemos al comando con el mensaje
    print('fecha')
    actualizar_pantalla("Fecha mostrada")
    reset_pantalla_timer()
```

#### 6. `handlers/system_commands.py`

Manejadores de comandos del sistema como `/status` y `/ip`.

```python
# handlers/system_commands.py

from utils import llamadaSistema
from oled_display import actualizar_pantalla
from utils import obtener_ip

def status(bot, message):
    try:
        print('status')
        cpu_usage = llamadaSistema("top -bn1 | grep 'Cpu(s)'")
        memory_usage = llamadaSistema("free -m")
        disk_usage = llamadaSistema("df -h")
        temp = llamadaSistema("vcgencmd measure_temp")
        
        # Construir el mensaje de respuesta
        respuesta = (f"Uso de CPU:\n{cpu_usage}\n\n"
                    f"Uso de Memoria:\n{memory_usage}\n\n"
                    f"Uso de Disco:\n{disk_usage}\n\n"
                    f"Temperatura de la CPU:\n{temp}")
        
        bot.reply_to(message, respuesta)
        actualizar_pantalla("Estado del sistema mostrado")
        reset_pantalla_timer()
    except Exception as e:
        bot.reply_to(message, f"Error al obtener el estado del sistema: {str(e)}")
        actualizar_pantalla("Error en estado")
        reset_pantalla_timer()

def ip(bot, message):
    ip_address = obtener_ip()
    bot.reply_to(message, ip_address)
    print('ip')
    actualizar_pantalla(f"IP: {ip_address}")
    reset_pantalla_timer()
```

#### 7. `handlers/minecraft_handler.py`

Manejadores de comandos relacionados con Minecraft.

```python
# handlers/minecraft_handler.py

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import llamadaSistema
from oled_display import actualizar_pantalla

def minecraft(bot, call):
    print('minecraft')
    container_name = "mc-server"
    try:
        status_output = llamadaSistema("docker ps -f name=mc-server --format '{{.Status}}'")
        message = ("¿Qué deseas hacer? /logs\n\n"
                   f"el estado del contenedor {container_name} es: {(status_output,'esta apagado')[status_output=='']}")
        actualizar_pantalla("Minecraft: " + ("Encendido" if status_output else "Apagado"))
        reset_pantalla_timer()
    except Exception as e:
        # Manejar cualquier error
        message = ("¿Qué deseas hacer?\n\n"
                   f

"error al obtener el estado del contenedor: {str(e)}")
        actualizar_pantalla("Error Minecraft")
        reset_pantalla_timer()
    finally:
        bot.send_message(call.chat.id, message, reply_markup=gen_markup_mc())

def gen_markup_mc():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("Apagar", callback_data="stop"),
        InlineKeyboardButton("Encender", callback_data="start"),
        InlineKeyboardButton("Detalle", callback_data="detalle")
    )
    return markup

def handle_docker_commands(bot, call):
    respuesta = call.data
    # Verificar el estado actual del contenedor antes de intentar apagarlo
    status_output = llamadaSistema("docker-compose -f /home/patana/minecraft-server/docker-compose.yml ps")
    if respuesta == "stop":
        if "Exit" in status_output:
            mensaje_accion = "El servidor ya está apagado."
        else:
            accion = llamadaSistema("docker-compose -f /home/patana/minecraft-server/docker-compose.yml stop")
            mensaje_accion = "Apagando el servidor..."
    elif respuesta == "start":
        if "Up" in status_output:
            mensaje_accion = "El servidor ya está encendido."
        else:
            accion = llamadaSistema("docker-compose -f /home/patana/minecraft-server/docker-compose.yml start")
            mensaje_accion = "Encendiendo el servidor..."
    elif respuesta == "detalle":
        mensaje_accion = llamadaSistema("docker-compose -f /home/patana/minecraft-server/docker-compose.yml ps")
    else:
        mensaje_accion = "Comando desconocido"
    bot.send_message(call.from_user.id, mensaje_accion)
    reset_pantalla_timer()
```

#### 8. `bot.py`

Punto de entrada principal que importa y registra todos los manejadores.

```python
# bot.py

import time
import threading
import telebot
from config import TOKEN, ADMIN_ID
from utils import obtener_ip
from oled_display import actualizar_pantalla
from handlers.admin_handler import admin
from handlers.basic_commands import start, ping, fecha
from handlers.system_commands import status, ip
from handlers.minecraft_handler import minecraft, handle_docker_commands

bot = telebot.TeleBot(token=TOKEN)

# Registrar los manejadores de comandos
@bot.message_handler(commands=['start', 'inicio'])
def handle_start(message):
    start(bot, message)

@bot.message_handler(commands=['admin'])
def handle_admin(message):
    admin(bot, message)

@bot.message_handler(commands=['ping'])
def handle_ping(message):
    ping(bot, message)

@bot.message_handler(commands=['fecha'])
def handle_fecha(message):
    fecha(bot, message)

@bot.message_handler(commands=['status'])
def handle_status(message):
    status(bot, message)

@bot.message_handler(commands=['ip'])
def handle_ip(message):
    ip(bot, message)

@bot.message_handler(commands=['minecraft', 'mc'])
def handle_minecraft(message):
    minecraft(bot, message)

@bot.callback_query_handler(func=lambda call: call.data in ["stop", "start", "detalle"])
def handle_callback(call):
    handle_docker_commands(bot, call)

# Función para resetear el temporizador de inactividad de la pantalla
def reset_pantalla_timer():
    global pantalla_timer
    if pantalla_timer is not None:
        pantalla_timer.cancel()
    pantalla_timer = threading.Timer(60.0, mostrar_ip_pantalla)
    pantalla_timer.start()

# Función para mostrar la IP en la pantalla
def mostrar_ip_pantalla():
    actualizar_pantalla(f"IP: {obtener_ip()}")

# Mantener la dirección IP en la pantalla hasta que haya interacción con el bot
pantalla_timer = None
reset_pantalla_timer()

while True:
    try:
        bot.send_message(ADMIN_ID, '¡Desperté!', disable_notification=True)
        time.sleep(60)
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(15)
```

### Instalación

1. Clona el repositorio.
2. Instala las dependencias necesarias:
   ```bash
   pip install pyTelegramBotAPI Adafruit_SSD1306 Pillow
   ```
3. Configura tu archivo `config.py` con tu token de bot y tu ID de administrador.
4. Ejecuta el bot:
   ```bash
   python bot.py
   ```

### Uso

- `/start` o `/inicio`: Muestra un mensaje de bienvenida y comandos disponibles.
- `/admin`: Accede a los comandos administrativos (solo para el administrador).
- `/ping`: Responde con un mensaje de estado.
- `/fecha`: Muestra la fecha y hora actuales.
- `/status`: Muestra el estado del sistema (uso de CPU, memoria, disco y temperatura).
- `/ip`: Muestra la dirección IP de la Raspberry Pi.
- `/minecraft` o `/mc`: Muestra opciones para administrar el servidor de Minecraft.

### Contribuciones

Las contribuciones son bienvenidas. Si tienes alguna mejora o nueva funcionalidad, no dudes en hacer un fork del repositorio y enviar un pull request.

### Licencia

Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo `LICENSE`.

Espero que esta documentación te sea útil y facilite la comprensión y el uso de tu bot de Telegram para la Raspberry Pi.