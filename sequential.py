import itertools
import subprocess
import time
import pandas as pd

def sequential_sat_encoding(n):
    clauses = []

    # Variables
    variables = ['X{}'.format(i) for i in range(1, n+1)]
    new_variables = ['S{}'.format(i) for i in range(1, n)]

    # ALO Clauses
    amo_clause = ' '.join(variables) + ' 0'  # At most one constraint
    clauses.append(amo_clause)
    
    # AMO Clauses
    for i in range(1, n-1):  # Adjusted here
        # X1 → S1
        clause = ['-{}'.format(variables[0]), new_variables[0], '0']
        clauses.append(' '.join(clause))
        
        # (Xi v Si-1) → Si
        clause = ['-{}'.format(variables[i]), new_variables[i-1], new_variables[i], '0']
        clauses.append(' '.join(clause))
        
        # (Si-1 → ¬Xi)
        clause = ['-{}'.format(new_variables[i-1]), '-{}'.format(variables[i]), '0']
        clauses.append(' '.join(clause))
        
        if i == n-2:  # Adjusted here
            # (Sn-1 → ¬Xn)
            clause = ['-{}'.format(new_variables[i]), '-{}'.format(variables[i+1]), '0']  # Adjusted here
            clauses.append(' '.join(clause))

    # Problem statement
    problem_statement = 'p cnf {} {}\n'.format(n, len(clauses))

    # All clauses
    cnf = '\n'.join(clauses)

    return problem_statement + cnf

def convert_to_dimacs(n, clauses):
    # Create a mapping of variable names to integers
    var_mapping = {f'X{i}': i for i in range(1, n+1)}
    var_mapping.update({f'S{i}': n+i for i in range(1, n)})

    # Convert clauses to use integer variables
    int_clauses = []
    for clause in clauses.split('\n')[1:]:  # Skip the first line (problem statement)
        int_clause = []
        for var in clause.split():
            if var.startswith('-'):
                # Negative variable
                int_clause.append('-' + str(var_mapping[var[1:]]))
            elif var != '0':
                # Positive variable
                int_clause.append(str(var_mapping[var]))
            else:
                # End of clause
                int_clause.append('0')
        int_clauses.append(' '.join(int_clause))

    # Problem statement
    problem_statement = 'p cnf {} {}\n'.format(2*n-1, len(int_clauses))

    # All clauses
    cnf = '\n'.join(int_clauses)

    return problem_statement + cnf

# n = 4
# sat_problem = sequential_sat_encoding(n)
# sat_problem_dimacs = convert_to_dimacs(n, sat_problem)
# print(sat_problem_dimacs)

# # Ghi `sat_problem` vào một tệp văn bản
# with open('temp/temp_sequential.cnf', 'w') as f:
#     f.write(sat_problem_dimacs)

# # Chạy Kissat trên tệp văn bản
# result = subprocess.run(['kissat', 'temp/temp_sequential.cnf'], capture_output=True, text=True)

# # In kết quả
# print(result.stdout)

# Example usage:
results = []
total_time = 0

for n in range(2, 201):  # Start from 2 as it requires at least two variables
    
    sat_problem_old = sequential_sat_encoding(n)
    sat_problem = convert_to_dimacs(n, sat_problem_old)
    
    # Write the problem to a temporary file
    with open('temp/temp_sequential.cnf', 'w') as f:
        f.write(sat_problem)
        
    start_time = time.time()
    # Use a SAT solver to solve the problem
    result = subprocess.run(['kissat', 'temp/temp_sequential.cnf'], capture_output=True, text=True)
    end_time = time.time()
    
    # Calculate the processing time
    process_time = end_time - start_time
    total_time += process_time

    # Parse the solution
    solution = result.stdout
    sat_status = 'SAT' if 's SATISFIABLE' in solution else 'UNSAT'

    results.append({'n': n, 'Solution': solution, 'Processing Time': process_time, 'SAT Status': sat_status})

results.append({'n': 'Total', 'Processing Time': total_time})

df = pd.DataFrame(results)

# Write the DataFrame to an Excel file
df.to_excel('output/results_sequential.xlsx', index=False)
