# Testing basic pixela graphing, may use for visual tracking


import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.environ['USERNAME']
TOKEN = os.environ['TOKEN']
GRAPH_ID = os.environ['GRAPH_ID']

pixela_endpoint = "https://pixe.la/v1/users"

# Create Graph
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": GRAPH_ID,
    "name": "Conquer Tracker",
    "unit": "tasks",
    "type": "int",
    "color": "ajisai",
    "startOnMonday": True
}

headers = {
    "X-USER-TOKEN": TOKEN,
}

# Call to create
# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

# Link to view
# view_graph = f"{graph_endpoint}/{GRAPH_ID}.html"

# Call to add value to graph
add_data_endpoint = f"{graph_endpoint}/{GRAPH_ID}"

today = datetime.now()
today_str = today.strftime("%Y%m%d")

add_today = {
    "date": today_str,
    "quantity": "3"
}

response = requests.post(url=add_data_endpoint, json=add_today, headers=headers)
print(response.text)