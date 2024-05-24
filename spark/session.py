from pyspark.sql import DataFrameReader, SparkSession
from pyspark.sql.dataframe import DataFrame

jdbc_url = "jdbc:postgresql://localhost:5432/bigdata?ssl=true&sslmode=require&user=khuong&password=123456789"

def query(spark: SparkSession, query: str) -> DataFrameReader:
  return spark.read \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("driver", "org.postgresql.Driver") \
    .option("query", query)


class BigdataSlim:
  spark: SparkSession

  def __init__(self) -> None:
    self.spark = SparkSession.builder \
    .master("local") \
    .appName("bigdata") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.extraClassPath", "/home/khuong/.local/opt/java-jar/postgresql-jdbc.jar") \
    .config("spark.sql.warehouse.dir", "/user/khuong") \
    .getOrCreate()

  def query(self, query: str) -> DataFrameReader:
    return self.spark.read \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("driver", "org.postgresql.Driver") \
    .option("query", query) \

class BigdataSession:
  spark: SparkSession
  df: DataFrame
  df_uni: DataFrame

  def __init__(self):
    self.spark = SparkSession.builder \
      .master("local") \
      .appName("test") \
      .config("spark.driver.memory", "2g") \
      .config("spark.executor.memory", "2g") \
      .config("spark.driver.extraClassPath", "/home/khuong/.local/opt/java-jar/postgresql-jdbc.jar") \
      .config("spark.sql.warehouse.dir", "/user/khuong") \
      .getOrCreate()

      # , avg(uni_entry.entry_point) as avg_entry_point
    self.df: DataFrame = query(self.spark, """
    select uni_code.university_id, uni_code.university, uni_code.subject_code
      , subject_name
      , min(uni_entry.entry_point) as min_entry_point
      , max(uni_entry.entry_point) as max_entry_point
      , uni_entry.code
      , universities.location
    from university_subject_entry uni_entry
    left join university_subject_code uni_code
    on (uni_entry.university_id, uni_entry.subject_code, uni_entry.year) = (uni_code.university_id, uni_code.subject_code, uni_code.year)
    left join universities
    on universities.id = uni_code.university_id
    where uni_entry.entry_point <= 30
    group by
    uni_code.university_id, uni_code.university
    , uni_code.subject_code, subject_name
    , uni_entry.year, uni_entry.code
    , universities.location
    """).load()

    self.students_subject_df = self.spark.read.load("student_each_subject")

    self.students_df = query(self.spark, """
      select * from student_score
      where year = 2023
    """).load()

    self.subjects_df = query(self.spark, """
    select * from subjects
      where first in ('geography', 'citizenship education', 'chemistry', 'physics', 'foreign_language', 'biology', 'history', 'math', 'literature', 'english'
      ) and second in  ('geography', 'citizenship education', 'chemistry', 'physics', 'foreign_language', 'biology', 'history', 'math', 'literature', 'english'
      ) and third in  ('geography', 'citizenship education', 'chemistry', 'physics', 'foreign_language', 'biology', 'history', 'math', 'literature', 'english'
      )
    """).load().cache()

    self.location_df = query(self.spark, """
      select * from location
    """).load().cache()

  def stop(self):
    self.spark.stop()
