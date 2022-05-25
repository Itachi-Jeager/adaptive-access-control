"""This model will contain the mappings for the Zones and IDs
"""

# resources
"""This resources should contain information about resources available
Zone A: Some Data
Zone B: Some other Data
Zone C: Other Data
"""
import requests
from pprint import pprint
import json

ACTION_SEVERITY = {
                    'read': 117906,
                    'create': 240983,
                    'update': 117913,
                    'delete': 279443
}

# get rick and morty data
# rick_response = requests.get('https://rickandmortyapi.com/api/character')

# rick_json = rick_response.json()['results']

# # parse JSON response
# rick_and_morty_data = json.dumps(rick_json)

# # write the response to file
# with open("../resources/rick characters.json", "w") as outfile:
#     outfile.write(rick_and_morty_data)



    