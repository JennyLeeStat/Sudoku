# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: When two possible digits are locked in two boxes, we can rule out these two digits from peers. This strategy is called
[Naked twins](http://www.sudokudragon.com/sudokustrategy.htm#XL2104). 
First we filter boxes with two possible digits and check any pairs belong to the same unitlist. 
If so, we eliminate those two digits from their peers in the unit. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We'll add an additional local constraint that two diagonals, [A1, B2, ..., I9] and [A9, B8, ..., I1],   in the board include one set of all digits, digits 1 through 9 appear only once. 


### Conda Environments
You can find the Conda environment file for Mac OS at environment.yml


### Reference

* http://norvig.com/sudoku.html
* https://github.com/udacity/aind-sudoku

