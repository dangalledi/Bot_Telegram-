# bot.py

import os
import time
import threading
import telebot
from utils import llamadaSistema, obtener_ip
from oled_display import actualizar_pantalla
from handlers.admin_handler import admin
from handlers.basic_commands import start, ping, fecha, comandos
from handlers.system_commands import status, ip
from handlers.minecraft_handler import minecraft, handle_docker_commands
from handlers.transmission_handler import mostrar_menu_torrents, agregar_torrent, estado_descargas, eliminar_torrent, listar_torrents, eliminar_torrent_step, agregar_torrent_step 
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(token=os.getenv('TOKEN'))

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

# Registrar los manejadores de comandos
@bot.message_handler(commands=['start', 'inicio'])
def handle_start(message):
    start(bot, message)
    reset_pantalla_timer()

@bot.message_handler(commands=['admin'])
def handle_admin(message):
    admin(bot, message)
    reset_pantalla_timer()

@bot.message_handler(commands=['ping'])
def handle_ping(message):
    ping(bot, message)
    reset_pantalla_timer()
    
@bot.message_handler(commands=['comandos'])
def handler_comandos(message):
    comandos(bot, message)
    reset_pantalla_timer()

@bot.message_handler(commands=['fecha'])
def handle_fecha(message):
    fecha(bot, message)
    reset_pantalla_timer()

@bot.message_handler(commands=['status'])
def handle_status(message):
    status(bot, message)
    reset_pantalla_timer()

@bot.message_handler(commands=['ip'])
def handle_ip(message):
    ip(bot, message)
    reset_pantalla_timer()

@bot.message_handler(commands=['minecraft', 'mc'])
def handle_minecraft(message):
    minecraft(bot, message)
    reset_pantalla_timer()

@bot.callback_query_handler(func=lambda call: call.data in ["stop", "start", "detalle"])
def handle_docker_commands(call):
    print(f"Comando de Docker recibido: {call.data}")
    
    if call.data == "stop":
        bot.send_message(call.message.chat.id, "Deteniendo el servidor de Docker...")
        # Agrega tu lógica para detener el servidor de Docker
    
    elif call.data == "start":
        bot.send_message(call.message.chat.id, "Iniciando el servidor de Docker...")
        # Agrega tu lógica para iniciar el servidor de Docker
    
    elif call.data == "detalle":
        bot.send_message(call.message.chat.id, "Mostrando detalles del servidor de Docker...")
        # Agrega tu lógica para mostrar los detalles
    
    reset_pantalla_timer()

@bot.callback_query_handler(func=lambda call: call.data in ["ip", "status", "pwd", "ls"])
def handle_system_commands(call):
    print(f"Comando del sistema recibido: {call.data}")
    
    if call.data == "ip":
        # Mostrar la IP
        ip_address = obtener_ip()
        bot.send_message(call.message.chat.id, f"IP del sistema: {ip_address}")
    
    elif call.data == "status":
        # Mostrar estado del sistema (puedes mover tu función status aquí)
        status_info = llamadaSistema("top -bn1 | grep 'Cpu(s)'")
        bot.send_message(call.message.chat.id, f"Estado del sistema: {status_info}")
    
    elif call.data == "pwd":
        # Mostrar el directorio actual
        current_dir = llamadaSistema("pwd")
        bot.send_message(call.message.chat.id, f"Directorio actual: {current_dir}")
    
    elif call.data == "ls":
        # Mostrar los archivos en el directorio actual
        files = llamadaSistema("ls")
        bot.send_message(call.message.chat.id, f"Archivos:\n{files}")
    
    reset_pantalla_timer()  # Para manejar la pantalla
  
# Manejador para el comando /torrents
@bot.message_handler(commands=['torrents'])
def handle_torrents(message):
    mostrar_menu_torrents(bot, message)

# Manejador de callbacks para torrents
@bot.callback_query_handler(func=lambda call: call.data in ["agregar_torrent", "estado_descargas", "listar_torrents", "eliminar_torrent"])
def handle_torrent_callback(call):
    if call.data == "agregar_torrent":
        bot.send_message(call.message.chat.id, "Envía el enlace del torrent (magnet o archivo):")
        bot.register_next_step_handler(call.message, lambda msg: agregar_torrent_step(bot, msg))

    elif call.data == "estado_descargas":
        respuesta = estado_descargas()
        bot.send_message(call.message.chat.id, respuesta)

    elif call.data == "listar_torrents":
        respuesta = listar_torrents()
        bot.send_message(call.message.chat.id, respuesta)

    elif call.data == "eliminar_torrent":
        bot.send_message(call.message.chat.id, "Envía el ID del torrent que deseas eliminar:")
        bot.register_next_step_handler(call.message, lambda msg: eliminar_torrent_step(bot, msg))

# Mantener la dirección IP en la pantalla hasta que haya interacción con el bot
pantalla_timer = None
reset_pantalla_timer()

while True:
    try:
        bot.send_message(os.getenv('ADMIN_ID'), '¡Desperté!', disable_notification=True)
        time.sleep(60)
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(15)
