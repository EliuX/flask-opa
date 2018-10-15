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
      opa run -s data.json app.rego


Bind the OPA class to your Flask application
'''''''''''''''''''''''''''''''''''''''''''''
Its easy to bind the Flask-OPA library to your application. Just follow the following steps:

#. Create the OPA class specifying the wanted parameters

   .. code-block:: python

      app = Flask(__name__)
      opa = OPA(app, parse_input, url="http://localhost:8181/v1/data/package_name/allow")
      opa.init_app(app)

   * ``parse_input`` url is basically is a function that returns a json with among other things
     an `input` entry which has the data the policy needs to its evaluation.
   * ``url must`` contain that method or property to be evaluated. E.g. `allow` will just return
     a `true` or `false` to specify if the access your be or not granted.

#. Specify the logging level to `DEBUG` if you want to get access to Flask-OPA logs of its operations using

   .. code-block:: python

      app.logger.setLevel(logging.DEBUG)

#. Run your application

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


