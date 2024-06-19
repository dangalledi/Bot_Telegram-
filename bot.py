# bot.py

import time
import threading
import telebot
from config import TOKEN, ADMIN_ID
from utils import obtener_ip
from oled_display import actualizar_pantalla
from handlers.admin_handler import admin
from handlers.basic_commands import start, ping, fecha, comandos
from handlers.system_commands import status, ip
from handlers.minecraft_handler import minecraft, handle_docker_commands

bot = telebot.TeleBot(token=TOKEN)

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
def handle_callback(call):
    handle_docker_commands(bot, call)
    reset_pantalla_timer()

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
