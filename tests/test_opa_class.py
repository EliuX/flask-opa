import pytest
import requests
import responses
from flask import json
from flask.app import Flask

from flask_opa import AccessDeniedException, OPA, OPAUnexpectedException, OPAServerUnavailableException
from tests.conftest import DATABASE_POLICIES_URL, parse_input, init_app


@responses.activate
def test_get_home_page_granted(app):
    opa_url = app.config.get('OPA_URL')
    responses.add(responses.POST, opa_url,
                  json={'result': True}, status=200)

    response = app.test_client().get('/')

    assert 0 < len(response.data)
    assert 200 == response.status_code


@responses.activate
def test_opa_grant_access(app):
    opa_url = app.config.get('OPA_URL')
    responses.add(responses.POST, opa_url, json={'result': True}, status=200)

    response = app.test_client().get('/')

    assert 0 < len(response.data)
    assert 200 == response.status_code


@responses.activate
def test_opa_create_with_staticmethod_deny_access():
    app = Flask(__name__)
    opa_url = 'http://localhost:8181/v1/data/dm/allow'
    app.opa = OPA.secure(app, input_function=parse_input, url=opa_url)
    init_app(app)

    responses.add(responses.POST, opa_url, json={'result': False}, status=200)

    response = app.test_client().get('/')

    assert 403 == response.status_code


@responses.activate
def test_opa_denies_access(app):
    opa_url = app.config.get('OPA_URL')
    responses.add(responses.POST, opa_url, json={'result': False}, status=200)

    response = app.test_client().post('/')

    assert 403 == response.status_code


@pytest.mark.xfail(raises=ValueError)
def test_app_with_missing_url(app_with_missing_url):
    pass


@responses.activate
@pytest.mark.xfail(raises=AccessDeniedException)
def test_app_secured_from_configuration_raises_access_denied(app_secured_from_configuration):
    opa_url = app_secured_from_configuration.config.get('OPA_URL')
    responses.add(responses.POST, opa_url, json={'result': False}, status=200)

    app_secured_from_configuration.test_client().post('/')


@responses.activate
def test_app_secured_with_pep_allow_access(app_using_pep):
    responses.add(responses.POST,
                  DATABASE_POLICIES_URL,
                  json={'result': True},
                  status=200)
    opa_url = app_using_pep.config.get('OPA_URL')
    responses.add(responses.POST, opa_url, json={'result': True}, status=200)

    response = app_using_pep.test_client().get('/search?q=lorem')

    assert 0 < len(response.data)
    assert 200 == response.status_code


@responses.activate
def test_when_pep_fails_and_deny_on_opa_fail_is_false_then_result_not_returned(app_using_pep):
    app_using_pep.opa.pep["Database PEP"]._deny_on_opa_fail = False

    opa_url = app_using_pep.config.get('OPA_URL')
    responses.add(responses.POST,
                  opa_url,
                  json={'result': True},
                  status=200)

    responses.add(responses.POST,
                  DATABASE_POLICIES_URL,
                  json={'result': False},
                  status=200)

    response = app_using_pep.test_client().get('/search?q=lorem')

    assert 200 == response.status_code
    assert json.loads(response.data).get("result", "") is None


@responses.activate
def test_when_pep_fails_and_deny_on_opa_fail_is_true_then_return_403(app_using_pep):
    app_using_pep.opa.pep["Database PEP"]._deny_on_opa_fail = True

    opa_url = app_using_pep.config.get('OPA_URL')
    responses.add(responses.POST,
                  opa_url,
                  json={'result': True},
                  status=200)

    responses.add(responses.POST,
                  DATABASE_POLICIES_URL,
                  json={'result': False},
                  status=200)

    response = app_using_pep.test_client().get('/search?q=lorem')

    assert 403 == response.status_code


def test_app_without_opa_input_function_raise_value_error(app):
    with pytest.raises(ValueError):
        app.config['OPA_SECURED'] = True
        app.config['OPA_URL'] = 'http://localhost:8181/v1/data/examples/allow'
        app.opa = OPA(app, input_function=None).secured()


def test_app_with_pep_with_no_url_raise_value_error(app):
    with pytest.raises(ValueError):
        app.opa('Database PEP', '')


@responses.activate
def test_change_app_opa_url(app):
    app.opa.url = app.config.get('OPA_URL')
    responses.add(responses.POST, app.opa.url,
                  json={'result': True}, status=200)

    response = app.test_client().get('/')

    assert 200 == response.status_code


@responses.activate
@pytest.mark.xfail(raises=OPAUnexpectedException)
def test_app_retrieves_non_ok_value_should_raise_error(app):
    app.opa.url = app.config.get('OPA_URL')

    responses.add(responses.POST, app.opa.url,
                  json={'result': True}, status=404)

    response = app.test_client().get('/')

    assert 403 == response.status_code


@responses.activate
def test_app_that_denies_on_fail_when_no_connection_then_deny_access(app):
    app.opa.deny_on_opa_fail = True
    app.opa.url = app.config.get('OPA_URL')

    error_when_opa_server_is_down = requests.exceptions.ConnectionError("OPA server down")
    responses.add(responses.POST, app.opa.url,
                  body=error_when_opa_server_is_down)

    response = app.test_client().get('/')

    assert 'OPA server down' == json.loads(response.data).get("message", "")
    assert 403 == response.status_code


def test_opa_with_pep_name(app_using_pep):
    pep = app_using_pep.opa.pep['Database PEP']

    assert "Database PEP" in str(pep)


def test_app_using_pep_that_doesnt_denies_on_fail_when_no_connection_then_grant_access(app_using_pep):
    app_using_pep.opa.deny_on_opa_fail = False
    app_using_pep.opa.pep["Database PEP"].deny_on_opa_fail = False

    response = app_using_pep.test_client().get('/')

    assert 200 == response.status_code
