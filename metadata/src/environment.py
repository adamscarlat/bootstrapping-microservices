import os
import uvicorn

PORT = int(os.environ["PORT"])

DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

RABBIT_USER = os.environ["RABBIT_USER"]
RABBIT_PASSWORD = os.environ["RABBIT_PASSWORD"]
RABBIT_HOST = os.environ["RABBIT_HOST"]
RABBIT_PORT = int(os.environ["RABBIT_PORT"])

DEV = int(os.environ.get("DEV", 0))

def start_app():
  reload = False
  if DEV:
    reload = True

  uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=reload)