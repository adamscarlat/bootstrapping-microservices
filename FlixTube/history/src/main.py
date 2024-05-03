import environment

from fastapi import FastAPI


app = FastAPI()

@app.get("/history")
async def get_history():
  return "hello"


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=environment.PORT)