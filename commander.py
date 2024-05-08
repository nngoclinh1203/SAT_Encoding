from itertools import combinations
import subprocess
import time
import pandas as pd
import math

def to_dimacs(clauses, num_vars):
    dimacs = []
    dimacs.append('p cnf {} {}'.format(num_vars, len(clauses)))
    for clause in clauses:
        dimacs.append(''.join(clause) + ' 0')
    return '\n'.join(dimacs)

def binomial_sat_encoding(n, k):
    clauses = []

    # At least one item must be chosen in each subset of k items
    for subset in combinations(range(1, n + 1), k):
        clause = [str(item) for item in subset]
        clause.append('0')  # End of clause
        clauses.append(' '.join(clause))

    # At most one item must be chosen in each subset of k + 1 items
    for subset in combinations(range(1, n + 1), k + 1):
        for item in subset:
            clause = ['-{}'.format(item)] + [str(other_item) for other_item in subset if other_item != item]
            clause.append('0')  # End of clause
            clauses.append(' '.join(clause))

    # All clauses
    cnf = '\n'.join(clauses)
    print("cnf: ", cnf)

    return cnf

def commander_sat_encoding(n):
    # Generate variable names
    variables = ['X{}'.format(i) for i in range(1, n+1)]

    # Generate clauses using Commander encoding
    clauses = commander_encoding(variables, n)

    # Convert to DIMACS format
    dimacs = to_dimacs(clauses, n)

    return dimacs

def commander_encoding(variables, n):
    num_groups = math.floor(math.sqrt(n))
    group_size_max = math.ceil(n / num_groups)

    groups = [variables[i:i+group_size_max] for i in range(0, len(variables), group_size_max)]
    print(groups)
    print(len(groups), '------------------------')
    
    commanders = ['C{}'.format(i) for i in range(1, len(groups) + 1)]  # Change here
    clauses = []
    
    # AMO, ALO Clauses for c1, c2,…, cm
    clauses_commander = binomial_sat_encoding(len(groups), 2)
    print("clauses_commander: ", clauses_commander)
    clauses.extend(clauses_commander.split('\n')[0:])
    print("clauses: ", clauses)
    
    
    
    for group, commander in zip(groups, commanders):
        # If a commander variable ci is true then exactly one variable true in Gi
        clauses.extend(at_most_one(group + [commander]))
        print(clauses)
        clauses.extend(at_least_one(group, commander))
        print(clauses, '------------------------')
        # If a commander variable ci is false then all variables false in Gi
        for var in group:
            clauses.append('-{} -{}'.format(commander, var))
            
    return clauses

def at_most_one(variables):
    return ['-{} -{}'.format(var1, var2) for i, var1 in enumerate(variables) for var2 in variables[i+1:]]

def at_least_one(variables, commander):
    return ['{} -{}'.format(' '.join(variables), commander)]

satproblem = commander_sat_encoding(6)
print(satproblem)
