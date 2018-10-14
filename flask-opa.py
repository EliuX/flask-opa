import requests


class OPAException(Exception):
    """Exception evaluating a request in OPA"""

    def __init__(self, message):
        super().__init__(message)


class OPAUnexpectedException(Exception):
    """Unexpected error evaluating the request in OPA"""

    def __init__(self, message='Unexpected error'):
        super().__init__(message)


class AccessDeniedException(OPAException):
    """OPA Denied the request"""

    def __init__(self, message='Denied'):
        super().__init__(message)


class OPA(object):
    def __init__(self, app, input_function, deny_on_opa_fail=True):
        self.app = app
        self._input_function = input_function
        self.deny_on_opa_fail = deny_on_opa_fail

    def init_app(self, app):
        app.config.setdefault('OPA_URL', 'http://localhost:8181')
        self.app.before_request(self.check_authorization)

    def check_authorization(self):
        input = self.input
        url = self.url
        self.app.logger.debug("OPA query: %s. content: %s", url, input)
        response = requests.post(url, data=input)
        self.check_opa_response(response)

    def check_opa_response(self, response):
        try:
            if response.status_code != 200:
                opa_error = "OPA status code: %s. content: %s", \
                            response.status_code, response.json()
                self.app.logger.error(opa_error)
                raise OPAUnexpectedException(opa_error)

            allowed = response.json()
            self.app.logger.debug("OPA result: %s", allowed)
            if not allowed:
                raise AccessDeniedException()
        except OPAException as e:
            if self.deny_on_opa_fail:
                raise e

    def input(self):
        return self.input_function()

    @property
    def input_function(self):
        return self._input_function

    @input_function.setter
    def input_function(self, f):
        self._input_function = f

    @property
    def url(self):
        return self.app.config.get('OPA_URL')

    @url.setter
    def input(self, url):
        self.app.config.set('OPA_URL', url)
        self.app.logger.debug("OPA url changed to: %s", url)
