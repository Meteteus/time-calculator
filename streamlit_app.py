import streamlit as st
import json

# Function to calculate time difference in seconds
def calculate_time_difference(start_time, end_time):
    start_seconds = start_time[0]*3600 + start_time[1]*60 + start_time[2]
    end_seconds = end_time[0]*3600 + end_time[1]*60 + end_time[2]
    elapsed_seconds = end_seconds - start_seconds
    return elapsed_seconds

# Function to convert seconds to hh:mm:ss format
def convert_seconds_to_hhmmss(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Streamlit app layout
st.title("Time Elapsed Calculator")
st.write("Enter start time and end time, name your calculation, and view your history.")

# Initialize the history list in session state if not already there
if "history" not in st.session_state:
    st.session_state["history"] = []

# Input: Start Time (3 columns for hours, minutes, seconds)
st.subheader("Start Time")
col1, col2, col3 = st.columns(3)
start_hours = col1.number_input("Hours", min_value=0, max_value=23, key="start_hours", value=0)
start_minutes = col2.number_input("Minutes", min_value=0, max_value=59, key="start_minutes", value=0)
start_seconds = col3.number_input("Seconds", min_value=0, max_value=59, key="start_seconds", value=0)

# Input: End Time (3 columns for hours, minutes, seconds)
st.subheader("End Time")
col1, col2, col3 = st.columns(3)
end_hours = col1.number_input("Hours", min_value=0, max_value=23, key="end_hours", value=0)
end_minutes = col2.number_input("Minutes", min_value=0, max_value=59, key="end_minutes", value=0)
end_seconds = col3.number_input("Seconds", min_value=0, max_value=59, key="end_seconds", value=0)

# Input: Name for the calculation
calculation_name = st.text_input("Name this calculation", "")

# Add custom CSS to style the buttons and modal
st.markdown("""
    <style>
        .stButton button {
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton>button:first-child {
            background-color: #1E90FF; /* Blue color */
            color: white;
        }
        .stButton>button:first-child:hover {
            background-color: #4682B4; /* Darker blue */
        }
        .stButton>button:last-child {
            background-color: red; /* Red color */
            color: white;
        }
        .stButton>button:last-child:hover {
            background-color: darkred; /* Darker red */
        }
        /* Modal styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5); /* Black background with transparency */
            overflow: auto;
        }
        .modal-content {
            background-color: white;
            margin: 15% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
            max-width: 500px;
            border-radius: 8px;
        }
        .modal-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }
        .modal-button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
        }
        .confirm-btn {
            background-color: green;
            color: white;
        }
        .cancel-btn {
            background-color: gray;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Button to calculate the time difference
if st.button("Calculate", key="calculate", help="Click to calculate time elapsed"):
    # Check if the input is valid
    if (start_hours, start_minutes, start_seconds) == (0, 0, 0) and (end_hours, end_minutes, end_seconds) == (0, 0, 0):
        st.warning("Both start and end times are set to 0. Please input valid times.")
    else:
        # If the fields are empty, treat them as 0 when calculating
        start_hours = start_hours if start_hours is not None else 0
        start_minutes = start_minutes if start_minutes is not None else 0
        start_seconds = start_seconds if start_seconds is not None else 0
        end_hours = end_hours if end_hours is not None else 0
        end_minutes = end_minutes if end_minutes is not None else 0
        end_seconds = end_seconds if end_seconds is not None else 0

        start_time = (start_hours, start_minutes, start_seconds)
        end_time = (end_hours, end_minutes, end_seconds)

        # Check if end time is earlier than start time
        start_seconds_total = start_time[0]*3600 + start_time[1]*60 + start_time[2]
        end_seconds_total = end_time[0]*3600 + end_time[1]*60 + end_time[2]

        if end_seconds_total < start_seconds_total:
            st.error("End time cannot be earlier than start time. Please enter valid times.")
        else:
            # Calculate time difference
            elapsed_seconds = calculate_time_difference(start_time, end_time)

            # Convert elapsed time to hh:mm:ss
            time_str = convert_seconds_to_hhmmss(elapsed_seconds)

            # Add the current calculation to the history
            if calculation_name:
                st.session_state["history"].append({"name": calculation_name, "result": time_str})
            else:
                st.session_state["history"].append({"name": "Unnamed", "result": time_str})

            st.success(f"Time elapsed: {time_str}")

# Display the history download button
if st.session_state["history"]:
    st.subheader("Download History")
    # Convert history to JSON for easy download
    history_json = json.dumps(st.session_state["history"], indent=4)
    st.download_button("Download History", data=history_json, file_name="calculation_history.json", mime="application/json")

# Show a "Reset History" button and implement the confirmation pop-up
if st.button("Reset History", key="reset", help="Click to reset your history"):
    # Show the reset confirmation pop-up (using custom HTML/CSS)
    st.markdown("""
        <div class="modal" id="resetModal">
            <div class="modal-content">
                <p>Are you sure you want to reset the history?</p>
                <div class="modal-buttons">
                    <button class="modal-button confirm-btn" onclick="window.location.reload();">Confirm</button>
                    <button class="modal-button cancel-btn" onclick="document.getElementById('resetModal').style.display='none';">Cancel</button>
                </div>
            </div>
        </div>
        <script>
            document.getElementById('resetModal').style.display = 'block';
        </script>
    """, unsafe_allow_html=True)
