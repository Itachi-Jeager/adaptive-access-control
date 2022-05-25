"""This module contains the implementation for the Chinese wall Policy
and Access Control Module.
"""
import catboost as cat
from pymongo import MongoClient
from datetime import time
import random


class ChineseWallPolicy(object):
    """Module for the chinese wall Policy

    This class contains methods that check the user's
    activity upon access granted, and returns zone data
    When the user is logged into with the correct credentials

    """

    def __init__(self, user_name, mongodb_client) -> None:
        self.user_name = user_name
        self.mongodb_client = mongodb_client

    def check_user_activity(self) -> list:
        user_db = self.mongodb_client.access_control
        
        count_logins = user_db["user_info"].count_documents({"user_name": self.user_name})
        
        queried_zones = []
        if count_logins == 1:
            find_user = user_db["user_info"].find_one({"user_name": self.user_name})
            queried_zones.append(find_user["resource_zone"])
            return queried_zones

        elif count_logins > 1:
            find_user = user_db["user_info"].find({"user_name": self.user_name})
            
            for user in find_user:
                queried_zones.append(user["resource_zone"])

            return queried_zones

        else:
            return queried_zones
           

    def query_resource_data(self, requested_zone: str):
        user_db = self.mongodb_client.access_control

        find_content = user_db['zone_data'].find({"zone": requested_zone})

        results = []

        for content in find_content:
            results.append(content)
        return results


    def wall_policy(self, resource_zone):
        zones_queried = self.check_user_activity()

        if len(zones_queried) == 1:
            zone_results = self.query_resource_data(resource_zone)
            return zone_results
            

        elif len(zones_queried) > 1 and zones_queried[0] == resource_zone:
            zone_results = self.query_resource_data(resource_zone)
            return zone_results

        elif len(zones_queried) > 1 and zones_queried[0] != resource_zone:
            return f"access denied to resources at {zones_queried[-1]}"

        elif len(zones_queried) > 1 and zones_queried[0] != zones_queried[-1]:
            return f"access denied to resources at {zones_queried[-1]}"

        else:
            return "empty list"

    pass


class AccessControlModule(object):
    def __init__(self, user_name, user_password, resource_zone, severity_action, mongodb_client,  sensitivity_resource=9000, history_of_risk = 118295) -> None:
        self.user_name = user_name
        self.user_pass = user_password
        self.sensitivity_resource = sensitivity_resource
        self.resource_zone = resource_zone
        self.risk_history = history_of_risk
        self.action_severity = severity_action
        self.mongodb_client = mongodb_client

    def generate_user_context(self, user_name, user_password):

        pass

    def check_user(self):
        """A function for checking if user exists

        This function goes through a list of IDs, to find if the
        ID supplied exists in the list, it it doesn't it appends
        to the list. May need to use a database for this later.
        The Zone the ID has would be used to determine how it is 
        limited

        Args:
            context (str): The user identifier
        """


        user_db = self.mongodb_client.access_control
        find_user = user_db["user_info"].find_one({"user_name": self.user_name, "resource_zone": self.resource_zone})

        if find_user is not None:
            
            print("Welcome back User")
            # print(f"Details: {find_user}")
            return find_user
        else:
        
            print("Registering new user")
            if len(self.user_name) > 8 and len(self.user_pass) > 8:
                generate_context = random.randint(75000, 100000)

            else:
                generate_context = random.randint(25000, 50000)
            new_user = {"user_name": self.user_name,
                        "resource_zone": self.resource_zone,
                        "risk_history": self.risk_history,
                        "user_context": generate_context}
            new_user_db = user_db["user_info"].insert_one(new_user)
            # add user details to the database
            return new_user

    def update_risk_history(self, risk_probability) -> int:
        user_db = self.mongodb_client.access_control

        new_risk_history = int(self.risk_history * risk_probability[1])

        result = user_db['user_info'].update_one({'user_name': self.user_name, 'resource_zone': self.resource_zone}, {'$inc': {'risk_history': new_risk_history}})
        
        return result.modified_count

    def risk_assess_module(self):
        loaded_model = cat.CatBoostClassifier()

        loaded_model.load_model("proposed_model")

        user_dict = self.check_user()

        user_data = [user_dict["user_context"], self.sensitivity_resource, self.action_severity, user_dict["risk_history"]]

        prediction = loaded_model.predict(user_data)

        prediction_probability = loaded_model.predict_proba(user_data)

        update_user_risk = self.update_risk_history(prediction_probability)

        return prediction, prediction_probability, update_user_risk



# if __name__ == "__main__":
#     with MongoClient("mongodb://localhost:27017") as client:
#         checking_user = AccessControlModule(18913,273476,"zone B", 310732,client, 19721)
#         user_acesss, user_risk = checking_user.risk_assess_module()
#         print(user_acesss, user_risk)
#         # process_users = ChineseWallPolicy(34687, client)
#         # user_zones = process_users.wall_policy()
#         # print(user_zones)
#         # fails [18913,273476,310732,19721]
