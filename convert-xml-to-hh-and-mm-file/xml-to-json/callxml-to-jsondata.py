######################################################
# Filename: callxml-to-jsondata.py
# Purpose: This code extracts call details from an XML file
#          based on a provided phone number and saves the
#          details as a JSON file.
# Author: Sibu
# Date: May 25, 2023
######################################################

import xml.etree.ElementTree as ET
import json
import datetime

# Parse the XML file
tree = ET.parse('calls.xml')
root = tree.getroot()

# Prompt the user to enter the phone number
number = input("Enter the phone number: ")

calls = []

# Extract call details for the provided phone number
for call in root.findall(".//call[@number='{}']".format(number)):
    duration = call.get('duration')
    if duration != "0":
        date_time_str = call.get('readable_date')
        date_time_obj = datetime.datetime.strptime(date_time_str, '%d-%b-%Y %I:%M:%S %p')
        time_str = date_time_obj.strftime('%I:%M %p').lstrip('0')
        call_data = {
            "time": time_str,
            "call_duration": duration           
        }
        calls.append(call_data)

# Prompt the user to enter the output file name
filename = input("Enter the output file name: ")

# Ensure the file name ends with ".json"
if not filename.endswith(".json"):
    filename += ".json"

# Save the call details as a JSON file
with open(filename, 'w') as f:
    json.dump(calls, f)

print("Call details written to", filename)
