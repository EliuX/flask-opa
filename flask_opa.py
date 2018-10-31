"""
Flask Extension for OPA
"""

import requests
from flask.app import Flask

__version__ = "0.5-beta"


class OPAException(Exception):
    """Exception evaluating a request in OPA"""

    def __init__(self, message):
        super().__init__(message)


class OPAUnexpectedException(OPAException):
    """Unexpected error evaluating the request in OPA"""

    def __init__(self, message='Unexpected error'):
        super().__init__(message)


class AccessDeniedException(OPAException):
    """OPA Denied the request"""

    def __init__(self, message='Denied'):
        super().__init__(message)


class OPA(object):
    def __init__(self,
                 app: Flask,
                 input_function,
                 url: str = None,
                 allow_function=None):
        super(OPA, self).__init__()
        self._app = app
        self._pep = {}
        self._input_function = input_function
        self._allow_function = allow_function or self.default_allow_function
        self._deny_on_opa_fail = app.config.get('OPA_DENY_ON_FAIL', True)
        self._url = url or app.config.get('OPA_URL')
        if self._app.config.get('OPA_SECURED', False):
            self.secured()

    @staticmethod
    def secure(*args, **kwargs):
        return OPA(*args, **kwargs).secured()

    def secured(self,
                url=None,
                input_function=None,
                allow_function=None):
        """Secure app"""
        if self.check_authorization not in self._app.before_request_funcs:
            self._url = url or self._url
            self._allow_function = allow_function or self._allow_function
            self._input_function = input_function or self._input_function
            if self._url and self._input_function and self._allow_function:
                self._app.before_request(self.check_authorization)
            else:
                raise ValueError("Invalid OPA configuration")
        return self

    def check_authorization(self):
        input = self.input
        url = self.url
        self._app.logger.debug("%s, OPA query: %s. content: %s",
                               self.app, url, input)
        response = requests.post(url, json=input)
        try:
            self.check_opa_response(response)
        except OPAException as e:
            if self.deny_on_opa_fail:
                raise e

    def check_opa_response(self, response):
        if response.status_code != 200:
            opa_error = "OPA status code: {}. content: {}".format(
                response.status_code, str(response)
            )
            self._app.logger.error(opa_error)
            raise OPAUnexpectedException(opa_error)
        resp_json = response.json()
        self._app.logger.debug("OPA result: %s", resp_json)
        if not self.allow_function(resp_json):
            raise AccessDeniedException()
        return resp_json

    def __call__(self, name: str, url: str,
                 input_function=None,
                 allow_function=None):
        """Creates a PEP"""
        return PEP(self, name, url, input_function, allow_function)

    @property
    def pep(self):
        return self._pep

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def deny_on_opa_fail(self):
        return self._deny_on_opa_fail

    @property
    def input(self):
        return self.input_function()

    @property
    def input_function(self):
        return self._input_function

    @property
    def allow_function(self):
        return self._allow_function

    @property
    def app(self):
        return self._app

    @classmethod
    def default_allow_function(cls, response_json):
        return response_json.get('result', False)


class PEP(OPA):
    """Class to handle Policy Enforcement Points"""

    def __init__(self,
                 opa: OPA,
                 name: str,
                 url: str,
                 input_function=None,
                 allow_function=None,
                 deny_on_opa_fail: bool = False):
        self._app = opa.app
        opa.pep[name] = self
        self._url = url
        self._input_function = input_function or opa.input_function
        self._allow_function = allow_function or opa.allow_function
        self._deny_on_opa_fail = deny_on_opa_fail or False
        self._name = name or "PEP"
        if not (self._app and self._url and
                self._input_function and self._allow_function):
            raise ValueError("Invalid Police Enforcement Point configuration")

    def check_authorization(self, *args, **kwargs):
        _input = self.input(*args, **kwargs)
        _url = self.url
        self._app.logger.debug("%s query: %s. content: %s", self, _url, _input)
        response = requests.post(_url, json=_input)
        self.check_opa_response(response)

    def __call__(self, f):
        def secure_function(*args, **kwargs):
            try:
                self.check_authorization(*args, **kwargs)
                return f(*args, **kwargs)
            except OPAException as e:
                if self.deny_on_opa_fail:
                    raise e

        return secure_function

    def input(self, *args, **kwargs):
        return self._input_function(*args, **kwargs)

    @property
    def deny_on_opa_fail(self):
        return self._deny_on_opa_fail

    def __str__(self):
        return "<{}>".format(self._name)
