from pyspark.sql import Row
from session import BigdataSlim


bigdata = BigdataSlim()

# df = bigdata.spark.read.load("student_subject_splited")
#
# location_df = bigdata.query("""
# select * from location
# """).load()
#
# df = df.join(location_df, df.student_id.startswith(location_df.pcode))
#
# df.groupBy(["subject", "year", "iso_code", "name", "pcode"]).avg("point") \
# .withColumnsRenamed({
#   "avg(point)": "avg_point",
#   "name": "provence"
# }) \
# .write.save("student_subject_avg")

df = bigdata.spark.read.load("student_subject_avg")

df.show()

# def check(row: Row):
#   if row.iso_code is None and row.provence == "Bà Rịa-Vũng Tàu":
#     return (row.subject, row.year, "VN-43", row.provence, row.pcode, row.avg_point)
#   return (row.subject, row.year, row.iso_code, row.provence, row.pcode, row.avg_point)
#
#
# df = df.rdd.map(check).toDF(
#   schema=[ "subject", "year", "iso_code", "provence", "pcode", "avg_point" ]
# )
#
# df.write.save("student_subject_avg_true")
