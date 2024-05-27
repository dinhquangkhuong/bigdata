#!/bin/sh

python -m venv venv
. venv/bin/activate

pip install apache-superset pyspark pandas unidecode

mkdir university_subject_code

