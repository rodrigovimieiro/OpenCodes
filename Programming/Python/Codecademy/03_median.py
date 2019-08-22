"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""

def median (number_list):
  sorted_list = sorted(number_list)
  size = len(sorted_list)
  result = 0
  if size%2 == 0:	# Even
    result = (sorted_list[size/2 - 1] + sorted_list[size/2]) / 2.0
  else:	# Odd
    result = sorted_list[int(size/2)]
  return result

grades = [100, 100, 90, 40, 80, 100, 85, 70, 90, 65, 90, 85, 55]
print(median(grades))