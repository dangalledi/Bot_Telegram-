# -*- coding: utf-8 -*-

# Importar librerias
import os
import sys
import time
import glob
import numbers
import subprocess
import telebot

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

'''# Manejador correspondiente al comando /temp_ambiente
@bot.message_handler(commands=['temp_ambiente'])
def temp_ambiente(message):
    amb = llamadaSistema("python /home/pi/Adafruit_Python_DHT/examples/simpletest.py") # Llamada al sistema
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
    print('temp_ambiente_12')'''

# Manejador correspondiente al prender o apagar un rele
GPIO.setup(12,GPIO.OUT)  

@bot.message_handler(commands=['luz_on'])
def luz_on(message):
    GPIO.output(12,GPIO.HIGH)
    amb = "Listo!"
    bot.reply_to(message,amb) 
    #bot.send_message(ID,amb)
    print('luz_on')

@bot.message_handler(commands=['luz_off'])
def luz_off(message):
    GPIO.output(12,GPIO.LOW)
    amb = "Listo!"
    bot.reply_to(message,amb)
    #bot.send_message(ID,amb)
    print('luz_off')

# Manejador correspondiente al prender o apagar la guirnalda de luces
GPIO.setup(11,GPIO.OUT)

@bot.message_handler(commands=['lucecitas_on'])
def light_on(message):
    GPIO.output(11,GPIO.HIGH)
    amb = "Listo!"
    bot.reply_to(message,amb) 
    #bot.send_message(ID,amb)
    print('light_on')

@bot.message_handler(commands=['lucecitas_off'])
def light_off(message):
    GPIO.output(11,GPIO.LOW)
    amb = "Listo!"
    bot.reply_to(message,amb)
    #bot.send_message(ID,amb)
    print('light_off')

@bot.message_handler(commands=['all_off'])
def all_off(message):
    GPIO.output(12,GPIO.LOW)
    GPIO.output(11,GPIO.LOW)
    amb = "Listo, buenas noches <3 !"
    bot.reply_to(message,amb)
    #bot.send_message(ID,amb)
    print('all_off')


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
