import environment

from fastapi import FastAPI

app = FastAPI()

@app.get("/history")
async def get_history():
  return "hello computer!"

if __name__ == "__main__":
  environment.start_app()