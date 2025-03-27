import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load dataset
df = pd.read_csv("movie_dataset.csv")  # Update with your dataset path

# Data Cleaning & Feature Engineering
df["genres"].fillna("Unknown", inplace=True)
df["runtime"].fillna(df["runtime"].median(), inplace=True)
df["director"].fillna("Unknown", inplace=True)
df["main_genre"] = df["genres"].apply(lambda x: x.split()[0] if x != "Unknown" else "Unknown")

# Select features and target
df_final = df[["budget", "popularity", "vote_average", "vote_count", "runtime", "main_genre", "revenue"]]

# Splitting data
X = df_final.drop(columns=["revenue"])
y = df_final["revenue"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define preprocessing
num_features = ["budget", "popularity", "vote_average", "vote_count", "runtime"]
cat_features = ["main_genre"]

num_transformer = StandardScaler()
cat_transformer = OneHotEncoder(handle_unknown="ignore")

preprocessor = ColumnTransformer(
    transformers=[
        ("num", num_transformer, num_features),
        ("cat", cat_transformer, cat_features),
    ]
)

# Model pipeline
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train the model
model.fit(X_train, y_train)

# Save the trained model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

# Evaluate model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model saved as 'model.pkl'.")
print(f"Mean Absolute Error: ${mae:,.2f}")
print(f"R² Score: {r2:.2f}")
