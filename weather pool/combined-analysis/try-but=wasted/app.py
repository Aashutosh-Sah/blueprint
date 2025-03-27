import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3


API_URL = "http://127.0.0.1:5000"  # Flask backend URL

st.title("Customer Segmentation Dashboard")

# Upload CSV
data_file = st.file_uploader("Customer_Data.csv", type=["csv"])
if data_file:
    df = pd.read_csv(data_file)
    st.write("Customer_Data.csv:")
    st.write(df.head())

    # Train Model
    if st.button("Train Model & Segment Customers"):
        response = requests.get(f"{API_URL}/train")
        if response.status_code == 200:
            st.success("Model trained and customers segmented successfully!")
        else:
            st.error("Error training model")

    # Visualize Segments
    if st.button("Show Segmentation Results"):
        conn = sqlite3.connect("customers.db")
        df_clustered = pd.read_sql("SELECT * FROM customer_segments", conn)
        conn.close()
        
        st.write("### Segmented Customer Data:")
        st.write(df_clustered.head())

        # Plot Clusters
        plt.figure(figsize=(8,5))
        sns.scatterplot(x=df_clustered["Annual_Income"], y=df_clustered["Spending_Score"], hue=df_clustered["Cluster"], palette='viridis')
        plt.xlabel("Annual Income")
        plt.ylabel("Spending Score")
        plt.title("Customer Segmentation Visualization")
        st.pyplot(plt)

    # Predict Cluster
    st.write("### Predict Customer Segment:")
    age = st.number_input("Age", min_value=18, max_value=100)
    income = st.number_input("Annual Income", min_value=10000, max_value=200000)
    spending = st.number_input("Spending Score", min_value=1, max_value=100)

    if st.button("Predict Cluster"):
        payload = {"Age": age, "Annual_Income": income, "Spending_Score": spending}
        response = requests.post(f"{API_URL}/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Customer Cluster: {result['Predicted Cluster']}")
        else:
            st.error("Prediction failed")
