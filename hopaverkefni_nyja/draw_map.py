
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
    
import folium

# Extract all coordinates
coords = locations_coords.values()

# Calculate the average latitude and longitude to center the map
avg_lat = sum([lat for lat, _ in coords]) / len(coords)
avg_lon = sum([lon for _, lon in coords]) / len(coords)

# Create a folium map centered around the average coordinates
m = folium.Map(location=(avg_lat, avg_lon), zoom_start=12)

# Define a function to scale the demand value to a suitable radius for visualization
def scale_demand_to_radius(demand_value):
    return demand_value / 3 # This is just an example scale. Adjust as necessary.

# Add a circle for each location, with the radius proportional to the demand
for location, (lat, lon) in locations_coords.items():
    demand = locations_demand_dict[location]
    radius = scale_demand_to_radius(demand)
    
    folium.CircleMarker(
        location=(lat, lon),
        radius=radius,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.6,
        popup=f"{location}: Demand {demand}",
    ).add_to(m)

# Save the map to an HTML file or display it in Jupyter
m.save('map.html')
