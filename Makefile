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
	rm -rf consumer/__pycache__/
	rm -rf producer/__pycache__/
	rm -rf __pycache__/
	docker-compose down

