"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
# Add your function below!
def average (numbers):
  avrg = 0
  n = 0
  for number in numbers:
    avrg = avrg + number
    n = n + 1
  avrg = float(avrg) / n
  return avrg

def get_average (student):
  homework = average(student["homework"] )
  quizzes = average(student["quizzes"] )
  test = average(student["tests"] )
  return 0.1*homework + 0.3*quizzes + 0.6*test

def get_letter_grade (score):
  if score >= 90:
    return "A"
  elif score >= 80:
    return "B"
  elif score >= 70:
    return "C"
  elif score >= 60:
    return "D"
  else:
    return "F"
  
def get_class_average (class_list):
  results = []
  for student in class_list:
    avgr = get_average(student)
    results.append(avgr) 
  return average(results)


lloyd = {
  "name": "Lloyd",
  "homework": [90.0, 97.0, 75.0, 92.0],
  "quizzes": [88.0, 40.0, 94.0],
  "tests": [75.0, 90.0]
}
alice = {
  "name": "Alice",
  "homework": [100.0, 92.0, 98.0, 100.0],
  "quizzes": [82.0, 83.0, 91.0],
  "tests": [89.0, 97.0]
}
tyler = {
  "name": "Tyler",
  "homework": [0.0, 87.0, 75.0, 22.0],
  "quizzes": [0.0, 75.0, 78.0],
  "tests": [100.0, 100.0]
}


print(get_class_average([lloyd, alice, tyler]))
print(get_letter_grade(get_class_average([lloyd, alice, tyler])))