# logger.py

import logging
from datetime import datetime

# Generar un nombre de archivo único basado en el timestamp actual
log_filename = datetime.now().strftime('bot_log_%Y%m%d_%H%M%S.log')

# Configuración del logger
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def log_action(user, action):
    logging.info(f'User: {user} - Action: {action}')