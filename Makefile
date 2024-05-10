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


webuni:
	rm -f university_data/*
	rm -f university_subject_code/*
	rm -f university_subject/*
	python src/uni

