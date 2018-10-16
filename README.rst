Flask-OPA
=========
Simple to use `Flask <http://flask.pocoo.org/>`_ extension that lets you use
`Open Policy Agent <https://www.openpolicyagent.org>`_ in your project.


How to run the application
---------------------------
If you want to try a demo check the code in `examples`, but for development:

Run OPA in server mode
'''''''''''''''''''''''

#. Check the `latest OPA release <https://github.com/open-policy-agent/opa/releases>`_ and download it.
#. Put the binary file in the path of your system
#. Allow its execution with something like
#. Run opa in server mode with the sample policies

   .. code-block:: bash

      cd examples
      opa run -s -w data.json app.rego

  * ``-s`` is to run it in server mode instead of opening the REPL
  * ``-w`` is for watching the changes of the data/policy files

Specify configuration variables
'''''''''''''''''''''''''''''''''''''''''''''
* ``OPA_URL`` url string that specifies the OPA url to evaluate your input. It includes the path of the policy. E.g
http://localhost:8181/v1/data/examples/allow.

* ``OPA_SECURED`` boolean to specify if OPA will be enabled to your application.

See more at the `rest api reference <https://www.openpolicyagent.org/docs/rest-api.html>`_

Bind the OPA class to your Flask application
'''''''''''''''''''''''''''''''''''''''''''''
Its easy to bind the Flask-OPA library to your application. Just follow the following steps:

#. Create the OPA instance

   .. code-block:: python

      app = Flask(__name__)
      app.config.from_pyfile('app.cfg')
      opa = OPA(app, parse_input)

   Lets see the parameters that we passed to the OPA class:

   * ``parse_input`` (Required) contains a method that returns the input data json to be evaluated by the policy, e.g.:

   .. code-block:: python

        {
            "input": {
              "method": "GET",
              "path": ["data", "jon"],
              "user": "paul"
            }
        }

   * ``url`` (Optional) to use an specific url instead of the ``OPA_URL`` optionally specified in the app configuration.
   * ``allow_function`` (Optional) predicate that determinate if the response from OPA allows (True) or denies (False) the request


If you want enforce the OPA security in your application you can create the OPA instance like this:

   .. code-block:: python

        opa = OPA.secured(app, parse_input, url="http://localhost:8181/v1/data/package_name/allow")

or

   .. code-block:: python

        opa = OPA(app, parse_input, url="http://localhost:8181/v1/data/package_name/allow").secured()

otherwise OPA will enforce your security only if ``OPA_SECURED`` is `True`.

#. Specify the logging level to `DEBUG` if you want to get access to Flask-OPA logs of its operations using

   .. code-block:: python

      app.logger.setLevel(logging.DEBUG)

#. Run your Flask application.

Status
------
Pre-release or Beta: The project has gone through multiple rounds of active development with a goal of reaching
a stable release version, but is not there yet.

Path of Development: Active (October 2nd 2018)

Author
------
Eliecer Hernandez - `eliecerhdz@gmail.com <mailto:eliecerhdz@gmail.com>`_. To know more of me please visit
my `website <http://eliux.github.io>`_.

License
-------
This project is licensed under the MIT License - see the `LICENSE.md <LICENSE.md>`_ file for details.


