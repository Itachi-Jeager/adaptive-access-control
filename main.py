"""This will be the main script that houses streamlit app
    """

from dotenv import load_dotenv
import pandas as pd
import os
import streamlit as st
from pymongo import MongoClient
from app.access_control_module import ChineseWallPolicy, AccessControlModule
import app.models as models

load_dotenv()

my_db = os.getenv("MONGODB_ATLAS")


# TODO: Display time
# TODO: Display location
# TODO: make the database data appear in a dataframe
# TODO: add update data functionality
# TODO: add create data functionality
# TODO: try normalization/ standard scaler

# app name
st.title("The Risk Based Access Control Module")

# app image
st.image("https://source.unsplash.com/vO9-gal54go/640x426")

# Welcome message
st.subheader(
    """
    Welcome to the interface for simulating access requests to the\
    Adaptive Risk Based Access Control System. 
    Please supply a Username and Password , Resource Zone (dropdown), User Action.
    
    """
)

collect_user_name = st.text_input(
    'User Name',
    
)

collect_user_pass = st.text_input(
    'Password', type="password"
)

# Add select box to choose what zone resource
collect_resource_zone = st.selectbox(
    'Resource Zone',
    ('zone A', 'zone B', 'zone C')
)

# Add number input to the sidebar to collect user context 
# collect_user_context = st.sidebar.number_input(
#     'User Context (ID)', value=0
# )

# Add number input to the sidebar to collect resource sensitivity 
# collect_resource_sensitivity = st.sidebar.number_input(
#     'Resource Sensitivity',
#     value=800
# )


def action_severity_callback():
    """A streamlit callback which uses state to query a mapping

    Fetches the session state for action severity and uses it
    to fetch its number equivalent

    Returns:
        action_number(int): the number mapping to the action selected
    """
    # fetch session state
    chosen_action = st.session_state.action_state
    # change the state to lower case
    lower_case_chosen_action = chosen_action.lower()
    # query action severity
    action_number = models.ACTION_SEVERITY[lower_case_chosen_action]
    
    return action_number


# Add selectbox with key and callback to get user action
collect_user_action_severity = st.selectbox(
    'User Action Severity',
    ('Read', 'Create', 'Update', 'Delete'),
    key='action_state',
    on_change=action_severity_callback,
)

# # Add number input box
# collect_user_risk_history = st.sidebar.number_input(
#     'User Risk History',
#     value=118424
# )
# Functionality to the center of the page

# action if request access button is clicked
if st.button("Request Access"):
    # collect current action severity
    collector = action_severity_callback()
    
    # open a connection to the database
    st.write(f'Risk Module Running with action {collect_user_action_severity}')
    with MongoClient(my_db) as client:
        checking_user = AccessControlModule(collect_user_name,
                                           collect_user_pass,
                                           collect_resource_zone, 
                                            collector,
                                            client,
                                            )
        # retrieve processing results
        user_access, user_risk, update_status = checking_user.risk_assess_module()
    # access granted flow
    if user_access == 1:
        st.write("Access Granted")
        st.write(f" Welcome Device {collect_user_name}")
        st.write(f"You have requested Resource at {collect_resource_zone}")
        
        # open another connection to the database to retreive requested zone
        with MongoClient(my_db) as client:
            process_users = ChineseWallPolicy(collect_user_name, client)
            user_zones = process_users.wall_policy(collect_resource_zone)
            
        
        if type(user_zones) == str:
            st.write(user_zones)

        else:
            my_df = pd.DataFrame(user_zones)
        st.dataframe(my_df)

    else:
        st.write("Access Denied")


# left_column, right_column = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column.write("There be a column here")
    




# # Or even better, call Streamlit functions inside a "with" block:
# # with right_column:
# #     chosen = st.radio(
# #         'Sorting hat',
# #         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
# #     st.write(f"You are in {chosen} house!")
# #     if user_access == 1:
# #         st.write(f"Welcome Device {collect_user_context}")
# #         st.write("Display Content from Zone A")