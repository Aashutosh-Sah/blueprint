import streamlit as st
import pickle
import numpy as np

# Load the trained model
with open("/mnt/data/model.pkl", "rb") as file:
    model = pickle.load(file)

# Streamlit app layout
st.set_page_config(page_title="Movie Popularity Predictor", layout="centered")
st.title("🎬 Movie Popularity Predictor")
st.markdown("Predict the chance of a movie being popular based on its budget and genre.")
st.write(f"Model type: {type(model)}")

# Input fields
budget = st.number_input("Enter the movie budget ($M)", min_value=0.1, step=0.1)
genre = st.selectbox("Select a Genre", ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller"])

# Genre encoding (modify if needed based on model training)
genre_dict = {"Action": 0, "Comedy": 1, "Drama": 2, "Horror": 3, "Romance": 4, "Sci-Fi": 5, "Thriller": 6}
genre_encoded = genre_dict.get(genre, 0)

# Prediction
if st.button("Predict Popularity"):
    input_data = np.array([[budget, genre_encoded]])
    prediction = model.predict(input_data)[0] 
    
    st.success(f"Predicted Popularity Score: {prediction:.2f}")

