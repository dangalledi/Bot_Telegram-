# handlers/system_commands.py

from utils import llamadaSistema, obtener_ip
from oled_display import actualizar_pantalla
from logger import log_action 

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
    except Exception as e:
        bot.reply_to(message, f"Error al obtener el estado del sistema: {str(e)}")
        log_action(message.from_user.username, '/status')
        actualizar_pantalla("Error en estado")

def ip(bot, message):
    ip_address = obtener_ip()
    bot.reply_to(message, ip_address)
    print('ip')
    log_action(message.from_user.username, '/ip')
    actualizar_pantalla(f"IP: {ip_address}")
