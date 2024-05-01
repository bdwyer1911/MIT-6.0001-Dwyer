# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 09:58:58 2024

@author: bdwye
"""



#initialize some fixed variables
portion_down_payment = 0.25 
r = 0.04 
current_savings = 0
total_cost = 1000000
semi_annual_raise = .07
total_months = 36
epsilon = 100

#initialize our inputs
input_annual_salary = float(input('Enter your annual salary:'))

#caluclate down payment required
down_required = portion_down_payment*total_cost

#initialize our counter
counter = 0 

#initialize our bisecting guess
low_value = 0
high_value = 10000
guess = (low_value+high_value)/2/10000

while abs(current_savings - down_required) >= epsilon:
    #reset some values every time the while loop starts again
    annual_salary = input_annual_salary
    current_savings = 0
    
    #check if possible
    for months in range(1,total_months+1):
        if months > 0 and months%6 == 0:
            annual_salary = annual_salary*(1+semi_annual_raise)
        addition = current_savings*r/12 #do this within the while loop since we need it recalculated every time
        current_savings = current_savings + (addition) + (annual_salary*high_value/12/10000) #divided by 12 to make it monthly
    
    #procedure for if it's not possible to save that much    
    if current_savings < down_required:
        print('it is not possible to pay down the payment in 3 years')
        possible = False
        break
    else:
        possible = True
        annual_salary = input_annual_salary
        current_savings = 0
    
    for months in range(1,total_months+1):
        if months > 0 and months%6 == 0:
            annual_salary = annual_salary*(1+semi_annual_raise) #raises every 6 months
        addition = current_savings*r/12 #do this within the while loop since we need it recalculated every time
        current_savings = current_savings + (addition) + (annual_salary*guess/12) #divided by 12 to make it monthly
            
    if current_savings > down_required:
        high_value = guess*10000
        
    else:
        low_value = guess*10000
            
    #make a new guess and increment the counter
    guess = (low_value+high_value)/2/10000
    counter += 1
    
#print out the results
if possible:      
    print('Ideal savings rate: ', guess)    
    print('Steps in bisection search: ', counter)
