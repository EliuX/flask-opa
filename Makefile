# Made by EliuX for OPA-Flask.

demo:
	nohup opa run -s -w examples &
	export FLASK_ENV=development
	export FLASK_APP=examples/app.py
	flask run

lint:
	flake8 flask_opa.py --count

coverage:
	coverage erase
	coverage run -m pytest -v
