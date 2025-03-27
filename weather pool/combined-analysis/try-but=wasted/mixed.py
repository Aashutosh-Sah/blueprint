import sqlite3
import streamlit as st

# Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# Create the 'customers' table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
""")
conn.commit()

# Streamlit UI
st.title("Customer Database")
st.write("Enter customer details:")

name = st.text_input("Name")
email = st.text_input("Email")

if st.button("Add Customer"):
    if name and email:
        try:
            cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            st.success("Customer added successfully!")
        except sqlite3.IntegrityError:
            st.error("Email already exists!")
    else:
        st.error("Please fill out both fields.")

# Display all customers in the database
if st.button("Show All Customers"):
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    
    if customers:
        st.write("### Customer List")
        for customer in customers:
            st.write(f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}")
    else:
        st.write("No customers found.")

# Close connection when done (important for resource management)
conn.close()
