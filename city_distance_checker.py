import csv, sys, os
import geopy.distance
from geopy.geocoders import Nominatim
from tqdm import tqdm

geolocator = Nominatim(user_agent="city_distance_checker")
location_cache = {}
distance_cache = {}

def is_within_radius(city, state, reference_location, radius):
    try:
        if (city, state) in distance_cache:
            return distance_cache[(city, state)] <= radius

        if (city, state) in location_cache:
            city_coords = location_cache[(city, state)]
        else:
            city_location = geolocator.geocode(f"{city}, {state}")
            city_coords = (city_location.latitude, city_location.longitude)
            location_cache[(city, state)] = city_coords

    except Exception as e:
        print(f"Error getting location for {city}, {state}: {e}")
        return False

    distance = geopy.distance.distance(city_coords, reference_location).miles
    distance_cache[(city, state)] = distance

    return distance <= radius

def get_coordinates(city, state):
    try:
        location = geolocator.geocode(f"{city}, {state}")
        city_coords = (location.latitude, location.longitude)
        distance_cache[(city, state)] = 0 # set cache for initial city
        location_cache[(city, state)] = city_coords # set cache for initial city
        return city_coords
    except Exception as e:
        print(f"Error getting location for {city}, {state}: {e}")
        return None, None


def main():
    try:
        ref_city = input("Enter the reference city: ")
        ref_state = input("Enter the reference state: ")
        radius = int(input("Enter the radius (in miles): "))
        ref_coords = get_coordinates(ref_city, ref_state)  # Get coordinates for the reference city
        if ref_coords == (None, None):
            print("Could not get coordinates for reference city. Exiting...")
            sys.exit(1)
        print(f"Coordinates for {ref_city}, {ref_state}: {ref_coords}")
        input_file = input("\nEnter the input file name: ")
        output_file = input("Enter the output file name: ")
        print() # adding newline 
        within_radius_column_name = f"within_{radius}_miles_of_{ref_city.replace(' ', '_')}"

        results = []

        with open(input_file, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            pbar = tqdm(reader, unit="cities", desc="Cities processed")
            
            for row in pbar:
                person = row["person"]
                city = row["city"]
                state = row["state"]

                within_radius = is_within_radius(city, state, ref_coords, radius)
                
                row[within_radius_column_name] = within_radius
                results.append(row)
                
                tqdm.write(f"{person}, {city}, {state}, within_radius: {within_radius}")

        with open(output_file, "w", newline='') as csvfile:
            fieldnames = ["person", "city", "state", within_radius_column_name]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in results:
                writer.writerow(row)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    main()
