# import Libraries
import requests
import json
import os

# call  API
url = 'https://api.tfl.gov.uk/BikePoint'
response = requests.get(url)

if response.status_code == 200:
    # if the response is successful, save the json response into a data variable
    data = response.json()
    # extract a list of id values for all bikes
    id = [item.get('id') for item in data]

    # iterate through the ids and request individual bike data
    for bp in id: 
        endpoint = url + '/' + bp
        endpoint_response = requests.get(endpoint)
        endpoint_data = endpoint_response.json()

        # get modified time stamp to name our file
        first_value = endpoint_data['additionalProperties'][0]
        modified = first_value.get('modified')
        modified = modified.replace(":", "-")
        modified = modified.replace(".", "-")

        file_list = [f for f in os.listdir('.') if f.endswith('.json')]
        
        filename = modified + bp + '.json'

        # if the file already exists, just print an up to date message
        if filename in file_list:
            print('Up to date')
        else:
        # otherwise create the file
            with open(filename, 'w') as file:
                json.dump(endpoint_data,file)
        
else:
    # error handling
    data = response.json()
    error_message = data.get("message", "No message provided.")
    print(f'Error {response.status_code}:{error_message}')
