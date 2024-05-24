from pyspark.sql import Row

def turnTotalEach(row: Row):
  row_dict = row.asDict()
  first = float(row_dict.get(row.first, 0))
  second = float(row_dict.get(row.second, 0))
  third = float(row_dict.get(row.third, 0))
  return (row.id, row.code, row.first, row.second, row.third, row.location, first + second + third)
