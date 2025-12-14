import streamlit as st
import os
from journeys import insert_journey, fetch_all_journeys
from db import get_connection
from operators import fetch_operators, get_or_create_operator
from stations import fetch_stations, get_or_create_station

st.set_page_config(page_title="Train Journeys", layout="wide")

st.title("🚆 Train Journey Tracker")

menu = st.sidebar.radio("Menu", ["Add Journey", "View Journeys"])

operators = fetch_operators()
stations = fetch_stations()

# Prepare display lists with sentinel options
# operatorNames = [op["name"] for op in operators]
# operatorNames.append("Add new operator")

# stationNames = [s["name"] for s in stations]
# stationNames.append("Add new station")

# Add Journey Page
if menu == "Add Journey":
    st.header("Add a New Train Journey")
    with st.form("add_train_journey_form"):
        # Mandatory Fields
        operator = st.text_input("Operator Name *", help="Enter the name of the train operator.")
        originStation = st.text_input("Starting Station *", help="Enter the name of the starting station.")
        destinationStation = st.text_input("Destination Station *", help="Enter the name of the destination station.")

        journeyDate = st.date_input("Journey Date *", help="Select the date of the journey.")

        # Optional Fields
        st.subheader("Optional Information")
        trainNumber = st.text_input("Train Number", max_chars=100, help="Enter the train number.")
        locomotiveType = st.text_input("Locomotive Type", max_chars=100, help="Enter the type of locomotive used.")
        locomotiveNumber = st.text_input("Locomotive Number", max_chars=100, help="Enter the locomotive number.")
        carType = st.text_input("Car Type", max_chars=100, help="Enter the type of car used.")
        carNumber = st.text_input("Car Number", max_chars=100, help="Enter the car number.")

        intermediateStops = st.text_area("Enter intermediate stops in travel order", help="Enter station names separated by commas. Example: Station A, Station B, Station C")
        
        gpxFile = st.file_uploader("Upload GPX File", type=["gpx"], help="Upload a GPX file of the journey.")
        notes = st.text_area("Additional Notes", help="Enter any additional notes about the journey.")

        submitted = st.form_submit_button("Submit Journey")
        
        if submitted:
            # Resolve operator
            if not operator.strip():
                st.error("Operator is required")
                st.stop()
            operatorID = get_or_create_operator(operator.strip())

            # Resolve start station
            if not originStation.strip():
                st.error("Starting station is required")
                st.stop()
            originStationID = get_or_create_station(originStation.strip())

            # Resolve end station
            if not destinationStation.strip():
                st.error("Destination station is required")
                st.stop()
            destinationStationID = get_or_create_station(destinationStation.strip())

            # Resolve intermediate stops
            stopIDs = []
            if intermediateStops:
                stop_names = [
                    name.strip()
                    for name in intermediateStops.split(",")
                    if name.strip()
                ]

                for stop_name in stop_names:
                    stop_id = get_or_create_station(stop_name)
                    stopIDs.append(stop_id)

            gpxPath = None
            if gpxFile:
                os.makedirs("gpx_files", exist_ok=True) # Ensure directory exists
                gpxPath = os.path.join("gpx_files", gpxFile.name)
                with open(gpxPath, "wb") as f:
                    f.write(gpxFile.read())

            insert_journey(
                {
                    "operator": operatorID,
                    "originStation": originStationID,
                    "destinationStation": destinationStationID,
                    "journeyDate": journeyDate,
                    "trainNumber": trainNumber,
                    "locomotiveType": locomotiveType,
                    "locomotiveNumber": locomotiveNumber,
                    "carType": carType,
                    "carNumber": carNumber,
                    "stops": stopIDs,
                    "gpxPath": gpxPath,
                    "notes": notes   
                }
            )

            st.success("Journey saved successfully!")
            
else:
    st.header("My Journeys")
    journeys = fetch_all_journeys()
    # st.dataframe(journeys)
    journeys = fetch_all_journeys()
    for j in journeys:
        with st.expander(
            f"{j['journeyDate']} — {j['originStation']} → {j['destinationStation']} ({j['operator']})"
        ):
            st.markdown(f"""
    **Train Number:** {j['trainNumber'] or "—"}  
    **Locomotive:** {j['locomotiveType'] or "—"} {j['locomotiveNumber'] or ""}  
    **Car:** {j['carType'] or "—"} {j['carNumber'] or ""}  

    **Intermediate Stops:**  
    {j['intermediateStops'] or "None"}

    **Notes:**  
    {j['notes'] or ""}
    """)