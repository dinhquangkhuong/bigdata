from pyspark.sql import functions as F
from pyspark.sql import SparkSession

jdbc_url = "jdbc:postgresql://127.0.0.1:5432/bigdata"

      # .config("spark.driver.extraClassPath", "/home/khuong/.local/opt/java-jar/postgresql-jdbc.jar") \
spark: SparkSession = SparkSession.builder \
      .appName("test") \
      .config("spark.driver.memory", "2g") \
      .config("spark.executor.memory", "2g") \
      .config("spark.sql.warehouse.dir", "/user/khuong") \
      .getOrCreate()

students_subject_df = spark.read.load("student_each_subject_2")
students_subject_add_df = spark.read.load("student_each_subject_3")

students_subject_final_df = students_subject_df.union(students_subject_add_df) \
.groupBy([ 'id', 'student_id', 'code', 'year' ]) \
.max('total_point').withColumnRenamed('max(total_point)', 'total_point')

# students_subject_final_df.write.save("student_compund_subject_final")

students_subject_final_df.write.jdbc(url=jdbc_url, table="student_compund_subject_final", properties={
  'user': 'khuong',
  'password': '123456789'
}, mode='append')


