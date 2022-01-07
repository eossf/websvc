from logging import NullHandler
import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

@app.get("/")
def root():
    return {"message": "Helloworld"}

@app.get("/user")
def user():
    return {"userId": 1,"id": 1,"title": "delectus aut autem","completed": False }

@app.get("/info")
def info():
    return {
  "array": [
    1,
    2,
    3
  ],
  "boolean": True,
  "color": "gold",
  "null": "",
  "number": 123,
  "object": {
    "a": "b",
    "c": "d"
  },
  "string": "Hello World"
}

if __name__ == "__main__":
    uvicorn.run('main:app', host=os.getenv("API_HOST", "127.0.0.1"), port=os.getenv("API_PORT", 8000), reload=True, debug=True)