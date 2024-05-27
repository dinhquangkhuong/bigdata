include .env

clean:
	rm -rf src/consumer/__pycache__/
	rm -rf src/producer/__pycache__/
	rm -rf university_subject_code/*
	rm -rf data*/*

activate venv:
	. venv/bin/activate


