from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import sqlite3

app = Flask(__name__)

# Load dataset and preprocess
def load_data():
    df = pd.read_csv("customer_data.csv")
    df.dropna(inplace=True)
    df = pd.get_dummies(df, drop_first=True)  # Encode categorical features
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    return df, df_scaled

# Train K-Means model
def train_kmeans(n_clusters=4):
    df, df_scaled = load_data()
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(df_scaled)
    return df, kmeans

# Initialize Database
def init_db():
    conn = sqlite3.connect("customers.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            income INTEGER,
            spending_score INTEGER,
            cluster INTEGER
        )
    """)
    conn.commit()
    conn.close()

@app.route("/train", methods=["GET"])
def train():
    df, model = train_kmeans()
    conn = sqlite3.connect("customers.db")
    df[['Age', 'Annual_Income', 'Spending_Score', 'Cluster']].to_sql("customer_segments", conn, if_exists="replace", index=False)
    conn.close()
    return jsonify({"message": "Model trained and data stored successfully!"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    df, model = train_kmeans()
    input_data = np.array([data.values()])
    cluster = model.predict(input_data)[0]
    return jsonify({"Predicted Cluster": int(cluster)})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
