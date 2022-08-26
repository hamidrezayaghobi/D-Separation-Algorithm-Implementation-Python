# D Separation Algorithm Implementation Python

## Summary:
In this project we implement the d-separation algorithm using python, so we can find if two variables are dependent or independent. And by using a variable elimination algorithm we find those two variables' probability

## Input:
1. Number of Beysian vertices (N)
2. In the next 2N lines(2 line for each vertice):
    1. Father of vertice (empty if vertice doesn't have any father) separated with space
    2. CPT table of vertice
3. All Observation separated with "," in this style: {vertice_number -> 0/1}. For example 12 -> 0 means we observe False for vertice number 12
4. number of two node separated with space (A B)

## Output:
1. Print "independent"/"dependent"
2. Probability of A
3. Probability of B

## Constraint
1. 1 <= N <= 20


## Example
 ```
    Input: 
    5

    0.001

    0.002
    1 2
    0.95 0.94 0.29 0.001
    3
    0.9 0.05
    3
    0.7 0.1
    1->1,2->1
    4 5

    Output:
    dependent
    0.86
    0.67
```
