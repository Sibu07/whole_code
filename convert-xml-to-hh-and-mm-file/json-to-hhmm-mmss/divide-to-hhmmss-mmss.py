######################################################
# Filename: divide-to-hhmmss-mmss.py
# Purpose: This code fetches call details from a specified URL,
#          processes the data, and saves the processed results
#          as separate JSON files. It also includes functions to
#          convert different duration formats.
# Author: Sibu
# Date: May 25, 2023
######################################################

import json
import random
import requests

# Function to convert mm:ss or hh:mm:ss duration format to hh:mm:ss format
def convert_mmss_to_hhmmss(duration):
    if ':' not in duration:
        raise ValueError("Invalid duration format. Expected format: 'mm:ss' or 'hh:mm:ss'")
    
    parts = duration.split(':')
    if len(parts) == 2:
        # duration is in mm:ss format
        minutes, seconds = int(parts[0]), int(parts[1])
        if minutes < 60:
            # duration is less than 1 hour
            return f"{minutes:02d}:{seconds:02d}"
        else:
            # duration is 1 hour or more
            hours = minutes // 60
            minutes = minutes % 60
            return f"{hours:01d}:{minutes:02d}:{seconds:02d}"
    elif len(parts) == 3:
        # duration is already in hh:mm:ss format
        return duration
    else:
        raise ValueError("Invalid duration format. Expected format: 'mm:ss' or 'hh:mm:ss'")

# Function to convert duration in seconds to hh:mm:ss format
def convert_seconds_to_hhmmss(duration):
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60

    if hours == 0:
        return f"{minutes:02d}:{seconds:02d}"
    else:
        return f"{hours:01d}:{minutes:02d}:{seconds:02d}"

# Prompt the user to enter the fetch URL
fetch_url = input("Enter the fetch URL: ")

try:
    # Fetch data from the specified URL
    response = requests.get(fetch_url)
    response.raise_for_status()
    json_data = json.loads(response.content)
except requests.exceptions.RequestException as e:
    print("Error: Unable to fetch data from the URL.")
    print(e)
    json_data = []

try:
    # Load existing data from data_hhmmss.json file if it exists
    with open('data_hhmmss.json', 'r') as f:
        data_hhmmss = json.load(f)
except FileNotFoundError:
    data_hhmmss = []
except json.decoder.JSONDecodeError:
    print("Error: Invalid JSON format in the file.")
    data_hhmmss = []

try:
    # Load existing data from data_mmss.json file if it exists
    with open('data_mmss.json', 'r') as f:
        data_mmss = json.load(f)
except FileNotFoundError:
    data_mmss = []
except json.decoder.JSONDecodeError:
    print("Error: Invalid JSON format in the file.")
    data_mmss = []

# Process each item in the fetched JSON data
for item in json_data:
    call_duration = item['call_duration']
    time = item['time']

    try:
        # Convert the call duration to the desired format
        if ':' in call_duration:
            # Duration is in hh:mm:ss or mm:ss format
            call_duration = convert_mmss_to_hhmmss(call_duration)
        else:
            # Duration is in seconds format
            call_duration = convert_seconds_to_hhmmss(int(call_duration))
    except ValueError as e:
        print(e)
        continue

    # Generate random values for internet speed and mobile charge
    internet_speed = round(random.uniform(0.1, 9.1), 1)
    mobile_charge = str(random.randint(10, 90))

    # Create a dictionary for the processed call data
    call_data = {
        "time": time,
        "Internet_speed": str(internet_speed),
        "call_duration": call_duration,
        "mobile_charge": mobile_charge.replace("\"", "\\\"")
    }

    # Append the call data to the appropriate list based on duration format
    if len(call_duration.split(':')) == 3:
        data_hhmmss.append(call_data)
    else:
        data_mmss.append(call_data)

# Save the processed data to separate JSON files
with open('data_hhmmss.json', 'w') as f:
    json.dump(data_hhmmss, f)

with open('data_mmss.json', 'w') as f:
    json.dump(data_mmss, f)

print("Data saved successfully.")
