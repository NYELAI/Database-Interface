import streamlit as st
from astrapy import DataAPIClient

# Initialize Astra DB client as before
token = "AstraCS:oBgERxehBMFmiBEhfFfmGQuv:e0568f3d7817910dd917c0ee228aefe89be012419cb379b64ee2b9a90a44c6bb"
client = DataAPIClient(token)
url = "https://1c09e70f-c87a-49c0-8254-9bc14bb60e31-us-east-2.apps.astra.datastax.com"
db = client.get_database_by_api_endpoint(url)
Constants_Collection = db.get_collection("constants")

st.title("Constants Page - CRUD Operations")

# View All or Specific Constant
st.header("View Constants")
view_option = st.selectbox("Choose to view all constants or a specific one:", ["","All", "Specific"])

if view_option == "All":
    # Display all constants
    constants = Constants_Collection.find()  # Use Astra DB find method
    for constant in constants:
        st.write(f"Variable: {constant['variable_name']}, Value: {constant['value']}")

elif view_option == "Specific":
    variable_name = st.text_input("Enter the variable name to view:")
    if variable_name:
        constant = Constants_Collection.find_one({"variable_name": variable_name})
        if constant:
            st.write(f"Variable: {constant['variable_name']}, Value: {constant['value']}")
        else:
            st.write("No constant found for the given variable name.")

# Update Constant
st.header("Update Constant")
variable_name_update = st.text_input("Enter the variable name to update:")
new_value = st.text_input("New Value:")

if st.button("Update Constant"):
    if variable_name_update and new_value:
        constant = Constants_Collection.find_one({"variable_name": variable_name_update})
        if constant:
            Constants_Collection.update_one(
                {"variable_name": variable_name_update},
                {"$set": {"value": new_value}}
            )
            st.write(f"Constant '{variable_name_update}' updated successfully.")
        else:
            st.write(f"No constant found with variable name: {variable_name_update}.")
    else:
        st.write("Please provide both variable name and new value.")

# Delete Constant
st.header("Delete Constant")
variable_name_delete = st.text_input("Enter the variable name to delete:")

if st.button("Delete Constant"):
    constant = Constants_Collection.find_one({"variable_name": variable_name_delete})
    if constant:
        Constants_Collection.delete_one({"variable_name": variable_name_delete})
        st.write(f"Constant '{variable_name_delete}' deleted successfully.")
    else:
        st.write(f"No constant found with variable name: {variable_name_delete}.")

# Add New Constant
st.header("Add New Constant")
new_variable_name = st.text_input("New Variable Name:")
new_value_add = st.text_input("Enter Value:")

if st.button("Add Constant"):
    if new_variable_name and new_value_add:
        Constants_Collection.insert_one({
            "variable_name": new_variable_name,
            "value": new_value_add
        })
        st.write(f"New constant '{new_variable_name}' added successfully.")
    else:
        st.write("All fields are required to add a new constant.")
