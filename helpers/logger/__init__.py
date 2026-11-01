
import logging
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
from pathlib import Path

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)

# Handler para exibir mensagens no terminal
streamHandler = StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Handler para salvar mensagens em arquivo
BASE_DIR = Path(__file__).resolve().parent.parent.parent

fileHandler = RotatingFileHandler(
    BASE_DIR / 'app.log',
    maxBytes=10000,
    backupCount=3,
    encoding='utf-8'
)

fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
