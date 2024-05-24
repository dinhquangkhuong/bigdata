from pyspark.sql import DataFrame, Row
from pyspark.sql.functions import expr
from session import BigdataSlim
from functools import reduce

jdbc_url = "jdbc:postgresql://127.0.0.1:5432/bigdata"

bigdata = BigdataSlim()

# student_score_df = bigdata.query("""
#   select * from student_score
# """)

subjects = ["geography", "citizenship education", "chemistry", "physics", "foreign_language", "biology", "history", "math", "literature", "english" ]

def queryOne(subject: str):
  query = """
    select id, student_id, year, \"{subject}\" as point, \'{subject}\' as subject from student_score
    where \"{subject}\" is not null
  """.format(subject=subject)
  return bigdata.query(query).load()


def df_union(ac: DataFrame, df: DataFrame):
  return ac.union(df)

subject_split = reduce(df_union, map(queryOne, subjects))


subject_split.write.save("student_subject_splited")

subject_split \
.write.jdbc(jdbc_url, "subject_split", mode='ignore',properties={
  'user': 'khuong',
  'password': '123456789'
})
#
# def splitRow(row: Row):
  


# student_score_df.rdd.map(splitRow)


