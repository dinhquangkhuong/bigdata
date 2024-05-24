#!/usr/bin/env spark-submit --jars /home/khuong/.local/opt/java-jar/postgresql-jdbc.jar

from pyspark.sql import Row, SparkSession
from pyspark.sql.dataframe import DataFrame
import json
from unidecode import unidecode

jdbc_url = "jdbc:postgresql://localhost:5432/bigdata?ssl=true&sslmode=require&user=khuong&password=123456789"

spark: SparkSession = SparkSession.builder \
  .master("local") \
  .appName("test") \
  .config("spark.jars", "/home/khuong/.local/opt/java-jar/postgresql-jdbc.jar") \
  .config("spark.sql.warehouse.dir", "/user/khuong") \
  .getOrCreate()

df: DataFrame = spark.read \
  .format("jdbc") \
  .option("url", jdbc_url) \
  .option("driver", "org.postgresql.Driver") \
  .option("user", "khuong") \
  .option("password", "123456789") \
  .option("query", "select * from university_subject_code") \
  .load()

# df: DataFrame = spark.read \
#   .format("jdbc") \
#   .option("url", jdbc_url) \
#   .option("driver", "org.postgresql.Driver") \
#   .option("user", "khuong") \
#   .option("password", "123456789") \
#   .option("query", "select * from university_subject_code") \
#   .load()

# student = {
#   'geography': 5,
#   'civic_education': 5,
#   'chemistry': 5,
#   'physics': 5,
#   'foreign_language_type': 5,
#   'foreign_language': 5,
#   'biology': 5,
#   'history': 5,
#   'math': 5,
#   'literature': 5,
#   'student_id': 5,
#   'english': 5,
# }
#
# choose_sub = [ 'geography', 'civic_education', 'chemistry' ]
#
# convert = {
#   'sinh hoc': 'biology',
#   'hoa': 'chemistry',
#   'giao duc cong': 'civic_education',
#   'tieng duc': 'foreign_language',
#   'tieng nhat': 'foreign_language',
#   'dia li': 'geography',
#   'hoa hoc': 'chemistry',
#   'anh': 'english',
#   'dia': 'geography',
#   'sinh': 'biology',
#   'tieng nga': 'foreign_language',
#   'lich su': 'history',
#   'vat li': 'physics',
#   'toan': 'math',
#   'tieng anh': 'foreign_language',
#   'tieng trung': 'foreign_language',
#   'ngu van': 'literature',
#   'tieng phap': 'foreign_language',
#   'giao duc cong dan': 'civic_education',
#   'van': 'literature'
# }
#
# rdd = df.rdd
#
# def parseRow(row: Row):
#   subject_raw: str = row['subject_raw']
#   subject_raw = subject_raw.replace("'", "\"")
#
#   subjects = list(map(lambda raw: (
#     row['university_id'],
#     row['university'],
#     row['subject_code'],
#     row['year'],
#     raw['code']
#   ), json.loads(subject_raw))) 
#   return subjects
#
# subjects = rdd.map(parseRow).flatMap(lambda v: v)
#
# df = spark.createDataFrame(subjects, schema=["university_id", "university", "subject_code", "year", "code"])
#
# # df.write.jdbc(jdbc_url, "uni_sub_code")
# df.write.csv("./nothello")

# print(subjects)

# subjects_code = subjects.distinct().collect()
#
# map(lambda val: val[1][1].split(","), subjects_code)
# array = []
# for value in subjects_code:
#   sub = value[0][1].split(", ")
#   for val in sub:
#     array.insert(0, unidecode(val.lower()))
#
# for a in list(set(array)):
#   print(a)

# file = open("helo.csv", 'w')
# print("code",  "first",  "second", "third", "fouth", sep=", ", file=file)
# for value in subjects_code:
#   print(value[1][1], ", ", value[0][1], sep="", file=file)
#
# file.flush()
# file.close()
#
