import sentry_sdk
import os
import bottle
import logging
import random

from bottle import Bottle, run, route
from sentry_sdk.integrations.bottle import BottleIntegration

sentry_sdk.init(
    dsn="https://cf6b57958b774f2bbe767f0f994f1a25@o381199.ingest.sentry.io/5208144",
    integrations=[BottleIntegration()]
)

app = Bottle()

@app.route("/")
def hello():
    html = """
        <!doctype html>
        <html lang="en">
          <head>
            <title>Стартовая страница</title>
          </head>
          <body>
            <div class="container">
              <h1>Hello, world!</h1>
            </div>
          </body>
        </html>
        """
    return html


@app.route("/success")
def index():
    html = """
    <!doctype html>
    <html lang="en">
      <head>
        <title> страница</title>
      </head>
      <body>
        <div class="container">
          <h1>all is well</h1>
        </div>
      </body>
    </html>
    """
    return html


@app.route("/fail")

def generate_fails():
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    logger = logging.getLogger("my-logger")
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    info_handler = logging.StreamHandler()
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    class MyFilter:

        def filter(self, logRecord):
            return logRecord.levelno == logging.INFO

    info_handler.addFilter(MyFilter())
    logger.addHandler(stream_handler)
    logger.addHandler(info_handler)

    levels = ['debug', 'info', 'warning', 'error', 'critical']

    for _ in range(10):
        level = random.choice(levels)
        eval('logger.{level}("тестовое сообщение уровня {level}")'.format(level=level))
        if level=='debug':
            raise Exception('Вам нужно проверить приложение на ошибки')

        elif level=='info':
            raise AttributeError('Это просто полезная информация')

        elif level== 'warning':
            raise TypeError('Предупреждение: в дальнейшем в приложении может возникнуть ошибка!')

        elif level=='error':
            raise RuntimeError('Ошибка!')

        else:
            raise RuntimeError('Критическая ошибка! Работа приложения остановлена!')



if os.environ.get("APP_LOCATION") == "heroku":
    run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="waitress",
        workers=3,
    )
else:
    app.run(host="localhost", port=8090, debug=True)



