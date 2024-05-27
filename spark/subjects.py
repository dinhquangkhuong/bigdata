


subjects_code = subjects.distinct().collect()

map(lambda val: val[1][1].split(","), subjects_code)
array = []
for value in subjects_code:
  sub = value[0][1].split(", ")
  for val in sub:
    array.insert(0, unidecode(val.lower()))

for a in list(set(array)):
  print(a)

file = open("helo.csv", 'w')
print("code",  "first",  "second", "third", "fouth", sep=", ", file=file)
for value in subjects_code:
  print(value[1][1], ", ", value[0][1], sep="", file=file)

file.flush()
file.close()

