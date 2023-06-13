# City Distance Checker

This script allows you to check if people from a CSV file live within a specified radius of a given city. The script will update the CSV file with a new column that indicates whether each person is within the specified radius.

## Requirements
1. Python 3.x
2. Geopy library
3. Tqdm library

To install these libraries, you can use the following commands:

```
pip install geopy
pip install tqdm
```

## Usage
To run the script, use the command:
```
python city_distance_checker.py
```

You will be prompted to enter:

1. The reference city
2. The reference state
3. The radius (in miles)
4. The input file name
5. The output file name

Example:
```
Enter the reference city: San Francisco
Enter the reference state: CA
Enter the radius (in miles): 100
Enter the input file name: sample-data.csv
Enter the output file name: results.csv
```


The input CSV file should contain at least the following columns: `person`, `city`, `state`. Here is a sample:

```csv
person,city,state
John Doe,San Francisco,CA
Jane Smith,Los Angeles,CA
```

## Output
The script will create an output CSV file with the same content as the input file, plus an additional column that indicates whether each person lives within the specified radius of the reference city. The name of the new column will be `within_[radius]_miles_of_[city]`. For example, if the reference city is San Francisco and the radius is 100 miles, the new column will be `within_100_miles_of_San_Francisco`.
Example output:
```csv
person,city,state,within_100_miles_of_San_Francisco
John Doe,San Francisco,CA,True
Jane Smith,Los Angeles,CA,False
```

## Caching
The script caches geolocation and distance data to improve performance. The cache is not persistent and will be cleared when the script finishes running.

## Error Handling
If the script can't find the geolocation data for a city or state, it will print an error message and consider that the person does not live within the radius.