# problem 6

titanic_data <- read.csv(file="titanic.csv", head=TRUE, sep=",")
print(titanic_data)

summary(titanic_data)

#Problem 7

# print names of columns
names(titanic_data)

# contents of first column
titanic_data$PassengerId

# contents of second column
titanic_data$Survived

#a table that outlines the distribution of genders in the dataset
table(titanic_data$Sex)


#Problem 8

#the proportion of men and women who survived
prop.table(table(titanic_data$Sex, titanic_data$Survived),1)

#The probability that someone would survive the crash based on gender
prop.table(table(titanic_data$Sex, titanic_data$Survived),2)


#Problem 9

titanic_data$Child<-0
titanic_data$Child[titanic_data$Age<18]<-1
aggregate(Survived ~ Sex + Child, data=titanic_data, FUN=function(x){sum(x)/length(x)})
