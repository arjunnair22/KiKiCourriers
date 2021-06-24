# KiKiCourriers

#Install python 3 latest version.

#Make sure the python is in environment path 

#In the root of the project run the following command

#python main.py

Idea behind the code

The idea is kind of a greedy approach where 
the package is initially sorted by package weight and pushed into the vehicle one by one. If any package is found to be have more weight than what can be inserted we replace the weight with one that was already in the vehicle by performing a linear search ( this can be improved to a binary search)

The logic to replace is to find a package with lowest weight greater than difference of current package weight - total weight in package

This is done for all packages for current vehicle and is iterated a number of times till the all packages are scheduled .
