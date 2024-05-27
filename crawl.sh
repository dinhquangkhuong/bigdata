#!/bin/sh

rm -f university_subject_code/*
python src/webscrap

cat university_subject_code/* > university_subject_code.csv


