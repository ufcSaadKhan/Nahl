import streamlit as st
import pandas as pd
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceAuthenticationFailed
from Utils.salesforce_login import sf

sf = None
if st.sidebar.button("Connect"):
    try:
        sf = Salesforce(username=username, password=password, security_token=security_token)
        st.sidebar.success("✅ Connected to Salesforce")
    except SalesforceAuthenticationFailed as e:
        st.sidebar.error("❌ Login failed. Check credentials.")

# --- Show Contacts ---
if sf:
    st.header("Salesforce Contacts")

    # Query Contact data
    query = "SELECT Id, FirstName, LastName, Email, Phone FROM Contact LIMIT 100"
    contacts = sf.query(query)
    records = contacts["records"]
    df = pd.DataFrame(records).drop(columns='attributes')

    st.dataframe(df)

    # Create new contact
    st.subheader("➕ Create New Contact")
    with st.form("create_contact"):
        first = st.text_input("First Name")
        last = st.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        submitted = st.form_submit_button("Create")

        if submitted:
            sf.Contact.create({
                "FirstName": first,
                "LastName": last,
                "Email": email,
                "Phone": phone
            })
            st.success("✅ Contact created! Please reload the app to see it.")