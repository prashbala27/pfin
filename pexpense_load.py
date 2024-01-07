import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql

# Function to create a PostgreSQL connection and cursor
def create_connection():
    connection = psycopg2.connect(
        user="xmnvcwda",
        password="kk_29N8o7-RKpdIO0QZthrTxmsukh60A",
        host="tiny.db.elephantsql.com",
        port="5432",
        database="xmnvcwda"
    )
    cursor = connection.cursor()
    return connection, cursor

# Function to insert data into the PostgreSQL database
def insert_data(connection, cursor, data):
    query = sql.SQL("INSERT INTO persfinance.Daily_Expenses (date, category, subcategory, credit_debit, amount, description, bank_details) VALUES (%s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (data["Date"], data["Category"], data["Subcategory"], data["Credit/Debit"], data["Amount"], data["Description"], data["Bank Details"]))
    connection.commit()

def main():
    st.title("Expense Tracker")

    # Define categories and credit/debit options
    categories = ["Food", "Utilities", "Transportation", "Entertainment", "Miscellaneous","Return Payment","Investment"]
    subcategories = ["Investment-Gold", "Investment-MutualFund", "Investment-TermInsurancePayment", 
                     "Food-Family", "Food-Friends","Misc-OnlinePurchase","Utils-2Wheeeler",
                     "Utils-4Wheeler","Trasnport-TrainTicket","Trasnport-Flight","Misc-Trip",
                     "Utils-EB","Utils-Mobile","Utils-Broadband","Enter-Netflix","Enter-Xbox",]
    credit_debit_options = ["Credit", "Debit"]
    bank_details_options = ["HDFC-9325", "HDFC-1148", "SBI-4398", "EQSM-1764"]

    # Create two columns for horizontal layout
    col1, col2, col3 = st.columns(3)

    # Get user input in the first column
    with col1:
        date = st.date_input("Date", pd.to_datetime("today"))
        category = st.selectbox("Category", categories)

    # Get user input in the second column
    with col2:
        subcategory = st.selectbox("Subcategory", subcategories)
        credit_debit = st.selectbox("Credit/Debit", credit_debit_options)
        amount = st.number_input("Amount", value=0.0, step=1.0)

    with col3:
        description = st.text_area("Description", "")
        bank_details = st.selectbox("Bank Details", bank_details_options)

    if st.button("Submit"):
        entered_data = {
            "Date": date,
            "Category": category,
            "Subcategory": subcategory,
            "Credit/Debit": credit_debit,
            "Amount": amount,
            "Description": description,
            "Bank Details": bank_details
        }

        # Display the entered information
        st.write("## Entered Information:")
        st.write(f"**Date:** {entered_data['Date']}")
        st.write(f"**Category:** {entered_data['Category']}")
        st.write(f"**Subcategory:** {entered_data['Subcategory']}")
        st.write(f"**Credit/Debit:** {entered_data['Credit/Debit']}")
        st.write(f"**Amount:** {entered_data['Amount']}")
        st.write(f"**Description:** {entered_data['Description']}")
        st.write(f"**Bank Details:** {entered_data['Bank Details']}")

        # Write data to PostgreSQL database
        connection, cursor = create_connection()
        insert_data(connection, cursor, entered_data)
        st.success("Data successfully written to the database.")

if __name__ == "__main__":
    main()