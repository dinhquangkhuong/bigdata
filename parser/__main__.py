

with open("data_csv/diemthi2023.csv") as file:
  lines = file.readlines();
  
  isFirst = True
  for line in lines:
    line = line[:-1]
    if isFirst:
      print(line, ", year", sep="")
      isFirst = False
    else:
      print(line, ", 2023", sep="")


  



