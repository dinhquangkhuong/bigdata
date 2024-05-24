#!/usr/bin/env spark-submit --jars /home/khuong/.local/opt/java-jar/postgresql-jdbc.jar --driver-memory 2g  --executor-memory 2g 

from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame
from session import BigdataSession
from utils import turnTotalEach

bigdata = BigdataSession()

df: DataFrame = bigdata.df
subject_df = bigdata.subjects_df

questions_df = bigdata.spark.read.csv("questions", header=True)

joined_question = questions_df.crossJoin(subject_df)

bigdata.students_subject_df.filter("code == 'A01' and year == 2023") \
.sort("total_point", ascending=False).show()

# total_points = joined_question.rdd.map(turnTotalEach).toDF(schema=[
#   "id", "code", "first", "second", "third", "location", "total_point"
# ]).cache()
#
# max_point = total_points.groupBy(["id"]) \
#   .max("total_point") \
#   .withColumnsRenamed({
#     "max(total_point)": "max_point",
#     "id": "student_id",
#   })
#
# max_p_full = total_points.join(max_point, ((total_points.id == max_point.student_id) & (total_points.total_point == max_point.max_point))) \
# .select(['student_id', 'code', 'first', 'second', 'third', 'max_point', 'location'])
#
# # max_p_full.show()
#
# location_df = bigdata.location_df
#
# max_p_full = max_p_full.join(location_df, (max_p_full.location == location_df.name)) \
#   .select(['student_id', 'code', 'first', 'second', 'third', 'max_point', 'location', 'pcode'])
#
# students_subject_df = bigdata.students_subject_df
# student_score = students_subject_df \
# .join(max_p_full.select(["student_id", "code", "max_point", "location", 'pcode' ])
#       , (students_subject_df.code == max_p_full.code))
#
#
#
# bigdata.stop()

# broadQuestion = bigdata.spark.sparkContext.broadcast(question)
# @F.udf(returnType=FloatType())
# def totalPoint(first, second, third):
#   first_p = question.get(first, 0)
#   second_p = question.get(second, 0)
#   third_p = question.get(third, 0)
#
#   return first_p + second_p + third_p
#
# # questions_df.
# # subject_df = subject_df.join(questions_df, "true").withColumn("total_point", totalPoint("first", "second", "third", ))
#
# max_subject = subject_df.sort("total_point", ascending=False).first()
# max_subject_bs = bigdata.spark.sparkContext.broadcast(max_subject)
#
# student_df = bigdata.students_df;
#
# first_sub = student_df.__getattr__(max_subject.first)
# second_sub = student_df.__getattr__(max_subject.second)
# thrid_sub = student_df.__getattr__(max_subject.third)
# # question['location']
#
# student_df = student_df.filter("student_id like '01%'") \
# .withColumn("max_compare", first_sub + second_sub + thrid_sub)
#
# student_df.filter("max_compare is not null") \
# .sort("max_compare", ascending=False) \
# .show()
#
# print(max_subject)
# print(30 * (1 - max_subject.total_point / 37.5))
# print(37.5 * (1 - max_subject.total_point / 30))
# df = df.filter(((max_subject.total_point  > df.avg_entry_point - 30 * (1 - df.avg_entry_point / 37.5)) \
# & ( max_subject.total_point < df.avg_entry_point + 37.5 * (1 - df.avg_entry_point / 30))) \
# df = df.filter(((max_subject.total_point > df.avg_entry_point - 0.5) & ( max_subject.total_point < df.avg_entry_point + 0.5)) \
#   & (df.code == max_subject.code)) \
#   .select("university", "location", "subject_name", "avg_entry_point", "max_entry_point", "min_entry_point", "code") \
#   .filter(df.location == broadQuestion.value.get("location")) \
#   .sort("avg_entry_point", ascending=False)
# df.show()
#
# bigdata.stop()
#

