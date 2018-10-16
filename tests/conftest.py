"""
Fixtures
"""

import pytest
from flask import json
from flask.app import Flask, request

from flask_opa import OPA, OPAException


def parse_input():
    return {
        "input": {
            "method": request.method,
            "path": request.path.strip().split("/")[1:],
            "user": request.headers.get("Authorization", ""),
        }
    }


@pytest.fixture
def app():
    """Import the test app"""
    app = Flask(__name__)
    app.config["OPA_SECURED"] = True
    app.config["OPA_URL"] = 'http://localhost:8181/v1/data/examples/allow'
    opa = OPA(app, input_function=parse_input).secured()
    init_app(app)
    return app


@pytest.fixture
def app_with_missing_url():
    app = Flask(__name__)
    OPA(app, input_function=parse_input)
    init_app(app)
    return app

@pytest.fixture
def app_secured_from_configuration():
    app = Flask(__name__)
    app.config["OPA_SECURED"] = True
    app.config["OPA_URL"] = 'http://localhost:8181/v1/data/examples/allow'
    OPA(app, input_function=parse_input)
    init_app(app)
    return app


def init_app(app):
    @app.route("/")
    def welcome_page():
        return "Test Home page"

    @app.errorhandler(OPAException)
    def handle_opa_exception(e):
        return json.dumps({
            "message": str(e)
        }), 403

