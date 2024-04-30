include .env

db:
	$(PYTHON) database

producer:
	$(PYTHON) src/producer
consumer:
	$(PYTHON) src/consumer 

clean:
	rm -rf src/consumer/__pycache__/
	rm -rf src/producer/__pycache__/

