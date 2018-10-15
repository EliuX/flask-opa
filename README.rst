Flask-OPA
=========
Simple to use `Flask <http://flask.pocoo.org/>`_ extension that lets you use
`Open Policy Agent <https://www.openpolicyagent.org>`_ in your project.


How to run the application
------------------
If you want to try a demo check the code in `examples`, but for development:
Run OPA in server mode
'''''''''''''''''''''''
1. Check the `latest OPA release <https://github.com/open-policy-agent/opa/releases>`_ and download it.
2. Put the binary file in the path of your system
3. Allow its execution with something like
    chmod 755 ~/opa
3. Run opa in server mode with the sample policies
    cd examples
    opa run -s data.json app.rego

Bind the OPA class to your Flask application
'''''''''''''''''''''''''''''''''''''''''''''
Its easy to bind the Flask-OPA library to your application. Just follow the following steps:
1. Create the OPA class specifying the wanted parameters
    app = Flask(__name__)
    opa = OPA(app, parse_input, url="http://localhost:8181/v1/data/package_name/allow")
    opa.init_app(app)

    - `parse_input` url is basically is a function that returns a json with among other things
      an `input` entry which has the data the policy needs to its evaluation.
    - The url must contain that method or property to be evaluated. E.g. `allow` will just return
      a `true` or `false` to specify if the access your be or not granted.

2. Specify the logging level to `DEBUG` if you want to get access to Flask-OPA logs of its operations
    app.logger.setLevel(logging.DEBUG)

3. Run your application





