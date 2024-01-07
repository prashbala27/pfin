import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
import altair as alt

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
# Function to execute a query and retrieve results
def execute_query(query):
    connection, cursor = create_connection()
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results

# Function to insert data into the PostgreSQL database
def insert_data(connection, cursor, data):
    query = sql.SQL("INSERT INTO persfinance.Daily_Expenses (date, category, subcategory, credit_debit, amount, description, bank_details) VALUES (%s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (data["Date"], data["Category"], data["Subcategory"], data["Credit/Debit"], data["Amount"], data["Description"], data["Bank Details"]))
    connection.commit()

# Function to retrieve data from the PostgreSQL database
def retrieve_data():
    connection, cursor = create_connection()
    cursor.execute("SELECT * FROM persfinance.Daily_Expenses")
    data = cursor.fetchall()
    connection.close()
    return data

def input_page():
    st.header("Input Page")

    # Define categories, subcategories, credit/debit options, and bank details options
    categories = ["Food", "Medical", "Utilities", "Transportation", "Entertainment", "Miscellaneous", "loaned", "Investment"]
    subcategories = ["NA", "Utils-Dress", "Investment-Gold", "Investment-MutualFund", "Investment-TermInsurancePayment",
                     "Food-Family", "Food-Friends", "Misc-OnlinePurchase", "Utils-2Wheeeler",
                     "Utils-4Wheeler", "Trasnport-TrainTicket", "Trasnport-Flight", "Misc-Trip",
                     "Utils-EB", "Utils-Mobile", "Utils-Broadband", "Enter-Netflix", "Enter-Xbox", "Loaned", "Loaned-Repaid"]
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

def chart_page():
    st.header("Charts Page")

    # Retrieve data from the database
    data = retrieve_data()

    # Convert data to a DataFrame
    columns = ["id", "date", "category", "subcategory", "credit_debit", "amount", "description", "bank_details"]
    df = pd.DataFrame(data, columns=columns)


    # Create a bar chart based on amount and categories
    bar_chart_category_subcategory = alt.Chart(df).mark_bar().encode(
        x=alt.X('category:N', title='Category'),
        y=alt.Y('sum(amount):Q', title='Total Amount'),
        color='subcategory:N',
        tooltip=['category:N', 'subcategory:N', 'sum(amount):Q']
    ).properties(
        title='Total Expense Distribution by Category and Subcategory',
        width=600,
        height=400
    ).interactive()

    st.subheader("Bar Chart - Total Expense Distribution by Category and Subcategory")
    st.altair_chart(bar_chart_category_subcategory, use_container_width=True)

def query_page():
    st.header("Query Page")

    # Default query
    default_query = "SELECT * FROM persfinance.Daily_Expenses LIMIT 10;"

    # Text area for the user to input the query
    query_input = st.text_area("Enter your SQL query here:", default_query)

    # Button to execute the query
    if st.button("Execute Query"):
        try:
            # Execute the query and retrieve results
            results = execute_query(query_input)

            # Display the results in a DataFrame
            if results:
                st.write("Query Results:")
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.warning("No results found.")
        except Exception as e:
            st.error(f"Error executing the query: {e}")
def main():
    st.title("Expense Tracker")

    # Navigation
    pages = ["Input", "Charts", "Query"]
    page = st.sidebar.radio("Select Page", pages)

    if page == "Input":
        input_page()
    elif page == "Charts":
        chart_page()
    elif page == "Query":
        query_page()

if __name__ == "__main__":
    main()