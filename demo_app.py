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

def predict_crop():
    st.title("Predict Crop")

    # Input form for user
    temp = st.slider("Temperature", min_value=0.0, max_value=60.0, step=0.1, value=25.0)
    rainfall = st.slider("Rainfall", min_value=0.0, max_value=1200.0, step=0.1, value=50.0)
    humidity = st.slider("Humidity", min_value=0.0, max_value=100.0, step=0.1, value=60.0)

    # Make prediction
    if st.button("Predict Crop"):
        input_data_point = np.array([[temp, rainfall, humidity]])
        prediction = model.predict(input_data_point)
        crop = get_crop(prediction)
        st.success(f"The recommended crop is: {crop}")

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

    # Add button to predict crops for this forecast
    predict_crops_for_input_data(forecast_data)
    
    uploaded_file = st.file_uploader(f"Upload CSV file to get forecasts", type="csv")

def predict_crops_for_input_data(input_data):
    st.title("Estimate crop based on forecasts")

    # Add button to predict crops for each row
    if st.button("Predict Crops"):
        for index, row in input_data.iterrows():
            temperature = (row['MMIN'] + row['MMAX']) / 2
            rainfall = row['TMRF']
            humidity = row['Humidity']

            input_data_point = np.array([[temperature, rainfall, humidity]])
            prediction_probabilities = model.predict_proba(input_data_point)[0]
            top_crops = get_top_crops(prediction_probabilities, k=5)

            st.success(f"Top 5 estimated crops for row {index + 1}:")
            for i, (crop, probability) in enumerate(top_crops, 1):
                st.write(f"{i}.{crop}")

def get_top_crops(probabilities, k=5):
    # Get indices of the top k probabilities
    top_indices = np.argsort(probabilities)[::-1][:k]

    # Map indices to crop names and probabilities
    top_crops = [(get_crop_label(index), probabilities[index]) for index in top_indices]

    return top_crops

def get_crop_label(prediction):
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
    
    return crop_mapping.get(int(prediction), "Unknown Crop")

def main():
    st.title("Crop Recommendation App")
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://media.gettyimages.com/id/1724875987/photo/corn-field-sunset.jpg?s=612x612&w=0&k=20&c=DjVgnMIeoV8eX71HhDBHG7kp9iPQ8y_TId5Ee_enidE=");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    # Create buttons for navigation on the home page
    predict_crop_button = st.button("Predict Crop", key="predict_crop_button")
    forecast_button = st.button("See Forecasts", key="forecast_button")
    crop_calendar_button = st.button("See Crop Calendar for Maharashtra State", key="crop_calendar_button")

    # Check button clicks and navigate to respective pages
    if predict_crop_button:
        st.session_state.page = "Predict Crop"
    elif forecast_button:
        st.session_state.page = "Forecast"
    elif crop_calendar_button:
        st.session_state.page = "Crop Calendar"

    # Display content based on the selected page
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    if st.session_state.page == "Predict Crop":
        predict_crop()

    elif st.session_state.page == "Forecast":
        forecast_page()

    elif st.session_state.page == "Crop Calendar":
        show_crop_calendar()

if __name__ == "__main__":
    main()
