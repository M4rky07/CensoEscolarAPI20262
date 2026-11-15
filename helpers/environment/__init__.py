import os
from pathlib import Path
from dotenv import load_dotenv

# Localiza a raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Carrega as variáveis de ambiente
load_dotenv(BASE_DIR / ".env")

# Disponibiliza as variáveis
environment = os.environ