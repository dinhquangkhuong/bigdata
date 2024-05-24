from pyspark.sql import Row, SparkSession
from session import query
from pyspark.sql import functions as F

jdbc_url = "jdbc:postgresql://localhost:5432/bigdata?ssl=true&sslmode=require&user=khuong&password=123456789"

spark = SparkSession.builder \
      .master("local") \
      .appName("test") \
      .config("spark.driver.memory", "2g") \
      .config("spark.executor.memory", "2g") \
      .config("spark.jars", "/home/khuong/.local/opt/java-jar/postgresql-jdbc.jar") \
      .config("spark.sql.warehouse.dir", "/user/khuong") \
      .getOrCreate()

student_score = query(spark, """
  select * from student_score
""").load()

subjects = query(spark, """
    select * from subjects
      where first in ('geography', 'citizenship education', 'chemistry', 'physics', 'foreign_language', 'biology', 'history', 'math', 'literature', 'english'
      ) and second in  ('geography', 'citizenship education', 'chemistry', 'physics', 'foreign_language', 'biology', 'history', 'math', 'literature', 'english'
      ) and third in  ('geography', 'citizenship education', 'chemistry', 'physics', 'foreign_language', 'biology', 'history', 'math', 'literature', 'english'
      )
""").load()
# subjects = query(spark, """
#     select * from subjects
#       where first in ('citizenship education') and second in  ('citizenship education') and third in ('geography', 'citizenship education', 'chemistry', 'physics', 'foreign_language', 'biology', 'history', 'math', 'literature', 'english'
#       )
# """).load()

student_score_with_subject = subjects.crossJoin(student_score).rdd

def getOr(d: dict, key, default):
  value = d.get(key, default)
  if value:
    return value
  return default

def turnTotalEach(row: Row):
  row_dict = row.asDict()
  first = float(getOr(row_dict, row.first, -1))
  second = float(getOr(row_dict,row.second, -1))
  third = float(getOr(row_dict,row.third, -1))
  if first == -1 or second == -1 or third == -1:
    return None
  return (row.id, row.year, row.student_id, row.code, row.first, row.second, row.third, first + second + third)

student_subject = student_score_with_subject.map(turnTotalEach) \
.filter(lambda row: row is not None) \
.toDF(schema=[
  "id", "year", "student_id", "code", "first", "second", "third", "total_point"
]).sort("total_point", ascending=False).withColumn("position", F.monotonically_increasing_id())

student_subject.write.save("student_each_subject_3")


