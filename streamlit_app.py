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
st.write("Enter start time and end time, and calculate the elapsed time.")

# Input: Start Time (3 columns for hours, minutes, seconds)
st.subheader("Start Time")
col1, col2, col3 = st.columns(3)
with col1:
    start_hours = st.number_input("Hours", min_value=0, max_value=23, value=0, key="start_hours")
with col2:
    start_minutes = st.number_input("Minutes", min_value=0, max_value=59, value=0, key="start_minutes")
with col3:
    start_seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, key="start_seconds")

# Input: End Time (3 columns for hours, minutes, seconds)
st.subheader("End Time")
col1, col2, col3 = st.columns(3)
with col1:
    end_hours = st.number_input("Hours", min_value=0, max_value=23, value=0, key="end_hours")
with col2:
    end_minutes = st.number_input("Minutes", min_value=0, max_value=59, value=0, key="end_minutes")
with col3:
    end_seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, key="end_seconds")

# Button to calculate the time difference
if st.button("Calculate"):
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
        st.success(f"Time elapsed: {time_str}")
