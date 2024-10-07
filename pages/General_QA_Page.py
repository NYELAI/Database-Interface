import streamlit as st
from astrapy import DataAPIClient
from dotenv import load_dotenv
import os

# Initialize the Astra DB client
token = "AstraCS:oBgERxehBMFmiBEhfFfmGQuv:e0568f3d7817910dd917c0ee228aefe89be012419cb379b64ee2b9a90a44c6bb"
client = DataAPIClient(token)
url = "https://1c09e70f-c87a-49c0-8254-9bc14bb60e31-us-east-2.apps.astra.datastax.com"
db = client.get_database_by_api_endpoint(url)

# Get the collection
General_QA_Collection = db.get_collection("general_qa")

# Streamlit App Layout
st.title("General QA Collection")

# Read - Fetch All or Specific Document
st.header("View Data")
view_option = st.selectbox("Choose to view all data or a specific GA:", ["","All", "Specific GA"])

if view_option == "All":
    # Display all documents
    documents = General_QA_Collection.find()  # Use Astra DB find method
    for doc in documents:
        st.write(doc)

elif view_option == "Specific GA":
    # Input to fetch specific document by GA
    ga_number = st.text_input("Enter the GA number to view (e.g., GA1):")
    if ga_number:
        # Corrected retrieval using find_one
        document = General_QA_Collection.find_one({"GA": ga_number})
        if document:
            st.write(document)
        else:
            st.write("No document found for the given GA number.")

# Update - Modify Specific Document
st.header("Update Data")
ga_number_update = st.text_input("Enter the GA number to update (e.g., GA1):")
new_question = st.text_input("New Question (Leave empty if no change):")
new_answer = st.text_input("New Answer (Leave empty if no change):")
new_url = st.text_input("New URL (Leave empty if no change):")

if st.button("Update Document"):
    update_fields = {}

    if new_question:
        update_fields["Question"] = new_question
    if new_answer:
        update_fields["Answer"] = new_answer
    if new_url:
        update_fields["URL"] = new_url

    if update_fields:
        # Perform the update operation only if there are fields to update
        document = General_QA_Collection.find_one({"GA": ga_number_update})
        if document:
            # Corrected to use update_one method
            General_QA_Collection.update_one({"GA": ga_number_update}, {"$set": update_fields})
            st.write(f"Document with GA: {ga_number_update} updated successfully.")
        else:
            st.write(f"No document found for GA: {ga_number_update}.")
    else:
        st.write("No fields to update.")

# Delete - Remove Specific Document
st.header("Delete Data")
ga_number_delete = st.text_input("Enter the GA number to delete (e.g., GA1):")

if st.button("Delete Document"):
    document = General_QA_Collection.find_one({"GA": ga_number_delete})
    if document:
        General_QA_Collection.delete_one({"GA": ga_number_delete})
        st.write(f"Document with GA: {ga_number_delete} deleted successfully.")
    else:
        st.write(f"No document found for GA: {ga_number_delete}.")

# Optional: Create - Add a New Document (if needed)
st.header("Add New Data")
new_ga = st.text_input("New GA number (e.g., GA6):")
new_question_create = st.text_input("Enter new question:")
new_answer_create = st.text_input("Enter new answer:")
new_url_create = st.text_input("Enter new URL:")

if st.button("Add Document"):
    if new_ga and new_question_create and new_answer_create and new_url_create:
        General_QA_Collection.insert_one({
            "GA": new_ga,
            "Question": new_question_create,
            "Answer": new_answer_create,
            "URL": new_url_create
        })
        st.write(f"New document with GA: {new_ga} added successfully.")
    else:
        st.write("All fields are required to add a new document.")
