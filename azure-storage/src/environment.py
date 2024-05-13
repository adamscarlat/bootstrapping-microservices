import os
import uvicorn

PORT = int(os.environ["PORT"])

STORAGE_ACCOUNT_NAME = os.environ["STORAGE_ACCOUNT_NAME"]
STORAGE_ACCESS_KEY = os.environ["STORAGE_ACCESS_KEY"]

DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

DEV = int(os.environ.get("DEV", 0))


def start_app():
  reload = False
  if DEV:
    reload = True

  uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=reload)