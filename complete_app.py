import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load the saved Random Forest model
model = pickle.load(open("new_random_forest_model.pkl", 'rb'))

# Load the saved LSTM model
with open("lstm_forecast_model.pkl", "rb") as file:
    lstm_model = pickle.load(file)

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

def forecast_page():
    st.title("Division-wise Forecast")

    # Define divisions and their corresponding CSV files
    division_files = {
        "Pune": "pune_forecast.csv",
        "Nagpur": "nagpur_forecast.csv",
        "Nashik": "nashik_forecast.csv",
        "Aurangabad": "aurangabad_forecast.csv",
        "Amravati": "amravati_forecast.csv",
        "Konkan": "konkan_forecast.csv",
    }

    # User selects a division
    selected_division = st.selectbox("Select Division", list(division_files.keys()))

    # Load the corresponding CSV file for the selected division
    file_path = division_files[selected_division]
    forecast_data = pd.read_csv(file_path)

    # Display the forecast results in a table
    st.write(f"Forecast Results for {selected_division}:")
    st.dataframe(forecast_data)

def main():
    st.title("Crop Recommendation App")

    # Create buttons for navigation
    predict_crop_button = st.button("Predict Crop", key="predict_crop_button")
    forecast_button = st.button("Forecast", key="forecast_button")

    # Check button clicks and navigate to respective pages
    if predict_crop_button:
        st.session_state.page = "Predict Crop"
    elif forecast_button:
        st.session_state.page = "Forecast"

    # Display content based on the selected page
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    if st.session_state.page == "Predict Crop":
        st.write("Welcome to the Predict Crop page!")
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
        if st.button("See Crop Calendar for Maharashtra State"):
            show_crop_calendar()

    elif st.session_state.page == "Forecast":
        forecast_page()
    else:
        st.write("Welcome to the Home page!")
        # Add your content for the Home page here

if __name__ == "__main__":
    main()
