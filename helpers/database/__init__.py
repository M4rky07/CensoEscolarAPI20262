import sqlite3

DATABASE = 'censoescolar.db'


def get_connection():
    conn = sqlite3.connect(DATABASE)
    return conn
