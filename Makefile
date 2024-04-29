PYTHON=python3

db:
	$(PYTHON) database

producer:
	$(PYTHON) producer/producer_runner.py

consumer:
	$(PYTHON) consumer/consumer_runner.py

clean:
	rm -rf consumer/__pycache__/
	rm -rf producer/__pycache__/
	rm -rf __pycache__/

