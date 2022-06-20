"""
This module contains the operations used to test and populate the database.

The operations are single use, and should only be run once.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
import pymongo
from pprint import pprint
import json
import pandas as pd

load_dotenv()

my_db = os.getenv("MONGODB_ATLAS")

client = MongoClient(my_db)
scraped_db = client.local

# scrapes = scraped_db["monday_scrape"].find_one({"title": "INCESSANT BODY PAINS. WHY? nine"})
# # scraped_db["pie_scraped"].

# # for item in scrapes:
# #     print(item)

# print(scrapes)

# insert dummy zone A data into the database
# with open('resources/location_data.json', 'r') as j:
#     location_data = json.loads(j.read())

# for location in location_data:
#     location['zone'] = 'zoneA'

# # print(location_data)

# access_control = client.access_control
# zone_collection = access_control['zone_data']
# zone_collection.insert_many(location_data)

# insert dummy zone B data into the database
# with open('resources/titan_data.json', 'r') as j:
#     titan_data = json.loads(j.read())

# for titan in titan_data:
#     titan['zone'] = 'zone C'

# # print(location_data)

# access_control = client.access_control
# zone_collection = access_control['zone_data']
# zone_collection.insert_many(titan_data)

# # insert dummy zone B data into the database
# with open('resources/rick_characters.json', 'r') as j:
#     rick_data = json.loads(j.read())

# for character in rick_data:
#     character['zone'] = 'zone B'

# # print(location_data)

# access_control = client.access_control
# zone_collection = access_control['zone_data']
# zone_collection.insert_many(rick_data)

# test mongo db data in a dataframe
# access_control = client.access_control
# zone_a_data = access_control['zone_data'].find({"zone": "zoneA"}, {'_id': False})
# list_type = list(zone_a_data)
# # my_df = pd.DataFrame(zone_a_data)
# print(list_type)

