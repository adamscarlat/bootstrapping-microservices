import os

PORT = int(os.environ["PORT"])

DBHOST = "localhost"
DBPORT = "4000"
DBNAME = os.environ["DBNAME"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DEV = int(os.environ.get("DEV", 0))