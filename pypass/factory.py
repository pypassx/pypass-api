# -*- coding: utf-8 -*-
"""
    factory
    ~~~~~~~

    This module includes the creating app and it's configuration

    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv2, see LICENSE for more details.
"""
import logging
import logging.handlers

from flask import Flask, jsonify

from .utils.logger import CtxFilter


def create_app(config):
    """
        Creates a flask app, and configure it's controllers,  logger and etc.
    :param config: config object
    :return:
    """
    app = Flask(config.NAME)

    configure_app(app, config)
    configure_logger(app)
    register_controllers(app)

    # TODO: register error handlers

    return app


def configure_app(app, config):
    """
        Configure the application using the config object
    :param app: the flask application
    :param config: the configuration object
    """
    if config is not None:
        app.config.from_object(config)
    app.config.from_envvar('project_CONFIG', silent=True)


def configure_logger(app):
    """
        Configures the logger and registers the logger handlers.
    :param app: the flask application
    """
    if app.config['DEBUG'] or app.config['TESTING']:
        return

    app.logger.addFilter(CtxFilter())
    formatter = logging.Formatter(app.config['LOG_FORMAT'])

    debug_file_handler = logging.handlers.TimedRotatingFileHandler(
        app.config['DEBUG_LOG'], when='D', backupCount=10)

    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    error_file_handler = logging.handlers.TimedRotatingFileHandler(
        app.config['ERROR_LOG'], when='D', backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)


def register_controllers(app):
    """
        Registers the controllers on the application.
    :param app: the flask application
    """
    for blueprint in app.config['ACTIVE_CONTROLLERS']:
        try:
            bp = __import__('pypass.controllers.{}'.format(blueprint),
                            fromlist=['controller'])
            app.register_blueprint(bp.controller)
        except ImportError:
            app.logger.warning("""could'nt register the "{}" controller due
            to an ImportError""".format(blueprint))
