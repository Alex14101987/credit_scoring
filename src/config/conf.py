import os
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DATA_FULL_PATH = "C:\\Program Files\\PostgreSQL\\14\\data\\"
DATABASE_NAME = 'home_credit'
DB_ARGS = {
    'database': DATABASE_NAME,
    'host': '127.0.0.1',
    'user': DB_USER,
    'password': DB_PASSWORD,
    'port': '5433'}
