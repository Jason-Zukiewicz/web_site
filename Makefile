.ONESHELL:


# BACKEND   --------------------------------------------------------------
.PHONY: setup_back
setup_back:
	cd back && \
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt && \
	FLASK_APP=src/main.py flask initdb


.PHONY: run_back
run_back:
	cd back && \
	. venv/bin/activate && \
	FLASK_APP=src/main.py flask run

.PHONY: rb
rb:
	make setup_back
	make run_back

# BACK - DOCKER  --------------------------------------------------------------

.PHONY: rbd
rbd:
	docker stop $$(docker ps -q)
	cd back && \
	docker build -t back .
	docker run -d -p 5000:5000 back
	

# FRONT --------------------------------------------------------------

.PHONY: setup_front
setup_front:
	cd front && npm install

.PHONY: run_front
run_front:
	cd front
	npm start

.PHONY: rf
rf:
	make setup_front
	make run_front

# FRONT - DOCKER ------------------------------------------------------
.PHONY: rfd
rfd:
	docker stop $$(docker ps -q)
	cd front && \
	docker build -t front .
	docker run -d -p 3000:3000 front

# CLEANER ------------------------------------------
.PHONY: clean clear
clean clear:
	cd back
	rm -rf venv/
	cd ..
	cd front
	rm -rf node_modules/


