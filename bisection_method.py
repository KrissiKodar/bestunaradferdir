import numpy as np
import matplotlib.pyplot as plt

current_function            = lambda x : x**3 +  30*x - x**6 - 2*x**4 - 3*x**2
derivative_current_function = lambda x : 3*x**2 +  30 - 6*x**5 - 8*x**3 - 6*x

def optimize_bisection(df, x0_lower, x0_higher, epsilon = 0.07, max_iterations = 10000):
    x_sol = (x0_lower + x0_higher)/2
    i     = 0
    while(i <= max_iterations):
        df_val = df(x_sol)
        
        if df_val >= 0:
            x0_lower = x_sol
        if df_val <= 0:
            x0_higher = x_sol
            
        x_sol = (x0_lower + x0_higher)/2
        
        if x0_higher - x0_lower <= 2*epsilon:
            return x_sol, i
        i += 1
    return x_sol, i

initial_guess_lower = 0
initial_guess_higher = 2
optimal_solution, iterations = optimize_bisection(derivative_current_function, initial_guess_lower, initial_guess_higher)

print(f"Initial guess, x_lower = {initial_guess_lower}, x_higher = {initial_guess_higher}")
print(f"Optimal solution is: x* = {optimal_solution}, f(x*) = {current_function(optimal_solution)},  solution found in {iterations} iterations")





# Generate a range of x-values
x = np.linspace(-0, 2, 400)  # Adjust the range as needed

# Calculate corresponding y-values using the function
y = current_function(x)

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='y = x^3 + 30x - x^6 - 2x^4 - 3x^2')
plt.title('Plot of the Function')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()
