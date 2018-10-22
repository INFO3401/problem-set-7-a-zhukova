# Anastasiya Zhukova
# Wednesday -- Problem Set 7


####################################################
# Question 1
####################################################

import pandas as pd 

obesity_df = pd.read_csv('CDC_Obesity_Data.csv')
A = obesity_df.Question.unique()
print(A)

# What does A equal in the expression X ∈ A?
# The printed output privides the names of all the elements of X in A


###################################################
# Question 2
####################################################

B = obesity_df['Data_Value'].sum()
print ('B is equivalent to'+ ' ' + str(B))

# The print statement prints out the sum of all values of the Data_Value column
# which is equivalent to B


###################################################
# Question 3
####################################################

#See png graphic labeled % of Adults who have Obesity.
#This data looks like it follows a standard normal distribution.


###################################################
# Question 4
####################################################

#See png graphic labeled % of Adults who have Obesity over time.
#This distribution shows us that the percentage of adults who have obesity is increasing over time.