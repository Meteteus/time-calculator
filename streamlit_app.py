import streamlit as st

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

# Button to calculate the time difference
if st.button("Calculate", key="calculate", help="Click to calculate time elapsed"):
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

# Display the history
if st.session_state["history"]:
    st.subheader("Calculation History")
    for idx, entry in enumerate(st.session_state["history"], start=1):
        st.write(f"{idx}. {entry['name']}: {entry['result']}")

# Button to reset history with confirmation
reset_history = st.button("Reset History", key="reset", help="Click to reset your history")

if reset_history:
    # Confirmation prompt for resetting history
    reset_confirm = st.button("Are you sure you want to reset the history? Click to confirm.")
    if reset_confirm:
        st.session_state["history"] = []  # Clear the history
        st.success("History has been reset.")
    else:
        st.warning("History reset canceled.")
