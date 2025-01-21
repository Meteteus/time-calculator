import streamlit as st

def convert_seconds_to_hhmmss(total_seconds):
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

st.title("Time Calculator")
st.write("Convert seconds into hh:mm:ss format.")

# User input
total_seconds = st.number_input("Enter the total seconds", min_value=0, step=1)

# Display the result
if total_seconds is not None:
    time_str = convert_seconds_to_hhmmss(total_seconds)
    st.write(f"Time in hh:mm:ss format: {time_str}")
