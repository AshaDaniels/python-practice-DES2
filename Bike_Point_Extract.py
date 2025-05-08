import requests
import json

url = 'https://api.tfl.gov.uk/BikePoint/BikePoints_1'
id = 'BikePoints_1'

response = requests.get(url)

if response.status_code == 200:
    #save the json response into a data variable
    data = response.json()

    #get modified time stamp to help us name our file
    first_value = data['additionalProperties'][0]
    modified = first_value.get('modified')
    modified = modified.replace(":", "-")
    modified = modified.replace(".", "-")

    filename = modified + id + '.json'

    with open(filename, 'w') as file:
        json.dump(data,file)
    
else:
    # Returns a cleaner error message
    data = response.json()
    error_message = data.get("message", "No message provided.")
    print(f'Error {response.status_code}:{error_message}')
