"""
Fixtures
"""
import json

import pytest
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


DATABASE_POLICIES_URL = 'http://localhost:8181/v1/data/examples/db/allow'


@pytest.fixture
def app():
    """Import the test app"""
    app = Flask(__name__)
    app.config["OPA_SECURED"] = True
    app.config["OPA_URL"] = 'http://localhost:8181/v1/data/examples/allow'
    app.opa = OPA(app, input_function=parse_input).secured()
    init_app(app)
    return app


@pytest.fixture
def app_with_missing_url():
    app = Flask(__name__)
    app.opa = OPA(app, input_function=parse_input)
    init_app(app)
    return app


@pytest.fixture
def app_secured_from_configuration():
    app = Flask(__name__)
    app.config["OPA_SECURED"] = True
    app.config["OPA_URL"] = 'http://localhost:8181/v1/data/examples/allow'
    app.opa = OPA(app, input_function=parse_input)
    init_app(app)
    return app

@pytest.fixture
def app_using_pep(app):
    init_pep(app)
    return app

def init_app(app):
    @app.route("/")
    def welcome_page():
        return "Test Home page"

    @app.errorhandler(OPAException)
    def handle_opa_exception(e):
        return json.dumps({"message": str(e)}), 403


def init_pep(app):
    def input_function_search_pep(*args, **kwargs):
        input = parse_input()
        input["text"] = kwargs.get("text") or args[0]
        return input

    secured_query = app.opa("Database PEP",
                            DATABASE_POLICIES_URL,
                            input_function_search_pep)

    @secured_query
    def query_data(text):
        return ["%s at the beginning" % text,
                "The word %s in the middle" % text,
                "In the end %s" % text]

    @app.route("/search")
    def search_page():
        result = query_data(text=request.args.get('q'))
        return json.dumps({"result": result}), 200
