.ONESHELL:

.PHONY: setup_backend
setup_back:
	cd back && \
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt && \
	FLASK_APP=src/main.py flask initdb

.PHONY: run_backend
run_back:
	cd back && \
	. venv/bin/activate && \
	FLASK_APP=src/main.py flask run



