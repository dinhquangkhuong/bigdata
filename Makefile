PYTHON=python3

initdb:
	$(PYTHON) database

producers:
	$(PYTHON) producer/producer_runner.py

consumers:
	$(PYTHON) consumer/consumer_runner.py

containers:
	docker-compose up

clean:
	docker-compose down

