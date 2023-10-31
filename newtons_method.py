import numpy as np
import matplotlib.pyplot as plt

current_function                   = lambda x : x**3 +  30*x - x**6 - 2*x**4 - 3*x**2
derivative_current_function        = lambda x : 3*x**2 +  30 - 6*x**5 - 8*x**3 - 6*x
second_derivative_current_function = lambda x : 6*x - 30*x**4 - 24*x**2 - 6

def optimize_newton(df, ddf, x0, epsilon = 0.001, max_iterations = 10000):
    x0_old = x0
    i     = 0
    while(i <= max_iterations):
        df_val  = df(x0)
        ddf_val = ddf(x0)
        
        x0 = x0 - df_val/ddf_val
        
        if abs(x0 - x0_old) <= epsilon:
            return x0, i
        x0_old = x0
        i += 1
    return x0, i

initial_guess = 1
optimal_solution, iterations = optimize_newton(derivative_current_function, second_derivative_current_function, initial_guess)

print(f"Initial guess, x = {initial_guess}")
print(f"Optimal solution is: x* = {optimal_solution}, f(x*) = {current_function(optimal_solution)},  solution found in {iterations} iterations")

