import itertools
import numpy as np
import time
import matplotlib.pyplot as plt
import ortools

def generate_distance_matrix(n, upper_bound = 11):
    # Create an n x n matrix with random values
    matrix = np.random.randint(1, upper_bound, size=(n, n))  # random values between 1 and 10
    
    # Set the diagonal to 0
    np.fill_diagonal(matrix, 0)
    
    # Make the matrix symmetric
    for i in range(n):
        for j in range(n):
            matrix[j][i] = matrix[i][j]
            
    return matrix

class tsp:
    def __init__(self, dist_array) -> None:
        self.dist_array = dist_array
    
    def brute_force(self):
        n = len(self.dist_array)
        cities = list(range(n))
        
        shortest_distance = float('inf')
        best_path = None
        
        # Generate all possible tours (permutations) and calculate the total distance
        for tour in itertools.permutations(cities):
            # Always start and end at the first city for simplicity
            total_distance = sum(self.dist_array[tour[i]][tour[i+1]] for i in range(n-1))
            total_distance += self.dist_array[tour[-1]][tour[0]]
            
            if total_distance < shortest_distance:
                shortest_distance = total_distance
                best_path = tour
                
        return best_path, shortest_distance
            





np.random.seed(123)
dist_matrix = generate_distance_matrix(5, 100)
print(dist_matrix)

test = tsp(dist_matrix)

start_time = time.time()
best_tour, best_distance = test.brute_force()
end_time = time.time()

print("Best tour:", best_tour)
print("Shortest distance:", best_distance)
print("Time taken:", end_time - start_time, "seconds")

    
