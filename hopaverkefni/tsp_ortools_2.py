"""Capacited Vehicles Routing Problem (CVRP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
import folium
import random
def create_data_model():
    """Stores the data for the problem."""

    locations = [
        "DC",
        "Krónan Grafarholt",
        "Krónan Mosfellsbær",
        "Krónan Bíldshöfi",
        "Krónan Árbær",
        "Krónan Jafnarsel",
        "Krónan Vallarkór",
        "Krónan Lindir",
        "Krónan Grandi",
        "Krónan Hallveigarstígur",
        "Krónan Borgartún",
        "Krónan Austurver",
        "Krónan Hamraborg",
        "Krónan Garðabær",
        "Krónan Flatahraun",
        "Krónan Hvaleyrarbraut", 
        "Krónan Norðurhella",
        "Krónan Skeifan"
    ]

    # Locations and their coordinates
    locations_coords = {
        "DC": (64.12238188422718, -21.80556258041812),
        "Krónan Grafarholt": (64.13060762774467, -21.7616648461748),
        "Krónan Mosfellsbær": (64.16676053874438, -21.69815013762845),
        "Krónan Bíldshöfi": (64.12663767072458, -21.81462238088484),
        "Krónan Árbær": (64.11727231871421, -21.78990314307976),
        "Krónan Jafnarsel": (64.09889301241216, -21.826971272553056),
        "Krónan Vallarkór": (64.0854487078441, -21.822379330997656),
        "Krónan Lindir": (64.10251080254932, -21.873620252057236),
        "Krónan Grandi": (64.15864328795905, -21.949117186999928),
        "Krónan Hallveigarstígur": (64.1475671399666, -21.936757566966456),
        "Krónan Borgartún": (64.14831566757304, -21.898992064855193),
        "Krónan Austurver": (64.13139401690862, -21.88937902795415),
        "Krónan Hamraborg": (64.11491170786942, -21.905171874291582),
        "Krónan Garðabær": (64.09941317124606, -21.909806731692516),
        "Krónan Flatahraun": (64.07763129311066, -21.942765716339103),
        "Krónan Hvaleyrarbraut": (64.06344469095414, -21.965596678979097),
        "Krónan Norðurhella": (64.04673427118828, -21.983942988771656),
        "Krónan Skeifan": (64.13047013989885, -21.872698450597895)
    }

    locations_demand = {
        "DC": 0,
        "Krónan Grafarholt": 57,
        "Krónan Mosfellsbær": 60,
        "Krónan Bíldshöfi": 80,
        "Krónan Árbær": 40,
        "Krónan Jafnarsel":  62,
        "Krónan Vallarkór": 62,
        "Krónan Lindir":  78,
        "Krónan Grandi": 80,
        "Krónan Hallveigarstígur": 43,
        "Krónan Borgartún": 55,
        "Krónan Austurver": 35,
        "Krónan Hamraborg":  35,
        "Krónan Garðabær":  10,
        "Krónan Flatahraun":  60,
        "Krónan Hvaleyrarbraut":  62,
        "Krónan Norðurhella":  61,
        "Krónan Skeifan": 72
    }

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


    # Create distance matrix
    distance_matrix = []
    for i in locations_coords:
        row = []
        for j in locations_coords:
            row.append(round(haversine(locations_coords[i], locations_coords[j]), 2))  # Distance rounded to two decimal places
        distance_matrix.append(row)


    print(distance_matrix)
    data = {}

    data["distance_matrix"] = distance_matrix

    locations_demand = [
        0,
        57,
         60,
        80,
        40,
        62,
         62,
          78,
         80,
         43,
         55,
         35,
          35,
          10,
          60,
          62,
        61,
        72
    ]




    #data["demands"] = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    data["demands"] = locations_demand
    data["vehicle_capacities"] = [500, 500]
    data["num_vehicles"] = 2
    data["depot"] = 0
    return data


def print_solution_bla(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")

    locations = [
        "DC",
        "Krónan Grafarholt",
        "Krónan Mosfellsbær",
        "Krónan Bíldshöfi",
        "Krónan Árbær",
        "Krónan Jafnarsel",
        "Krónan Vallarkór",
        "Krónan Lindir",
        "Krónan Grandi",
        "Krónan Hallveigarstígur",
        "Krónan Borgartún",
        "Krónan Austurver",
        "Krónan Hamraborg",
        "Krónan Garðabær",
        "Krónan Flatahraun",
        "Krónan Hvaleyrarbraut", 
        "Krónan Norðurhella",
        "Krónan Skeifan"
    ]

    locations_coords = {
        "DC": (64.12238188422718, -21.80556258041812),
        "Krónan Grafarholt": (64.13060762774467, -21.7616648461748),
        "Krónan Mosfellsbær": (64.16676053874438, -21.69815013762845),
        "Krónan Bíldshöfi": (64.12663767072458, -21.81462238088484),
        "Krónan Árbær": (64.11727231871421, -21.78990314307976),
        "Krónan Jafnarsel": (64.09889301241216, -21.826971272553056),
        "Krónan Vallarkór": (64.0854487078441, -21.822379330997656),
        "Krónan Lindir": (64.10251080254932, -21.873620252057236),
        "Krónan Grandi": (64.15864328795905, -21.949117186999928),
        "Krónan Hallveigarstígur": (64.1475671399666, -21.936757566966456),
        "Krónan Borgartún": (64.14831566757304, -21.898992064855193),
        "Krónan Austurver": (64.13139401690862, -21.88937902795415),
        "Krónan Hamraborg": (64.11491170786942, -21.905171874291582),
        "Krónan Garðabær": (64.09941317124606, -21.909806731692516),
        "Krónan Flatahraun": (64.07763129311066, -21.942765716339103),
        "Krónan Hvaleyrarbraut": (64.06344469095414, -21.965596678979097),
        "Krónan Norðurhella": (64.04673427118828, -21.983942988771656),
        "Krónan Skeifan": (64.13047013989885, -21.872698450597895)
    }




def print_solution(data, manager, routing, solution):
    """Prints solution on console and generates a map for each route."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    total_load = 0
    
    locations_coords = {
        "DC": (64.12238188422718, -21.80556258041812),
        "Krónan Grafarholt": (64.13060762774467, -21.7616648461748),
        "Krónan Mosfellsbær": (64.16676053874438, -21.69815013762845),
        "Krónan Bíldshöfi": (64.12663767072458, -21.81462238088484),
        "Krónan Árbær": (64.11727231871421, -21.78990314307976),
        "Krónan Jafnarsel": (64.09889301241216, -21.826971272553056),
        "Krónan Vallarkór": (64.0854487078441, -21.822379330997656),
        "Krónan Lindir": (64.10251080254932, -21.873620252057236),
        "Krónan Grandi": (64.15864328795905, -21.949117186999928),
        "Krónan Hallveigarstígur": (64.1475671399666, -21.936757566966456),
        "Krónan Borgartún": (64.14831566757304, -21.898992064855193),
        "Krónan Austurver": (64.13139401690862, -21.88937902795415),
        "Krónan Hamraborg": (64.11491170786942, -21.905171874291582),
        "Krónan Garðabær": (64.09941317124606, -21.909806731692516),
        "Krónan Flatahraun": (64.07763129311066, -21.942765716339103),
        "Krónan Hvaleyrarbraut": (64.06344469095414, -21.965596678979097),
        "Krónan Norðurhella": (64.04673427118828, -21.983942988771656),
        "Krónan Skeifan": (64.13047013989885, -21.872698450597895)
    }

    locations = [
        "DC",
        "Krónan Grafarholt",
        "Krónan Mosfellsbær",
        "Krónan Bíldshöfi",
        "Krónan Árbær",
        "Krónan Jafnarsel",
        "Krónan Vallarkór",
        "Krónan Lindir",
        "Krónan Grandi",
        "Krónan Hallveigarstígur",
        "Krónan Borgartún",
        "Krónan Austurver",
        "Krónan Hamraborg",
        "Krónan Garðabær",
        "Krónan Flatahraun",
        "Krónan Hvaleyrarbraut", 
        "Krónan Norðurhella",
        "Krónan Skeifan"
    ]

    # Initialize the map
    map_all_routes = folium.Map(location=[64.14, -21.9], zoom_start=11)
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'darkblue', 'darkred', 'cadetblue', 'darkgreen']

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
        folium.PolyLine(points, color=route_color, weight=2.5, opacity=1).add_to(map_all_routes)
        for point in points:
            folium.CircleMarker(point, radius=5, color=route_color, fill=True, fill_color=route_color).add_to(map_all_routes)

        total_distance += route_distance
        total_load += route_load

    # Save the map with all routes to an HTML file
    map_all_routes.save('all_routes.html')

    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")










def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

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

    # Add Capacity constraint.
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

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)


if __name__ == "__main__":
    main()