import requests
import json

# Define the API endpoint and payload
url = "http://127.0.0.1:3000/upload_score"  # API endpoint for the JS server
headers = {'Content-Type': 'application/json'}  # Define headers, if needed
payload = {
  "Minimum": 123,
  "Maximum": 456,
  "Average": 3000,
  "Score": 0.75,
  "timestamp": "2024-09-10T14:37:00"
}

# Convert payload to JSON format
data = json.dumps(payload)

# Send POST request
response = requests.post(url, headers=headers, data=data)

# Check the response
if response.status_code == 200:
    print("Request successful")
    print("Response data:", response.json())
else:
    print("Request failed")
    print("Status code:", response.status_code)
    print("Response text:", response.text)
