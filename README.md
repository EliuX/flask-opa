Flask-OPA
=========
[![Build Status](https://travis-ci.com/EliuX/flask-opa.svg?branch=master)](https://travis-ci.com/EliuX/flask-opa)
[![codecov](https://codecov.io/gh/EliuX/flask-opa/branch/master/graph/badge.svg)](https://codecov.io/gh/EliuX/flask-opa)
[![PyPI Version](http://img.shields.io/pypi/v/Flask-OPA.svg)](https://pypi.python.org/pypi/Flask-OPA)

Simple to use [Flask](http://flask.pocoo.org/>) extension that lets you secure your projects with
[Open Policy Agent](https://www.openpolicyagent.org). It allows 
* HTTP API Authorization
* Policy Enforcement Point (AOP using decorators on methods)

## Quick start 

Its recommended for you to try the app in the package `examples`. Thanks to the `Makefile` you can run the demo project 
with the following command

```bash
 make demo   
```

### How it works?

For a better understanding of what `make demo` does and how you should setup `flask_opa` in your project, follow the 
next steps:

1. Run OPA in server mode

    * Check the [latest OPA release](https://github.com/open-policy-agent/opa/releases) and download it.
    * Put the binary file in the path of your system
    * Allow its execution with something like `chmod 755 ./opa`
    * Run opa in server mode with the sample policies
    
    ```bash 
    opa run -s -w examples
    ```
    
      - `-s` is to run it in server mode instead of opening the REPL
      - `-w` is for watching the changes of the data/policy files

1. Specify configuration variables

    * `OPA_URL` url accessible in your running OPA server, used to evaluate your input. It includes the path of the 
     policy, e.g. `http://localhost:8181/v1/data/examples/allow`.
    
    * `OPA_SECURED` boolean to specify if OPA will be enabled to your application.
    
    See more at the [rest api reference](https://www.openpolicyagent.org/docs/rest-api.html)

1. Bind the OPA class to your Flask application

    Its easy to bind the Flask-OPA library to your application. Just follow the following steps:

1. Create the OPA instance

    ```python
    app = Flask(__name__)
    app.config.from_pyfile('app.cfg')
    opa = OPA(app, parse_input)
    ```

    Lets see the parameters that we passed to the OPA class:
    
    - `parse_input` (Required) contains a method that returns the input data json to be evaluated by the policy, e.g.:

    ```json
    {
        "input": {
          "method": "GET",
          "path": ["data", "jon"],
          "user": "paul"
        }
    }
    ```
    
    - `url` (Optional) to use an specific url instead of the `OPA_URL` optionally specified in the app configuration.
    - `allow_function` (Optional) predicate that determinate if the response from OPA allows (True) or denies (False) the request
    
    If you want enforce the OPA security in your application you can create the OPA instance like this:
    
    ```python
    opa = OPA.secure(app, parse_input, url="http://localhost:8181/v1/data/package_name/allow")
    ```
    
    or
    
    ```python
    opa = OPA(app, parse_input, url="http://localhost:8181/v1/data/package_name/allow").secured()
    ```
    
    otherwise OPA will enforce your security only if ``OPA_SECURED`` is `True`.
    
    Specify the logging level to `DEBUG` if you want to get access to Flask-OPA logs of its operations using
    
    ```python
    app.logger.setLevel(logging.DEBUG)
    ```

1. Run your Flask application.
    
## Policy Enforcement point
One of the features this module provides is [Policy Enforcement Point][PEP] which basically allows you to ensure policies
at any method of your application.
For practical purposes, lets imagine a sample method that is in charge of logging content related to actions done by 
users. In this case we must create a different input functions that provide useful information for certain policies that 
will decide if a log should be sent or not to a remote server. Lets suppose that such logging method is something like:

```python
def log_remotely(content):
    # Imagine a code to log this remotely
    app.logger.info("Logged remotely: %s", content)
```

to decorate it we will create a [PEP][PEP] decorator using our `OPA` instance as a function (callable mode). 
The parameters are pretty much the same as those used to secure the application. The resulting instance will decorate 
our function of interest:

```python
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
    # Imagine a code to log content remotely
    app.logger.info("Logged remotely: %s", content)
```

As you might have noticed, the only new thing we truly require for adding the [PEP][PEP] is a new input function. This 
function can provide a more versatile input than the one used by the `OPA` instance created for the whole app: in our 
example it provides data related to the user request and data provided by the parameters of the decorated function as 
well.

Read the [examples README](examples/README.md) for more detailed information about how to run a demo.

## Status

Pre-release or Beta: The project has gone through multiple rounds of active development with a goal of reaching
a stable release version, but is not there yet.

Path of Development: Active (October 31th 2018)

## Author

Eliecer Hernandez Garbey

### Links

- Main website: [EliuX Overflow](http://eliux.github.io)
- Twitter: [@eliux_black](https://twitter.com/eliux_black)
- LinkedIn: [eliecer-hernández-garbey-16172686](https://www.linkedin.com/in/eliecer-hern%C3%A1ndez-garbey-16172686/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.


[PEP]: https://tools.ietf.org/html/rfc2904#section-4.4
