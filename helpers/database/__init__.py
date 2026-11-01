
import sqlite3
from pathlib import Path

# Localiza a pasta raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Caminho do banco de dados
DATABASE = BASE_DIR / "censo_escolar.db"


def get_connection():

    if not DATABASE.exists():
        raise FileNotFoundError(
            f"Banco de dados não encontrado: {DATABASE}"
        )

    connection = sqlite3.connect(DATABASE)

    # Permite acessar os resultados como dicionários
    connection.row_factory = sqlite3.Row

    return connection
