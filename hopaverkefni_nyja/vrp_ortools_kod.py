"""Capacited Vehicles Routing Problem (CVRP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
import folium
import random


def create_data_model(distance_matrix, locations_demand, vehicle_capacities):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = distance_matrix
    data["demands"] = locations_demand
    data["vehicle_capacities"] = vehicle_capacities
    data["num_vehicles"] = len(vehicle_capacities)
    data["depot"] = 0
    return data

def print_solution(data, manager, routing, solution, locations_coords, locations, vehicle_capacities):
    """Prints solution on console and generates a map for each route."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    total_load = 0
    
    # Initialize the map
    map_all_routes = folium.Map(location=[64.14, -21.9], zoom_start=11)
    colors = ['blue', 'green', 'red', 'purple', 'cyan', 'brown', 'black','olive', 'magenta']
    already_used_color = []
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        points = []  # For mapping the route
        
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            location_name = locations[node_index]
            points.append(locations_coords[location_name])
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} ({location_name}) Load({route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            
        location_name = locations[manager.IndexToNode(index)]
        points.append(locations_coords[location_name])
        plan_output += f" {manager.IndexToNode(index)} ({location_name}) Load({route_load})\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        
        # Add the route to the map
        route_color = random.choice(colors)  # Picking a random color for each route
        while route_color in already_used_color:
            route_color = random.choice(colors)
        
        # Find the midpoint of the route
        midpoint_index = len(points) // 2
        midpoint_location = points[midpoint_index]

        # Add the vehicle ID at the midpoint of the route
        folium.Marker(
            location=midpoint_location,
            popup=f"V: {vehicle_id}, capacity: {vehicle_capacities[vehicle_id]}",
            icon=folium.Icon(color="white", icon_color=route_color)  # Use a neutral color for the marker but colored icon text
        ).add_to(map_all_routes)
                
        folium.PolyLine(points, color=route_color, weight=2.5, opacity=1).add_to(map_all_routes)
        for point in points:
            folium.CircleMarker(point, radius=5, color=route_color, fill=True, fill_color=route_color).add_to(map_all_routes)

        total_distance += route_distance
        total_load += route_load
        already_used_color.append(route_color)

    # Save the map with all routes to an HTML file
    map_all_routes.save('all_routes.html')

    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")





# Haversine distance, calculate distance between two coordinates
def haversine(coord1, coord2):
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # road heuristic mutliplier r
    r = 1.0
    return int(R * c * r * 1000)

def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    
    locations = [
        "DC",
        "Grafarholt",
        "Mosfellsbær",
        "Bíldshöfi",
        "Árbær",
        "Jafnarsel",
        "Vallarkór",
        "Lindir",
        "Grandi",
        "Hallveigarstígur",
        "Borgartún",
        "Austurver",
        "Hamraborg",
        "Garðabær",
        "Flatahraun",
        "Hvaleyrarbraut", 
        "Norðurhella",
        "Skeifan"
    ]
    # Locations and their coordinates
    

    locations_demand_dict = {
        "DC": 0,
        "Grafarholt": 57,
        "Mosfellsbær": 60,
        "Bíldshöfi": 80,
        "Árbær": 40,
        "Jafnarsel":  62,
        "Vallarkór": 62,
        "Lindir":  78,
        "Grandi": 80,
        "Hallveigarstígur": 43,
        "Borgartún": 55,
        "Austurver": 35,
        "Hamraborg":  35,
        "Garðabær":  10,
        "Flatahraun":  60,
        "Hvaleyrarbraut":  62,
        "Norðurhella":  61,
        "Skeifan": 72
    }

    locations_coords = {
        "DC": (64.12238188422718, -21.80556258041812),
        "Grafarholt": (64.13060762774467, -21.7616648461748),
        "Mosfellsbær": (64.16676053874438, -21.69815013762845),
        "Bíldshöfi": (64.12663767072458, -21.81462238088484),
        "Árbær": (64.11727231871421, -21.78990314307976),
        "Jafnarsel": (64.09889301241216, -21.826971272553056),
        "Vallarkór": (64.0854487078441, -21.822379330997656),
        "Lindir": (64.10251080254932, -21.873620252057236),
        "Grandi": (64.15864328795905, -21.949117186999928),
        "Hallveigarstígur": (64.1475671399666, -21.936757566966456),
        "Borgartún": (64.14831566757304, -21.898992064855193),
        "Austurver": (64.13139401690862, -21.88937902795415),
        "Hamraborg": (64.11491170786942, -21.905171874291582),
        "Garðabær": (64.09941317124606, -21.909806731692516),
        "Flatahraun": (64.07763129311066, -21.942765716339103),
        "Hvaleyrarbraut": (64.06344469095414, -21.965596678979097),
        "Norðurhella": (64.04673427118828, -21.983942988771656),
        "Skeifan": (64.13047013989885, -21.872698450597895)
    }
    # capacity of each vehicle
    capacity = 200
    # demand in each location (distribution center has 0 demand)
    locations_demand = [0, 57, 60, 80, 40, 62, 
                        62, 78, 80, 43, 55, 35, 
                        35, 10, 60, 62, 61, 72]
    # minimum number of vehicles needed
    min_vehicles = math.ceil(sum(locations_demand)/capacity)
    vehicle_capacities = [200]*min_vehicles
    #vehicle_capacities = [100, 125, 300, 500]
    
    
    # Create distance matrix
    distance_matrix = []
    for i in locations_coords:
        row = []
        for j in locations_coords:
            row.append(round(haversine(locations_coords[i], locations_coords[j]), 2))  # Distance rounded to two decimal places
        distance_matrix.append(row)

    data = create_data_model(distance_matrix, locations_demand, vehicle_capacities)
    #vehicle_capacities = [400, 400, 400]
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    ################### Each vehicle can only travel max_distance m ##################
    #-------------------------------------------------------------------------------#
    """ max_distance = 20000
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        max_distance,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)  """
    
    #################################################################################
    #-------------------------------------------------------------------------------#
    ################# Each vehicle can only carry a certain amount ##################
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )
    ################################################################################
    
    #################### constraints on particular locations ######################
    ######################### Special constraint 1 ################################
    city1_index = manager.NodeToIndex(locations.index("Grafarholt"))
    city2_index = manager.NodeToIndex(locations.index("Mosfellsbær"))

    routing.solver().Add(routing.VehicleVar(city1_index) != routing.VehicleVar(city2_index))
    
    ######################### Special constraint 2 ################################
    city3_index = manager.NodeToIndex(locations.index("Jafnarsel"))
    city4_index = manager.NodeToIndex(locations.index("Austurver"))

    routing.solver().Add(routing.VehicleVar(city3_index) == routing.VehicleVar(city4_index))

    
    ################################################################################

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    
    solution_time_limit = 1 # sec
    #search_parameters.log_search = True   # Optional: Enables detailed logging of the search process
    search_parameters.time_limit.FromSeconds(solution_time_limit)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    #print(solution)
    # Print the metrics:
    if solution:
        # Your existing print_solution function
        print_solution(data, manager, routing, solution, locations_coords, locations, vehicle_capacities)
        print("Number of nodes:", routing.nodes())
        print("Number of branches explored:", routing.solver().Branches())
        print("Number of solutions found:", routing.solver().Solutions())
        print("Search duration (ms):", routing.solver().WallTime())

        
    else:
        print("No solution found!")


if __name__ == "__main__":
    main()