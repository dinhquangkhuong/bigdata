
def take_question():
  values = {} 
  with open("questions/question.csv") as file:
    line = file.readlines()
    
    header = list(map(lambda sub: sub.strip() ,line[0].split(",")))
    value =  list(map(lambda sub: sub.strip(),line[1].split(",")))
    
    for index, head in enumerate(header):
      if value[index].isdigit():
        values[head] = float(value[index])
      else:
        values[head] = value[index]

    file.close()
  return values




