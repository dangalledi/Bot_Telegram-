# -*- coding: utf-8 -*-

# Importar librerias
import os
import sys
import time
import glob
import numbers
import subprocess
import telebot
import asyncio
# Importar desde librerias
#from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler)

##############################

TOKEN = "877543134:AAEydNfa6WwagUYuF6SWJt5Z0VaxCXc5H1Y" # A establecer por el usuario (consultar mediante @BotFather)
ID = 76726375 # A establecer por el usuario (consultar mediante @get_id_bot)

bot = telebot.TeleBot(token=TOKEN)
##############################

# Funcion para realizar llamadas del sistema (ejecutar comandos Linux)
def llamadaSistema(entrada):
    salida = "" # Creamos variable vacia
    f = os.popen(entrada) # Llamada al sistema
    for i in f.readlines(): # Leemos caracter a caracter sobre la linea devuelta por la llamada al sistema
        salida += i  # Insertamos cada uno de los caracteres en nuestra variable
    salida = salida[:-1] # Truncamos el caracter fin de linea '\n'

    return salida # Devolvemos la respuesta al comando ejecutado

##############################

# Comandos recibidos

# Manejador correspondiente al comando /inicio
@bot.message_handler(commands=['start','inicio'])
def start(message):
    bot.reply_to(message,"Este es un Bot que permite controlar y comprobar ciertos aspectos de una Raspberry Pi en el que se aloja. Para conocer los comandos implementados consulta la /ayuda") # Respondemos al comando con el mensaje
    print('start')

# Manejador correspondiente al comando /ayuda
@bot.message_handler(commands=['ayuda'])
def ayuda(message):
    bot.reply_to(message,"Lista de comandos implementados: \n\n/inicio - Comando de inicio\n\n/ayuda - Consulta la lista de comandos implementados y la descripcion de estos\n\n/comandos - Consulta de forma rapida la lista de comandos implementados\n\n/apagar - Apaga el sistema\n\n/reiniciar - Reiniciar el sistema\n\n/red_conectada - Consulta el nombre de la red a la que esta conectado\n\n/ip - Consulta la IP del sistema\n\n/temp - Consulta la temperatura actual del SOC\n\n/fecha - Consulta la fecha del sistema\n\n/almacenamientos - Consulta los dispositivos de almacenamiento en el sistema\n\n/arquitectura - Consulta la arquitectura del SOC\n\n/kernel - Consulta la version del Kernel del sistema\n\n/pwd - Consulta la ruta actual del Script del Bot\n\n /temp_ambiente") # Respondemos al comando con el mensaje
    print('ayuda')

#\n/cd - Accede a un directorio especifico\n\n/ls - Lista los archivos de una ruta especifica\n\n/lsusb - Consulta los dispositivos USB conectados al sistema\n\n/montajes - Consulta los dispositivos montados en el sistema\n\n/borrar - Elimina un archivo o directorio\n\n/cat - Muestra el contenido de un archivo\n\n/ssh_on - Activa el servidor SSH\n\n/ssh_off - Detiene el servidor SSH\n\n/ssh_reiniciar - Reinicia el servidor SSH\n\n/ssh_estado - Consulta el estado actual del servidor SSH\n\n/vnc_on - Activa el servidor VNC\n\n/vnc_off - Detiene el servidor VNC\n\n/scriptfex - Genera el archivo script.fex del sistema y lo exporta\n\n/importar - Importa archivos al sistema\n\n/exportar - Exporta archivos del sistema\n\n/drivers - Consulta los Drivers activos en el sistema\n\n/descargar - Realiza la descarga desde una URL (wget)\n\n/buscar - Realiza una busqueda de archivos segun un termino de busqueda en una localizacion especificada

def is_api_group(chat_id):
    return chat_id == GROUP_CHAT_ID


@bot.message_handler(func=lambda m: True, content_types=['new_chat_participant'])
def on_user_joins(message):
    if not is_api_group(message.chat.id):
        return

    name = message.new_chat_participant.first_name
    if hasattr(message.new_chat_participant, 'last_name') and message.new_chat_participant.last_name is not None:
        name += u" {}".format(message.new_chat_participant.last_name)

    if hasattr(message.new_chat_participant, 'username') and message.new_chat_participant.username is not None:
        name += u" (@{})".format(message.new_chat_participant.username)

    bot.reply_to(message, text_messages['welcome'].format(name=name))
    print('DHT11')

# Manejador correspondiente al comando /comandos
@bot.message_handler(commands=['comandos'])
def comandos(message):
    bot.reply_to(message,"Lista de comandos implementados: \n/inicio\n/ayuda\n/comandos\n/apagar\n/reiniciar\n/red_conectada\n/ip\n/temp\n/fecha\n/almacenamientos\n/arquitectura\n/kernel\n/pwd\n/temp_ambiente") # Respondemos al comando con el mensaje
    print('comandos')
#\n/cd\n/ls\n/lsusb\n/montajes\n/borrar\n/cat\n/ssh_on\n/ssh_off\n/ssh_reiniciar\n/ssh_estado\n/vnc_on\n/vnc_off\n/scriptfex\n/importar\n/exportar\n/drivers\n/descargar\n/buscar

# Manejador correspondiente al comando /apagar
@bot.message_handler(commands=['apagar'])
def apagar(message):
    bot.reply_to(message,"Apagando el sistema") # Respondemos al comando con el mensaje
    llamadaSistema("shutdown -h now") # Llamada al sistema
    print('apagar')

# Manejador correspondiente al comando /reiniciar
@bot.message_handler(commands=['reiniciar'])
def reiniciar(message):
    bot.reply_to(message,"Reiniciando el sistema") # Respondemos al comando con el mensaje
    llamadaSistema("reboot") # Llamada al sistema
    print('reboot')

# Manejador correspondiente al comando /red_conectada
@bot.message_handler(commands=['red_conectada'])
def red_conectada(message):
    ssidred = llamadaSistema("iwgetid") # Llamada al sistema
    bot.reply_to(message,ssidred) # Respondemos al comando con el mensaje
    print('red_conectada')

# Manejador correspondiente al comando /ip
@bot.message_handler(commands=['ip'])
def ip(message):
    ip = llamadaSistema("hostname -I") # Llamada al sistema
    ip = ip[:-1] # Eliminamos el ultimo caracter
    bot.reply_to(message,ip) # Respondemos al comando con el mensaje
    print('ip')

# Manejador correspondiente al comando /temp
@bot.message_handler(commands=['temp'])
def temp(message):
    temp = llamadaSistema(" /opt/vc/bin/vcgencmd measure_temp") # Llamada al sistema
    bot.reply_to(message,temp) # Respondemos al comando con el mensaje
    print('temp')

# Manejador correspondiente al comando /DHT11
@bot.message_handler(commands=['DHT11'])
def DHT11(message):
    llamadaSistema(" cd")
    print('DHT11')
    #DHT11 = llamadaSistema(" Adafruit_Python_DHT/examples/./AdafruitDHT.py 11 4 ") # Llamada al sistema
    bot.reply_to(message,DHT11) # Respondemos al comando con el mensaje
    print('DHT11')

@bot.message_handler(commands=["ping"])
def on_ping(message):
    bot.reply_to(message, "Still alive and kicking!")
    print('ping')

# Manejador correspondiente al comando /fecha
@bot.message_handler(commands=['fecha'])
def fecha(message):
    fecha = llamadaSistema("date") # Llamada al sistema
    bot.reply_to(message,fecha) # Respondemos al comando con el mensaje
    print('fecha')

# Manejador correspondiente al comando /almacenamientos
@bot.message_handler(commands=['almacenamientos'])
def almacenamientos(message):
    _fdisk = llamadaSistema("fdisk -l") # Llamada al sistema
    bot.reply_to(message,_fdisk) # Respondemos al comando con el mensaje
    print('almacenamientos')

# Manejador correspondiente al comando /arquitectura
@bot.message_handler(commands=['arquitectura'])
def arquitectura(message):
    _arquitectura = llamadaSistema("arch") # Llamada al sistema
    bot.reply_to(message,_arquitectura) # Respondemos al comando con el mensaje
    print('arquitectura')

# Manejador correspondiente al comando /kernel
@bot.message_handler(commands=['kernel'])
def kernel(message):
    _kernel = llamadaSistema("cat /proc/version") # Llamada al sistema
    bot.reply_to(message,_kernel) # Respondemos al comando con el mensaje
    print('kernel')

# Manejador correspondiente al comando /drivers
@bot.message_handler(commands=['drivers'])
def drivers(message):
    _lsmod = llamadaSistema("lsmod") # Llamada al sistema
    bot.reply_to(message,_lsmod) # Respondemos al comando con el mensaje
    print('drivers')

# Manejador correspondiente al comando /pwd
@bot.message_handler(commands=['pwd'])
def pwd(message):
    _pwd = llamadaSistema("pwd") # Llamada al sistema
    bot.reply_to(message,_pwd) # Respondemos al comando con el mensaje
    print('pwd')

# Manejador correspondiente al comando /cd
@bot.message_handler(commands=['cd'], pass_=True)
def cd(message, args):
    print('1')
    if len(args) == 1: # Comprobar si el comando presenta argumento o no
        print('2')
        directorio = args[0]
        os.chdir(directorio)
        bot.reply_to(message,"Cambiando al directorio " + directorio) # Respondemos al comando con el mensaje
    else:
        print('3')
        bot.reply_to(message,"Se debe especificar el directorio al que acceder.\n\nEjemplo:\n/cd /home/usuario") # Respondemos al comando con el mensaje

# Manejador correspondiente al comando /temp_ambiente
@bot.message_handler(commands=['temp_ambiente'])
async def temp_ambiente(message):
    amb = await llamadaSistema("python /home/pi/Adafruit_Python_DHT/examples/simpletest.py") # Llamada al sistema
    bot.reply_to(message,amb) # Respondemos al comando con el mensaje
    #bot.send_message(ID,amb)
    print('temp_ambiente')

# Manejador correspondiente al comando /temp_ambiente
@bot.message_handler(commands=['temp_ambiente_12'])
def temp_ambiente_12(message):
    #bot.reply_to(message,_pwd) # Respondemos al comando con el mensaje
    tiempo=0
    while tiempo >= 43200 :
        amb12 = llamadaSistema("python /home/pi/Adafruit_Python_DHT/examples/simpletest.py")
        print('tiempo')
        bot.send_message(ID,amb12)
        time.sleep(tiempo)
        tiempo =tiempo + 900
    print('temp_ambiente_12')

'''
@bot.message_handler(commands=['temp_acua'])
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
        bot.reply_to(message,"Temp: " + temp_c) # Respondemos al comando con el mensaje


# Manejador correspondiente al comando /ls
def ls(bot, update, args):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        if len(args) == 1: # Comprobar si el comando presenta argumento o no
            _ls = llamadaSistema("ls " + args[0]) # Llamada al sistema
        else:
            _ls = llamadaSistema("ls") # Llamada al sistema
        bot.reply_to(message,_ls) # Respondemos al comando con el mensaje

# Manejador correspondiente al comando /lsusb
def lsusb(message):
    _lsusb = llamadaSistema("lsusb") # Llamada al sistema
    bot.reply_to(message,_lsusb) # Respondemos al comando con el mensaje

# Manejador correspondiente al comando /montajes
def montajes(bot, update):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        _df = llamadaSistema("df") # Llamada al sistema
        bot.reply_to(message,_df) # Respondemos al comando con el mensaje

# Manejador correspondiente al comando /borrar
def borrar(bot, update, args):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        if len(args) == 1: # Comprobar si el comando presenta argumento o no
            archivo = args[0]
            llamadaSistema("rm -rf " + args[0]) # Llamada al sistema
            bot.reply_to(message,"Archivo " + archivo + " borrado") # Respondemos al comando con el mensaje
        else:
            bot.reply_to(message,"Especifica un archivo.\n\nEjemplo:\n/borrar /home/user/archivo.txt") # Respondemos al comando con el mensaje

# Manejador correspondiente al comando /cat
def cat(bot, update, args):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        if len(args) == 1: # Comprobar si el comando presenta argumento o no
            _cat = llamadaSistema("cat " + args[0]) # Llamada al sistema
            num_caracteres_fichero = len(_cat) # Determinamos el numero de caracteres que tiene el archivo
            if num_caracteres_fichero < 4096: # Si el numero de caracteres es menor a 4096 se envia un unico mensaje con todo el contenido
                bot.reply_to(message,_cat) # Respondemos al comando con el mensaje
            else: # Si el numero de caracteres es superior a 4096, se divide el contenido del archivo en diversos fragmentos de texto que se enviaran en varios mensajes
                num_mensajes = num_caracteres_fichero/float(4095) # Se determina el numero de mensajes a enviar
                if isinstance(num_mensajes, numbers.Integral) != True: # Si no es un numero entero (es decimal)
                    num_mensajes = int(num_mensajes) + 1 # Se aumenta el numero de mensajes en 1
                fragmento = 0
                for i in range(0, num_mensajes): # Se van enviando cada fragmento de texto en diversos mensajes
                    mensaje = _cat[fragmento:fragmento+4095].decode('utf-8', 'ignore') # Creamos un mensaje correspondiente al fragmento de texto actual
                    bot.reply_to(message,mensaje) # Respondemos al comando con el mensaje
                    fragmento = fragmento + 4095 # Aumentamos el fragmento de texto (cursor de caracteres)
        else:
            bot.reply_to(message,"Especifica un archivo.\n\nEjemplo:\n/cat /home/user/archivo.txt") # Respondemos al comando con el mensaje

# Manejador correspondiente al comando /ssh_on
def ssh_on(bot, update):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        llamadaSistema("/etc/init.d/ssh start") # Llamada al sistema
        bot.reply_to(message,"Iniciando servidor SSH") # Respondemos al comando con el mensaje

# Manejador correspondiente al comando /ssh_off
def ssh_off(bot, update):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        llamadaSistema("/etc/init.d/ssh stop") # Llamada al sistema
        bot.reply_to(message,"Deteniendo servidor SSH") # Respondemos al comando con el mensaje

# Manejador correspondiente al comando /ssh_reiniciar
def ssh_reiniciar(bot, update):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        llamadaSistema("/etc/init.d/ssh restart") # Llamada al sistema
        bot.reply_to(message,respuesta) # Respondemos al comando con el mensaje

# Manejador correspondiente al comando /ssh_estado
def ssh_estado(bot, update):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        respuesta = llamadaSistema("/etc/init.d/ssh status") # Llamada al sistema
        bot.reply_to(message,respuesta) # Respondemos al comando con el mensaje

# Manejador correspondiente al comando /vnc_on
def vnc_on(bot, update):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        update.message.reply_text("Iniciando servidor VNC")     # Respondemos al comando con el mensaje
        bot.reply_to(message,"vncserver :1 -geometry 1080x720 -depth 16 -pixelformat rgb565") # Llamada al sistema

# Manejador correspondiente al comando /vnc_off
def vnc_off(bot, update):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        bot.reply_to(message,"Cerrando servidor VNC") # Respondemos al comando con el mensaje
        llamadaSistema("vncserver -kill :1") # Llamada al sistema


# Manejador correspondiente al comando /scriptfex
def scriptfex(bot, update):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
        llamadaSistema("bin2fex /boot/script.bin /boot/script.fex") # Transforma Script.bin en Script.fex
        time.sleep(5) # Esperamos 5 segundos (para que se complete la transformacion)
        bot.sendDocument(ID, open('/boot/script.fex', 'rb')) # Enviamos el archivo

# Manejador correspondiente al comando /exportar
def exportar(bot, update, args):
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
    if len(args) == 1: # Solo hacer caso si el comando presenta argumento
        archivo = open(args[0], 'rb') # Abrimos el archivo
        try:
            bot.sendDocument(ID, archivo) # Intentar enviar el archivo
        finally:
            archivo.close() # Cerrar el archivo
    else:
        bot.reply_to(message,"Se debe especificar el archivo que deseas extraer.\n\nEjemplo:\n/exportar /home/user/archivo") # Respondemos al comando con el mensaje

esperando_archivo = 0
ruta_poner_archivo = ""
# Manejador correspondiente al comando /importar
def importar(bot, update, args):
    global esperando_archivo
    global ruta_poner_archivo
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
    if len(args) == 1: # Solo hacer caso si el comando presenta argumento
        ruta_poner_archivo = args[0]
        bot.reply_to(message,"Inserta el archivo a enviar (tipo documento)")
        esperando_archivo = 1
    else:
        bot.reply_to(message,"Se debe especificar la ruta donde deseas importar el archivo.\n\nEjemplo:\n/importar /home/user") # Respondemos al comando con el mensaje

esperando_ruta = 0
enlace_descarga = ""
# Manejador correspondiente al comando /descargar
def descargar(bot, update, args):
    global esperando_ruta
    global enlace_descarga
    #if update.message.chat_id == ID: # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
    if len(args) == 2: # Si el comando presenta 2 argumentos
        enlace_descarga = args[0]
        ruta = args[1]
        subprocess.Popen(["nohup", "wget", enlace_descarga, "-P", ruta])
        bot.reply_to(message,"Descargando en '" + ruta + "' desde el enlace " + enlace_descarga) # Respondemos al comando con el mensaje
    elif len(args) == 1: # Si el comando presenta 1 argumento
        if esperando_ruta == 0:
            enlace_descarga = args[0]
            bot.reply_to(message,"Especifica a continuacion, la ruta donde almacenar el archivo a descargar.\n\nEjemplo:\n/descargar https://raw.githubusercontent.com/J-Rios/TelegramBots/master/opibot.py /home/usuario/descargas")
            esperando_ruta = 1
    else:
        bot.reply_to(message,"Se debe especificar el enlace (URL) de descarga y el directorio de descarga.\n\nEjemplo:\n/descargar https://raw.githubusercontent.com/J-Rios/TelegramBots/master/opibot.py /home/usuario/descargas") # Respondemos al comando con el mensaje

# Manejador correspondiente al comando /buscar
def buscar(bot, update, args):
    #if update.message.chat_id == ID: # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
    if len(args) == 2: # Si el comando presenta 2 argumentos
        nombre_archivo = args[0]
        ruta = args[1]
        resultado = llamadaSistema("find " + ruta + " -name '*" + nombre_archivo + "*'") # Llamada al sistema
        bot.reply_to(message,"Archivos encontrados para el termino de busqueda:\n\n'" + resultado) # Respondemos al comando con el mensaje
    else:
        bot.reply_to(message,"Se debe especificar el archivo y el directorio desde el que buscar.\n\nEjemplo:\n/buscar .log /") # Respondemos al comando con el mensaje

##############################

# Manejador para mensajes recibidos que no son comandos
def mensaje_nocomando(bot, update):
    global esperando_ruta
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
    if esperando_ruta == 1:
        esperando_ruta = 0
        ruta = update.message.text
        subprocess.Popen(["nohup", "wget", enlace_descarga, "-P", ruta])
        bot.reply_to(message,"Descargando en '" + ruta + "' desde el enlace " + enlace_descarga) # Respondemos al comando con el mensaje
    else:
        bot.reply_to(message,"Por favor envia un comando adecuado.\n\nPara conocer los comandos implementados consulta la /ayuda") # Respondemos al comando con el mensaje

# Manejador para recepcion de archivos enviados por el usuario
def archivo_recibido(bot, update):
    global esperando_archivo
    global ruta_poner_archivo
    #if update.message.chat_id == ID : # Solo hacer caso si quien le habla es el remitente correspondiente a dicha ID
    if esperando_archivo == 1:
        nombre_archivo = update.message.document.file_name
        id_archivo = update.message.document.file_id
        archivo = bot.getFile(id_archivo)
        ruta_actual = os.getcwd()
        os.chdir(ruta_poner_archivo)
        archivo.download(nombre_archivo)
        os.chdir(ruta_poner_archivo)
        bot.reply_to(message,"Archivo " + nombre_archivo + " recibido y posicionado en " + ruta_poner_archivo)
        esperando_archivo = 0

##############################

def main():
    # Crear el manejador de eventos a partir del TOKEN del bot
    updater = Updater(TOKEN)

    # Obtener el registro de manejadores del planificador
    dp = updater.dispatcher

    # Asociamos manejadores para cada comando reconocible
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ayuda", ayuda))
    dp.add_handler(CommandHandler("comandos", comandos))
    dp.add_handler(CommandHandler("apagar", apagar))
    dp.add_handler(CommandHandler("reiniciar", reiniciar))
    dp.add_handler(CommandHandler("red_conectada", red_conectada))
    dp.add_handler(CommandHandler("ip", ip))
    dp.add_handler(CommandHandler("temp", temp))
    dp.add_handler(CommandHandler("fecha", fecha))
    dp.add_handler(CommandHandler("almacenamientos", almacenamientos))
    dp.add_handler(CommandHandler("arquitectura", arquitectura))
    dp.add_handler(CommandHandler("kernel", kernel))
    dp.add_handler(CommandHandler("pwd", pwd))
    dp.add_handler(CommandHandler("drivers", drivers))
    dp.add_handler(CommandHandler("cd", cd, pass_args=True))
    dp.add_handler(CommandHandler("ls", ls, pass_args=True))
    dp.add_handler(CommandHandler("lsusb", lsusb))
    dp.add_handler(CommandHandler("montajes", montajes))
    dp.add_handler(CommandHandler("borrar", borrar, pass_args=True))
    dp.add_handler(CommandHandler("cat", cat, pass_args=True))
    dp.add_handler(CommandHandler("ssh_on", ssh_on))
    dp.add_handler(CommandHandler("ssh_off", ssh_off))
    dp.add_handler(CommandHandler("ssh_reiniciar", ssh_reiniciar))
    dp.add_handler(CommandHandler("ssh_estado", ssh_estado))
    dp.add_handler(CommandHandler("vnc_on", vnc_on))
    dp.add_handler(CommandHandler("vnc_off", vnc_off))
    dp.add_handler(CommandHandler("scriptfex", scriptfex))
    dp.add_handler(CommandHandler("exportar", exportar, pass_args=True))
    dp.add_handler(CommandHandler("importar", importar, pass_args=True))
    dp.add_handler(CommandHandler("descargar", descargar, pass_args=True))
    dp.add_handler(CommandHandler("buscar", buscar, pass_args=True))

    # Asociamos un manejador para cualquier mensaje recibido (no comando)
    dp.add_handler(MessageHandler(Filters.text, mensaje_nocomando))
    dp.add_handler(MessageHandler(Filters.document, archivo_recibido))

    # Iniciamos el bot
    updater.start_polling()

    # Actualizamos el estado del bot (bloquea la ejecucion a la espera de mensajes)
    updater.idle()


if __name__ == '__main__':
    main()
    '''
aux =1
while True:
    while aux == 1 :
        local_time = time.time()
        bot.send_message(ID, 'Desperte !')
        bot.send_message(ID, local_time)
        aux +=1
    try:
        bot.polling()
    except Exception:
        time.sleep(15)

# Fin del Codigo
#http://biblioteca.serindigena.org/libros_digitales/kakan/kakan_lengua_de_los_diaguitas.pdf
