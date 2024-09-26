import pandas as pd
import json

# List of full paths to your CSV files
file_paths = [
    '/home/afarjana/SE4DL/bipython.csv',
    '/home/afarjana/SE4DL/netbox.csv',
    '/home/afarjana/SE4DL/beets.csv',
    '/home/afarjana/SE4DL/conda.csv',
    '/home/afarjana/SE4DL/prefect.csv',
    '/home/afarjana/SE4DL/pyload.csv'
]

# Initialize a list to store all method codes
all_method_codes = []

# Read each file and extract the "Method code" column
for path in file_paths:
    df = pd.read_csv(path)
    # Assuming 'Method code' column exists and I only want to extract this column
    method_codes = df['Method Code'].tolist()  # Convert column to list
    all_method_codes.extend(method_codes)  # Add to the master list

# Convert the list of method codes to JSON
json_data = json.dumps(all_method_codes, indent=4)

# Print first few entries to check the data
print("Sample of the JSON data:")
print(json.dumps(all_method_codes[:5], indent=4))  # Using slice [:5] to display more or less data

# Specify the directory and filename where I want to save the JSON file
save_path = '/home/afarjana/SE4DL/Dataset_methods.json'  # Desired file path

# Write the JSON data to the file at the specified path
with open(save_path, 'w') as json_file:
    json_file.write(json_data)

print(f"JSON file created successfully at {save_path}")
