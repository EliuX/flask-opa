Check the code
================

## Run the tests
For running the tests with Py.test execute
```bash
pytest -v
```

## Check the coverage
The intended code coverage is of about 85%
```bash
coverage run -m pytest -v
```

## Check if the code is PEP compliant
```bash
flake8 --ignore=F811 flask_opa.py
```
Using ``--ignore=F811`` ignores unused static methods
