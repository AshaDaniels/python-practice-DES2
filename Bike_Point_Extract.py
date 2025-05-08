import requests
import json
import os

url = 'https://api.tfl.gov.uk/BikePoint'
response = requests.get(url)

if response.status_code == 200:
    #save the json response into a data variable
    data = response.json()
    id = [item.get('id') for item in data]

    for bp in id: 
        endpoint = url + '/' + bp
        endpoint_response = requests.get(endpoint)
        endpoint_data = endpoint_response.json()

        #get modified time stamp to help us name our file
        first_value = endpoint_data['additionalProperties'][0]
        modified = first_value.get('modified')
        modified = modified.replace(":", "-")
        modified = modified.replace(".", "-")

        file_list = [f for f in os.listdir('.') if f.endswith('.json')]
        
        filename = modified + bp + '.json'

        if filename in file_list:
            print('Up to date')
        else:
            with open(filename, 'w') as file:
                json.dump(endpoint_data,file)
        
else:
    # Returns a cleaner error message
    data = response.json()
    error_message = data.get("message", "No message provided.")
    print(f'Error {response.status_code}:{error_message}')
