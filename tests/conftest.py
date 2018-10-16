"""
Fixtures
"""

import pytest
from flask.app import Flask

from examples.app import parse_input, app as sample_app
from flask_opa import OPA


@pytest.fixture
def app():
    """Import the test app"""
    return sample_app


@pytest.fixture
def app_with_missing_url():
    app = Flask(__name__)
    OPA(app, input_function=parse_input)
    return app

@pytest.fixture
def app_secured_from_configuration():
    app = Flask(__name__)
    app.config["OPA_SECURED"] = True
    app.config["OPA_URL"] = 'http://localhost:8181/v1/data/examples/allow'
    OPA(app, input_function=parse_input)
    return app
