import pandas as pd
import csv
import iso3166

# Get the list of country names
country_list = iso3166.countries_by_alpha3

# Load dataset
countries_df = pd.read_json("Countries.json")



# Define a dictionary to store distances
distances = {}

# Read the CSV file containing distances
with open('CSV Files/distances.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Read the header row

    # Build the distances dictionary
    for row in reader:
        country1 = row[0]  # The first column contains the country codes
        if country1 in country_list:  # Only process relevant countries
            distances[country1] = {}
            for i, distance in enumerate(row[1:], start=1):
                country2 = headers[i]
                if country2 in country_list:
                    distances[country1][country2] = float(distance) if distance != '?' else None

# Define the general function
def calc_index(country1, country2):
    """
    Returns the distance between two countries based on the CSV data.
    """
    if country1 in distances and country2 in distances[country1]:
        return distances[country1][country2]
    elif country2 in distances and country1 in distances[country2]:
        return distances[country2][country1]
    else:
        return None  # Distance not available


# Example usage
print(calc_index('ABW', 'AFG'))