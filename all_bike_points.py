# Import Libraries
import requests  # For making HTTP requests to fetch data from APIs
import json  # For working with JSON data
import os  # For interacting with the operating system, e.g., file handling
import boto3
from dotenv import load_dotenv
from load_test import load_to_s3

load_dotenv()

access_key = os.getenv('AWS_ACCESS_KEY')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_access_key
)

# Call the API
url = 'https://api.tfl.gov.uk/BikePoint'  # URL of the API endpoint to fetch bike point data
response = requests.get(url)  # Send a GET request to the API

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON response into a Python dictionary

    # Count the number of bike points
    number_of_bike_points = len([item.get('id') for item in data])

    # Iterate through each bike point
    for i in range(0, number_of_bike_points):
        bike_point = data[i]  # Get the bike point data for the current index

        # Get the first additional property and process its 'modified' value
        first_value = bike_point['additionalProperties'][0]  # Access the first additional property
        modified = first_value.get('modified')  # Retrieve the 'modified' timestamp
        # Replace problematic characters in the 'modified' value to make it file-system friendly
        modified = modified.replace(":", "-")
        modified = modified.replace(".", "-")

        # Get a list of all JSON files in the current directory
        file_list = s3_client.list_objects_v2(Bucket = bucket)

        # Get the bike point's ID
        bp = bike_point.get('id')
        
        # Create a filename using the modified timestamp and bike point ID
        filename = modified + bp + '.json'

        s3_contents = s3_client.list_objects_v2(Bucket = bucket)
        file_list = [item['Key'] for item in file_list.get('Contents', [])]

        # Check if the file already exists in the directory
        if filename in file_list:
            print('Up to date')  # Indicate the file is up to date
        else:
            # Otherwise, create the file
            with open(filename, 'w') as file:
                json.dump(bike_point, file)  # Write the bike point data to a JSON file
            #Run function created in load_test.py
            load_to_s3(filename)
            print('Uploaded ' + filename)

else:
    # Handle errors if the API request was not successful
    data = response.json()  # Parse the JSON response
    error_message = data.get("message", "No message provided.")  # Get the error message
    print(f'Error {response.status_code}:{error_message}')  # Print the error code and message
    
