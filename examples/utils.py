from flask.globals import request

from examples.app import app


def validate_logging_input_function(*arg, **kwargs):
    return {
        "input": {
            "user": request.headers.get("Authorization", ""),
            "content": arg[0]
        }
    }


secure_logging = app.opa("Logging PEP", app.config["OPA_URL_LOGGING"], validate_logging_input_function)


@secure_logging
def log_remotely(content):
    # Imagine a code to log this remotely
    app.logger.info("Logged remotely: %s", content)
