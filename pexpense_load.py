import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql

# Function to create a PostgreSQL connection and cursor
def create_connection():
    connection = psycopg2.connect(
        user="postgres",
        password="Thannu170218!",
        host="localhost",
        port="5432",
        database="postgres"
    )
    cursor = connection.cursor()
    return connection, cursor

# Function to insert data into the PostgreSQL database
def insert_data(connection, cursor, data):
    query = sql.SQL("INSERT INTO persfinance.Daily_Expenses (date, category, credit_debit, amount, description) VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(query, (data["Date"], data["Category"], data["Credit/Debit"], data["Amount"], data["Description"]))
    connection.commit()
def main():
    st.title("Expense Tracker")

    # Define categories and credit/debit options
    categories = ["Food", "Utilities", "Transportation", "Entertainment", "Miscellaneous"]
    credit_debit_options = ["Credit", "Debit"]

    # Create two columns for horizontal layout
    col1, col2 = st.columns(2)

    # Get user input in the first column
    with col1:
        date = st.date_input("Date", pd.to_datetime("today"))
        category = st.selectbox("Category", categories)

    # Get user input in the second column
    with col2:
        credit_debit = st.selectbox("Credit/Debit", credit_debit_options)
        amount = st.number_input("Amount", value=0.0, step=1.0)
        description = st.text_area("Description", "")

    # Add a "Submit" button
    if st.button("Submit"):
        entered_data = {
            "Date": date,
            "Category": category,
            "Credit/Debit": credit_debit,
            "Amount": amount,
            "Description": description
        }

        # Display the entered information
        st.write("## Entered Information:")
        st.write(f"**Date:** {entered_data['Date']}")
        st.write(f"**Category:** {entered_data['Category']}")
        st.write(f"**Credit/Debit:** {entered_data['Credit/Debit']}")
        st.write(f"**Amount:** {entered_data['Amount']}")
        st.write(f"**Description:** {entered_data['Description']}")

        # Write data to PostgreSQL database
        connection, cursor = create_connection()
        insert_data(connection, cursor, entered_data)
        st.success("Data successfully written to the database.")

if __name__ == "__main__":
    main()
