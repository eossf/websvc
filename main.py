import os
import sys
import logging
from logging import Logger, NullHandler, log
from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles
from uvicorn.config import LOGGING_CONFIG
from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger
from loguru import logger


LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False
WORKERS = int(os.environ.get("GUNICORN_WORKERS", "5"))


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


@app.get("/env/")
def env():
  async def read_item(key: str = ""):
    logging.Logger.info("env")
    print("test")
    return os.getenv(key)


def run():
  intercept_handler = InterceptHandler()
  # logging.basicConfig(handlers=[intercept_handler], level=LOG_LEVEL)
  # logging.root.handlers = [intercept_handler]
  logging.root.setLevel(LOG_LEVEL)

  seen = set()
  for name in [
      *logging.root.manager.loggerDict.keys(),
      "gunicorn",
      "gunicorn.access",
      "gunicorn.error",
      "uvicorn",
      "uvicorn.access",
      "uvicorn.error",
  ]:
      if name not in seen:
          seen.add(name.split(".")[0])
          logging.getLogger(name).handlers = [intercept_handler]

  logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])

  options = {
      "bind": "0.0.0.0",
      "workers": WORKERS,
      "accesslog": "-",
      "errorlog": "-",
      "worker_class": "uvicorn.workers.UvicornWorker",
      "logger_class": StubbedGunicornLogger
  }

  StandaloneApplication(app, options).run()


if __name__ == "__main__":
  run()


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_logger.setLevel(LOG_LEVEL)
        self.access_logger.setLevel(LOG_LEVEL)


class StandaloneApplication(BaseApplication):
    """Our Gunicorn application."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
