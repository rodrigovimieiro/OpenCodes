"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""

class Employee(object):
  """Models real-life employees!"""
  def __init__(self, employee_name):
    self.employee_name = employee_name

  def calculate_wage(self, hours):
    self.hours = hours
    return hours * 20.00

# Add your code below!
class PartTimeEmployee(Employee):
  def calculate_wage(self,hours):
    self.hours = hours
    return hours * 12.00
  

employee = Employee('Rodrigo')
print(employee.employee_name, employee.calculate_wage(10))

partTimeEmployee = PartTimeEmployee('Joao')
print(partTimeEmployee.employee_name, partTimeEmployee.calculate_wage(10))