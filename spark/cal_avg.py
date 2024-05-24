from pyspark.sql import DataFrameReader, functions as F
from pyspark.sql import SparkSession

jdbc_url = "jdbc:postgresql://localhost:5432/bigdata?ssl=true&sslmode=require&user=khuong&password=123456789"

def query(spark: SparkSession, query: str) -> DataFrameReader:
  return spark.read \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("driver", "org.postgresql.Driver") \
    .option("query", query)

spark: SparkSession = SparkSession.builder \
      .appName("test") \
 jj     .config("spark.driver.memory", "2g") \
      .config("spark.executor.memory", "2g") \
      .config("spark.driver.extraClassPath", "/home/khuong/.local/opt/java-jar/postgresql-jdbc.jar") \
      .config("spark.sql.warehouse.dir", "/user/khuong") \
      .getOrCreate()

location_df = query(spark, """
  select * from location
""").load().cache()

students_subject_df = spark.read.load("student_compund_subject_final")

students_subject_df_with_location = students_subject_df.join(location_df, on=(students_subject_df.student_id.startswith(location_df.pcode))).cache()

df = students_subject_df_with_location.groupBy(["code", "year", "pcode", "name", "mien", "iso_code" ]) \
.agg()
.avg("total_point").sort("avg(total_point)") \
.withColumnRenamed("avg(total_point)", "avg_total_point")


# df_max = students_subject_df_with_location.groupby(["code", "year", "pcode", "name", "mien", "iso_code" ]) \
# .max("total_point").sort("avg(total_point)") \
# .withColumnRenamed("avg(total_point)", "avg_total_point")
#
# df_min = students_subject_df_with_location.groupby(["code", "year", "pcode", "name", "mien", "iso_code" ]) \
# .min("total_point").sort("avg(total_point)") \
# .withColumnRenamed("avg(total_point)", "avg_total_point")


df.join(df_max, ((df.code == df_max.code) & (df.year == df_max.year) & (kjj)))

df.write.save("avg_sub_compound", mode='overwrite')
df.write.jdbc(jdbc_url, "avg_sub_compound", mode='overwrite')

# students_subject_df.limit(10).show()
