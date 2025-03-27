####************  this is total garbage but its was hard to write so i am not dlting it *******//// 



# import streamlit as st

# import pandas as pd
# import joblib
# import numpy as np
# import matplotlib.pyplot as plt
# from pathlib import Path

# # --- Path Configuration ---
# MODEL_PATH = "model.pkl"  # Place your model file in the same directory as this script

# # --- Page Setup ---
# st.set_page_config(
#     page_title="Movie Popularity Predictor",
#     page_icon="🎬",
#     layout="centered"
# )

# # --- Model Loading ---
# @st.cache_resource
# def load_model():
#     try:
#         model = joblib.load(MODEL_PATH)
#         st.success("✅ Model loaded successfully!")
#         return model
#     except Exception as e:
#         st.error(f"❌ Failed to load model: {str(e)}")
#         st.stop()  # Stop execution if model fails to load

# model = load_model()

# # --- Header Section ---
# st.title("🎬 Movie Popularity Predictor")
# st.markdown("""
# Predict your movie's chance of becoming a hit based on **budget** and **genre**.
# Upload your `model.pkl` file to get accurate predictions.
# """)

# # --- Input Section ---
# with st.form("prediction_form"):
#     col1, col2 = st.columns(2)
#     with col1:
#         budget = st.slider(
#             "Production Budget (in millions USD)",
#             min_value=1,
#             max_value=500,
#             value=50,
#             step=1
#         )
#     with col2:
#         genre = st.selectbox(
#             "Primary Genre",
#             ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Thriller"]
#         )
    
#     submitted = st.form_submit_button("Predict Popularity")

# # --- Prediction Logic ---
# if submitted:
#     # Create input DataFrame matching model's expected format
#     input_data = pd.DataFrame({
#         "budget": [budget],
#         "main_genre": [genre]  # Note: Spelling matches your error message
#     })
    
#     try:
#         # Make prediction
#         popularity_score = model.predict(input_data)[0]
        
#         # Ensure score is within 0-100 range
#         popularity_score = np.clip(float(popularity_score), 0, 100)
        
#         # --- Visualization ---
#         st.subheader("Prediction Results")
        
#         # Gauge Meter
#         fig, ax = plt.subplots(figsize=(10, 3))
#         ax.barh(['Popularity'], [100], color='#f0f2f6')  # Background
#         ax.barh(['Popularity'], [popularity_score], color='#ff4b4b')  # Progress
#         ax.text(popularity_score/2, 0, 
#                 f"{popularity_score:.1f}%", 
#                 va='center', ha='center', 
#                 color='white', fontsize=24, fontweight='bold')
#         ax.set_xlim(0, 100)
#         ax.axis('off')
#         st.pyplot(fig)
        
#         # --- Interpretation ---
#         st.markdown("### Popularity Interpretation")
#         if popularity_score >= 70:
#             st.success("🔥 High Chance of Going Viral!")
#             st.markdown("""
#             - Excellent potential for box office success
#             - Likely to trend on social media
#             - Good candidate for film festivals
#             """)
#         elif popularity_score >= 40:
#             st.warning("🟡 Moderate Popularity Potential")
#             st.markdown("""
#             - May need stronger marketing
#             - Consider A-list casting
#             - Optimize release timing
#             """)
#         else:
#             st.error("🔴 Needs Improvement")
#             st.markdown("""
#             - Re-evaluate budget allocation
#             - Consider genre trends
#             - Test with focus groups
#             """)
            
#     except Exception as e:
#         st.error(f"Prediction failed: {str(e)}")
#         with st.expander("Debug Details"):
#             st.write("Input Data:", input_data)
#             try:
#                 st.write("Model expects:", model.feature_names_in_)
#             except:
#                 st.write("Could not retrieve model's expected features")

# # --- Model Information Section ---
# with st.expander("ℹ️ About This Prediction"):
#     st.markdown("""
#     **How to use:**
#     1. Place your `model.pkl` file in the same folder as this script
#     2. Ensure your model was trained to predict popularity (0-100 scale)
#     3. The model should expect these features:
#        - `budget` (numeric)
#        - `main_genre` (categorical)
    
#     **For best results:**
#     - Train your model on recent movie data
#     - Include similar features in your training data
#     - Use regression or classification appropriate for your target
#     """)

# # --- Footer ---
# st.markdown("---")
# st.caption("""
# Need help with your model? Ensure it expects:
# - Budget (numeric)
# - Genre (categorical)
# """)