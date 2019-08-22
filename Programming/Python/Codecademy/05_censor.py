"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""

def censor(text, desired_word):
  size = len(desired_word)
  new_string = text.split()
  result = []
  for word in new_string:
    if word ==  desired_word:
      result.append(size*"*")
    else:
      result.append(word)
  return " ".join(result)

print(censor("Hello, my name is Rodrigo", "Rodrigo"))