
import psycopg2
from psycopg2.extras import RealDictCursor

from helpers.environment import environment


def get_connection():
    return psycopg2.connect(
        host=environment.get("DB_HOST"),
        port=environment.get("DB_PORT"),
        dbname=environment.get("DB_NAME"),
        user=environment.get("DB_USER"),
        password=environment.get("DB_PASSWORD"),
        cursor_factory=RealDictCursor
    )
