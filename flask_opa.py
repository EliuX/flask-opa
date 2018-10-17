"""
Flask Extension for OPA
"""
import requests
from flask.app import Flask

__version__ = "0.3"


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
                 input_function: 'function',
                 url: str = None,
                 allow_function: 'function' = None):
        self.app = app
        self._input_function = input_function
        self._allow_function = allow_function or self.default_allow_function
        self._deny_on_opa_fail = app.config.get('OPA_DENY_ON_FAIL', True)
        self._url = url or app.config.get('OPA_URL')
        if self.app.config.get('OPA_SECURED', False):
            self.secured()

    @staticmethod
    def secured(app: Flask, **kwargs):
        return OPA(app, kwargs).secured()

    def secured(self, url=None, input_function=None, allow_function=None):
        self._url = url or self._url
        self._allow_function = allow_function or self._allow_function
        self._input_function = input_function or self._input_function
        if self._url and self._input_function and self._allow_function:
            self.app.before_request(self.check_authorization)
        else:
            raise ValueError("Invalid OPA configuration")
        return self

    def check_authorization(self):
        input = self.input
        url = self.url
        self.app.logger.debug("OPA query: %s. content: %s", url, input)
        response = requests.post(url, json=input)
        self.check_opa_response(response)

    def check_opa_response(self, response):
        try:
            if response.status_code != 200:
                opa_error = "OPA status code: {}. content: {}".format(
                    response.status_code, str(response)
                )
                self.app.logger.error(opa_error)
                raise OPAUnexpectedException(opa_error)

            resp_json = response.json()
            self.app.logger.debug("OPA result: %s", resp_json)
            if not self.allow_function(resp_json):
                raise AccessDeniedException()
        except OPAException as e:
            if self._deny_on_opa_fail:
                raise e

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
        self.app.logger.debug("OPA URL changed to: %s", url)

    @property
    def input(self):
        return self.input_function()

    @property
    def input_function(self):
        return self._input_function

    @input_function.setter
    def input_function(self, f):
        self._input_function = f

    @property
    def allow_function(self):
        return self._allow_function

    @allow_function.setter
    def allow_function(self, new_allow_function):
        self._allow_function = new_allow_function

    @classmethod
    def default_allow_function(cls, response_json):
        return response_json.get('result', False)
