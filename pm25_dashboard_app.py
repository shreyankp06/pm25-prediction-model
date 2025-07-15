import streamlit as st
import pandas as pd
import pickle

with open("NEWDELHIpm25_predictor_rfl.pkl", "rb") as f:
    model = pickle.load(f)

FEATURE_ORDER = [
    'aod', 'Temp_Max', 'Temp_Min', 'Humidity', 'Precipitation', 'Wind_Speed',
    'SLP', 'U10M', 'V10M', 'TQV', 'TS'
]

SAMPLE_INPUT = {
    'aod': 0.367,
    'Temp_Max': 16.5,
    'Temp_Min': 5.0,
    'Humidity': 89,
    'Precipitation': 0.0,
    'Wind_Speed': 11.5,     
    'SLP': 1022.29,
    'U10M': 1.37,
    'V10M': -1.91,
    'TQV': 5.77,
    'TS': 281.29            
}

st.title(" PM2.5 Prediction Dashboard (New Delhi)")
st.write("Predict PM2.5 using manual input or by uploading a CSV file.")

mode = st.radio("Choose input method:", ["Manual Input", "Upload CSV"])

def classify_pm25(value):
    if value <= 50:
        return "Good"
    elif value <= 100:
        return "Satisfactory"
    elif value <= 200:
        return "Moderate"
    elif value <= 300:
        return "Poor"
    elif value <= 400:
        return "Very Poor"
    else:
        return "Severe"

if mode == "Manual Input":
    st.subheader("Enter Environmental Data")

    use_sample = st.button("Use Sample Input")

    values = SAMPLE_INPUT.copy() if use_sample else {}

    aod = st.number_input("AOD", 0.0, 5.0, value=values.get("aod", 0.5), step=0.01)
    temp_max = st.number_input("Max Temperature (°C)", 0.0, 50.0, value=values.get("Temp_Max", 25.0), step=0.1)
    temp_min = st.number_input("Min Temperature (°C)", 0.0, 40.0, value=values.get("Temp_Min", 15.0), step=0.1)
    humidity = st.slider("Humidity (%)", 0, 100, value=values.get("Humidity", 60))
    precipitation = st.number_input("Precipitation (mm)", 0.0, 100.0, value=values.get("Precipitation", 0.0), step=0.1)
    wind_speed = st.number_input("Wind Speed (m/s)", 0.0, 50.0, value=values.get("Wind_Speed", 5.0), step=0.1)
    slp = st.number_input("Sea Level Pressure (SLP hPa)", 900.0, 1100.0, value=values.get("SLP", 1013.0), step=0.1)
    u10m = st.number_input("U-component Wind @10m (m/s)", -50.0, 50.0, value=values.get("U10M", 1.0), step=0.1)
    v10m = st.number_input("V-component Wind @10m (m/s)", -50.0, 50.0, value=values.get("V10M", -1.0), step=0.1)
    tqv = st.number_input("Total Column Water Vapor (TQV kg/m²)", 0.0, 100.0, value=values.get("TQV", 10.0), step=0.1)
    ts = st.number_input("Surface Temperature (TS K)", 270.0, 320.0, value=values.get("TS", 285.0), step=0.1)

    if st.button("Predict PM2.5"):
        input_data = pd.DataFrame([{
            'aod': aod,
            'Temp_Max': temp_max,
            'Temp_Min': temp_min,
            'Humidity': humidity,
            'Precipitation': precipitation,
            'Wind_Speed': wind_speed,
            'SLP': slp,
            'U10M': u10m,
            'V10M': v10m,
            'TQV': tqv,
            'TS': ts
        }])

        input_data = input_data[FEATURE_ORDER]

        st.write("Inputs to the model:")
        st.dataframe(input_data)

        pm25_pred = max(0, model.predict(input_data)[0])
        st.subheader(f"Predicted PM2.5: {pm25_pred:.2f} µg/m³")
        st.subheader(f"AQI Category: {classify_pm25(pm25_pred)}")


elif mode == "Upload CSV":
    st.subheader("Upload CSV File")
    uploaded_file = st.file_uploader("Upload a CSV with these columns:", type="csv")
    st.code(", ".join(FEATURE_ORDER))

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data Preview:")
        st.dataframe(df.head())

        if not all(col in df.columns for col in FEATURE_ORDER):
            st.error(" CSV is missing one or more required columns.")
        else:
            df = df[FEATURE_ORDER]
            predictions = model.predict(df)
            df["Predicted_PM2.5"] = [max(0, p) for p in predictions]
            df["AQI_Category"] = df["Predicted_PM2.5"].apply(classify_pm25)

            st.success("Prediction complete!")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode()
            st.download_button("Download Results CSV", data=csv,
                               file_name="pm25_predictions.csv", mime="text/csv")

    if st.button("Download Template CSV"):
        template_df = pd.DataFrame(columns=FEATURE_ORDER)
        st.download_button("Download Template",
                           data=template_df.to_csv(index=False).encode(),
                           file_name="pm25_input_template.csv", mime="text/csv"
         )

