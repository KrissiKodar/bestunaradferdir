import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model(distance_matrix):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = distance_matrix
    return data

def main(distance_matrix):
    # Instantiate the data problem.
    data = create_data_model(distance_matrix)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           1, 0)

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    index = routing.Start(0)
    plan_output = 'Route:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f' {manager.IndexToNode(index)} ->'
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += f' {manager.IndexToNode(index)}\n'
    print(plan_output)
    print(f"Route distance: {route_distance}")

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



# Example usage:
np.random.seed(123)
dist = generate_distance_matrix(5, 100)
print(dist)
main(dist)
