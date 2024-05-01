# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 09:58:58 2024

@author: bdwye
"""



#initialize some variables
portion_down_payment = 0.25 #initialize
current_savings = 0 #initialize
r = 0.04 #initialize

#initialize our inputs
annual_salary = float(input('Enter your annual salary:'))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal:'))
total_cost = float(input('Enter the cost of your dream home:'))
semi_annual_raise = float(input('Enter the semi-annual raise, as a decimal:'))

#caluclate down payment required
down_required = portion_down_payment*total_cost

#initialize our counter
month_incrementer = 0 

while current_savings < down_required:
    if month_incrementer > 0 and month_incrementer%6 == 0:
        annual_salary = annual_salary*(1+semi_annual_raise)
    addition = current_savings*r/12 #do this within the while loop since we need it recalculated every time
    current_savings = current_savings + (addition) + (annual_salary*portion_saved/12) #divided by 12 to make it monthly
    month_incrementer += 1
    
print('Number of months: ', month_incrementer)
