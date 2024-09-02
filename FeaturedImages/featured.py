import requests
import json
import pandas as pd
import time

# Constants
RATE_LIMIT = 60  # max requests per minute
REQUEST_INTERVAL = 60 / RATE_LIMIT  # interval in seconds

def send_request(img, title, api_key):
    try:
        initial_response = requests.post(
            url="https://api.placid.app/api/rest/images",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
                "template_uuid": "t2rsm7ap6fybd",
                "layers": {
                    "img": {
                        "image": img
                    },
                    "title": {
                        "text": title
                    }
                }
            })
        )

        response_json = initial_response.json()
        if initial_response.status_code == 200 and 'polling_url' in response_json:
            polling_url = response_json['polling_url']
            return poll_until_image_generated(polling_url, api_key)
        else:
            print(f"Failed to queue image generation: {response_json}")
            return None
    except requests.exceptions.RequestException as e:
        print(f'HTTP Request to Placid API failed: {e}')
        return None

def poll_until_image_generated(polling_url, api_key):
    while True:
        try:
            response = requests.get(
                url=polling_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                }
            )
            response_json = response.json()
            if response.status_code == 200:
                if response_json['status'] == 'done' and 'image_url' in response_json:
                    return response_json['image_url']
                elif response_json['status'] == 'finished' and 'image_url' in response_json:
                    return response_json['image_url']
                elif response_json['status'] == 'failed':
                    print(f"Image generation failed: {response_json}")
                    return None
                else:
                    print(f"Still processing: {response_json['status']}")
            time.sleep(2)  # Sleep for 2 seconds before polling again
        except requests.exceptions.RequestException as e:
            print(f'Polling request failed: {e}')
            return None

def process_csv(file_path, api_key):
    # Try reading the CSV file with different encodings
    encodings_to_try = ['utf-8', 'ISO-8859-1', 'latin1']
    for enc in encodings_to_try:
        try:
            data = pd.read_csv(file_path, encoding=enc)
            print(f'Successfully read the CSV file with "{enc}" encoding.')
            break
        except UnicodeDecodeError:
            print(f'Failed to read the CSV file with "{enc}" encoding.')
    else:
        raise ValueError("None of the tried encodings could read the CSV file.")
    
    # Ensure 'featured' column exists
    if 'featured' not in data.columns:
        data['featured'] = ""
    
    # Loop through each row in the CSV and send a request for each row
    for index, row in data.iterrows():
        img = row['img']
        title = f"{row['title']}"
        image_url = send_request(img, title, api_key)
        if image_url:
            data.at[index, 'featured'] = image_url
            # Update the CSV file each time a new URL is generated successfully
            data.to_csv(file_path, index=False, encoding=enc)
        else:
            print(f"Failed to process row: {row['title']} with img: {img}")
        
        # Rate limiting
        time.sleep(REQUEST_INTERVAL)

# Replace 'path_to_your_csv_file.csv' with the path to your CSV file
# Replace 'your_actual_api_key' with your actual API key
csv_file_path = 'input.csv'
api_key = 'placid-x9s2lbrizcnvlf6n-fevqnpilgjglkj0g'
process_csv(csv_file_path, api_key)