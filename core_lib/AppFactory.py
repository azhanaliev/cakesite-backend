import logging
import logging.handlers

from flask import Flask

import configuration

__author__ = 'Azamatshekin'


def create_app(name, logger_name='daily.log', test=False):
    if not test:
        try:
            logging.basicConfig(level=logging.INFO,
                                format="%(threadName)s %(asctime)s %(name)-12s %(message)s",
                                datefmt="%d-%m-%y %H:%M")

            daily = logging.handlers.TimedRotatingFileHandler("log/" + logger_name, when="midnight", interval=1,
                                                              backupCount=15,
                                                              encoding="utf-8")
            logging.getLogger().addHandler(daily)
            fmt = logging.Formatter('%(asctime)s %(name)-12s %(message)s')
            daily.setFormatter(fmt)
            if configuration.DEBUG:
                daily.setLevel(logging.DEBUG)
            else:
                daily.setLevel(logging.INFO)
        except:
            pass

    app = Flask(name)
    return app
