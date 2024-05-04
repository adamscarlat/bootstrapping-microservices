import os
import uvicorn

PORT = int(os.environ["PORT"])

DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

VIDEO_STORAGE_HOST = os.environ["VIDEO_STORAGE_HOST"]
VIDEO_STORAGE_PORT = int(os.environ["VIDEO_STORAGE_PORT"])
HISTORY_HOST = os.environ["HISTORY_HOST"]
HISTORY_PORT = int(os.environ["HISTORY_PORT"])

DEV = int(os.environ.get("DEV", 0))

def start_app():
  reload = False
  if DEV:
    reload = True

  uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=reload)