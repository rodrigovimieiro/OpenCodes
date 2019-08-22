"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""

def remove_duplicates (elements):
  result = []
  for number in elements:
    if number not in result:
    	result.append(number)
  return result

print(remove_duplicates([1,2,3,1,4,5,2,6,7]))