import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the saved Random Forest model
model = pickle.load(open("new_random_forest_model.pkl", 'rb'))

# Helper function to map predicted label to crop
def get_crop(prediction):
    crop_mapping = {
        0: 'apple', 1: 'banana', 2: 'blackgram', 3: 'chickpea', 
        4: 'coconut', 5: 'coffee', 6: 'cotton', 
        7: 'grapes', 8: 'jute', 9: 'kidneybeans', 
        10: 'lentil', 11: 'maize', 12: 'mango', 
        13: 'mothbeans', 14: 'mungbean', 15: 'muskmelon', 
        16: 'orange', 17: 'papaya', 18: 'pigeonpeas', 
        19: 'pomegranate', 
        20: 'rice', 21: 'watermelon'
    }
    return crop_mapping.get(prediction[0], "Unknown Crop")

def show_crop_calendar():
    # Load your Excel sheet with crop calendar
    # Replace 'your_crop_calendar.xlsx' with the actual filename or path
    crop_calendar = pd.read_excel('CROPCALENDAR.xlsx')

    # Display the crop calendar as a Markdown table
    st.title("Crop Calendar")

    # Convert DataFrame to Markdown table
    markdown_table = crop_calendar.to_markdown(index=False)

    # Display Markdown table
    st.markdown(markdown_table, unsafe_allow_html=True)


def main():
    st.title("Crop Recommendation App")

    # Input form for user
    temp = st.slider("Temperature", min_value=0.0, max_value=60.0, step=0.1, value=25.0)
    rainfall = st.slider("Rainfall", min_value=0.0, max_value=1200.0, step=0.1, value=50.0)
    humidity = st.slider("Humidity", min_value=0.0, max_value=100.0, step=0.1, value=60.0)
    
    # Make prediction
    if st.button("Predict Crop"):
        input_data = np.array([[temp, rainfall, humidity]])
        prediction = model.predict(input_data)
        crop = get_crop(prediction)
        st.success(f"The recommended crop is: {crop}")

    # Add button to show crop calendar 
    if st.button("Calendar"):
        show_crop_calendar()

if __name__ == "__main__":
    main()
