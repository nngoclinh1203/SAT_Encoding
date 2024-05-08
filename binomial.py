import subprocess
from itertools import combinations
import pandas as pd
import time


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

    # Problem statement
    problem_statement = 'p cnf {} {}\n'.format(n, len(clauses))

    # All clauses
    cnf = '\n'.join(clauses)

    return problem_statement + cnf

results = []
total_time = 0;

# #Example usage:
# n = 3  # Number of items
# k = 2  # Number of items to choose
# sat_problem = binomial_sat_encoding(n, k)
# print(sat_problem)

for n in range(1,101):
    
    k = 2
    
    start_time_encoding = time.time()
    
    sat_problem = binomial_sat_encoding(n, k)
    
    end_time_encoding = time.time()
    
    encoding_time = end_time_encoding - start_time_encoding
    
    # Write the problem to a temporary file
    with open('temp/temp_binomial.cnf', 'w') as f:
        f.write(sat_problem)

    # Use kissat to solve the problem
    start_time = time.time()
    result = subprocess.run(['kissat', 'temp/temp_binomial.cnf'], capture_output=True, text=True)
    end_time = time.time()
    
    # Calculate the processing time
    process_time = end_time - start_time
    total_time += process_time

    # Parse the solution
    solution = result.stdout
    sat_status = 'SAT' if 's SATISFIABLE' in solution else 'UNSAT'

    results.append({'n': n, 'k': k, 'Solution': solution, 'Processing Time': process_time, 'SAT Status': sat_status})
    
    
results.append({'n': 'Total', 'k': 'Total', 'Solution': 'Total', 'Processing Time': total_time, 'SAT Status': 'Total'})
# # Convert the results to a DataFrame
# df = pd.DataFrame(results)


# # Write the DataFrame to an Excel file
# df.to_excel('output/results_binomial.xlsx', index=False)
print(encoding_time)
print('done')