import os
import uvicorn

PORT = int(os.environ["PORT"])
DEV = int(os.environ.get("DEV", 0))

def start_app():
  reload = False
  if DEV:
    reload = True

  uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=reload)