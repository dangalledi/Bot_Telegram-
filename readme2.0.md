# Bot de Telegram con Pantalla OLED

Este proyecto implementa un bot de Telegram en Python que interactúa con una pantalla OLED conectada a una Raspberry Pi a través de I2C.

## Requisitos

### Hardware:
- Raspberry Pi (cualquier modelo compatible con I2C)
- Pantalla OLED basada en el controlador SSD1306
- Conexión física entre la pantalla y la Raspberry Pi mediante I2C (SCL y SDA)

### Software:
- Python 3
- Entorno virtual de Python
- Acceso a internet para instalar dependencias

## Instalación

### 1. Clonar el repositorio

Clona este repositorio en tu Raspberry Pi:

```bash
git clone https://github.com/tu-usuario/bot_telegram.git
cd bot_telegram
```

### 2. Crear y activar un entorno virtual

Es recomendable utilizar un entorno virtual de Python para gestionar las dependencias. Para crear y activar el entorno virtual, ejecuta:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

Con el entorno virtual activado, instala las dependencias necesarias para el bot de Telegram y la pantalla OLED.

#### Dependencias de Python:

```bash
pip install pyTelegramBotAPI adafruit-circuitpython-ssd1306 Pillow
```

#### Otras dependencias del sistema:

Asegúrate de tener instalados los siguientes paquetes en tu Raspberry Pi:

```bash
sudo apt-get update
sudo apt-get install python3-dev python3-smbus i2c-tools
```

### 4. Habilitar I2C en la Raspberry Pi

Para que la Raspberry Pi pueda comunicarse con la pantalla OLED a través de I2C, habilita la interfaz I2C:

```bash
sudo raspi-config
```

Selecciona **Interfacing Options** > **I2C** y habilita la interfaz. Luego, reinicia la Raspberry Pi.

### 5. Verificar la conexión de la pantalla OLED

Para asegurarte de que la pantalla OLED esté conectada correctamente, ejecuta:

```bash
sudo i2cdetect -y 1
```

Deberías ver un dispositivo en la dirección `0x3c` si la pantalla está conectada correctamente.

### 6. Configurar el bot de Telegram

Debes crear un bot en Telegram y obtener un **token**. Sigue los pasos en la [documentación de Telegram](https://core.telegram.org/bots#botfather) para crear un bot.

Una vez que tengas el token, colócalo en tu script principal (`bot.py`) en la parte correspondiente.

### 7. Ejecutar el bot

Con el entorno virtual activado, puedes ejecutar el bot con:

```bash
python3 bot.py
```

## Uso

El bot estará ahora en funcionamiento y responderá a los mensajes que le envíen los usuarios. Además, actualizará la pantalla OLED con la información que se le especifique en el código.

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

