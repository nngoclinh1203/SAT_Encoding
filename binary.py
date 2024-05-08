from itertools import product
import subprocess
import time
import pandas as pd
import math

def binary_sat_encoding(n):
    clauses = []
    k = math.ceil(math.log2(n)) # Số bit cần thiết để biểu diễn n
    print("k = ", k)

    for i in range(1, n+1):
        binary = format(i-1, '0{}b'.format(k))  # Chỉnh lại i-1 để phù hợp với số thứ tự bắt đầu từ 0
        print(binary)
        clause = ''
        for j in range(k):
            if binary[j] == '0':
                clause += ' -Y{}'.format(j+1)
            else:
                clause += ' Y{}'.format(j+1)
        clause += ' 0'

        clauses.append(clause)

    return clauses
# Example usage:
n =  3 # Number of variables
sat_problem = binary_sat_encoding(n)

print(sat_problem)
# results = []
# total_time = 0;

# for n in range(1, 201):
    
#     sat_problem = binary_sat_encoding(n)
    
#     # Write the problem to a temporary file
#     with open('temp/temp_binary.cnf', 'w') as f:
#         f.write(sat_problem)

#     # Use kissat to solve the problem
#     start_time = time.time()
#     result = subprocess.run(['kissat', 'temp/temp_binary.cnf'], capture_output=True, text=True)
#     end_time = time.time()
    
#     # Calculate the processing time
#     process_time = end_time - start_time
#     total_time += process_time

#     # Parse the solution
#     solution = result.stdout
#     sat_status = 'SAT' if 's SATISFIABLE' in solution else 'UNSAT'

#     results.append({'n': n, 'Solution': solution, 'Processing Time': process_time, 'SAT Status': sat_status})

# results.append({'n': 'Total', 'Processing Time': total_time})

# df = pd.DataFrame(results)

# # Write the DataFrame to an Excel file
# df.to_excel('output/results_binary.xlsx', index=False)