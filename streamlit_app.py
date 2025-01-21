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

# Function to convert hh:mm:ss to total seconds
def convert_hhmmss_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(":"))
    return hours * 3600 + minutes * 60 + seconds

# Streamlit app layout
st.title("Elapsed Time Calculator")  # Title changed
st.write("Enter start time and end time, name your calculation, and view your history.")

# Initialize the history list in session state if not already there
if "history" not in st.session_state:
    st.session_state["history"] = []

# Create a form for the user input
with st.form(key="calculation_form"):
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

    # Submit button for the form
    submit_button = st.form_submit_button("Calculate")

# Button logic after form submission
if submit_button:
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

# Display the history with checkboxes next to each calculation
if st.session_state["history"]:
    st.subheader("Calculation History")
    selected_calculations = []
    selected_names = []

    for idx, entry in enumerate(st.session_state["history"], start=1):
        # Display each calculation with a checkbox to select it
        checkbox = st.checkbox(f"Include {entry['name']} - {entry['result']}", key=f"checkbox_{idx}")
        if checkbox:
            selected_calculations.append(entry['result'])
            selected_names.append(entry['name'])

    # If no checkboxes are selected, include all calculations by default
    if not selected_calculations:
        selected_calculations = [entry['result'] for entry in st.session_state["history"]]
        selected_names = [entry['name'] for entry in st.session_state["history"]]

    # Button to sum the selected results
    if st.button("Sum Selected Calculations"):
        if selected_calculations:
            total_seconds = sum(convert_hhmmss_to_seconds(entry) for entry in selected_calculations)
            total_time = convert_seconds_to_hhmmss(total_seconds)
            selected_names_str = ", ".join(selected_names)
            st.success(f"Total time for selected calculations ({selected_names_str}): {total_time}")
        else:
            st.warning("No calculations selected to sum.")

# New section to add time
st.subheader("Add Time")
if "time_rows" not in st.session_state:
    st.session_state["time_rows"] = [{"hours": 0, "minutes": 0, "seconds": 0}]

# Add a new row of time input when the "+" button is clicked
if st.button("Add Row of Time"):
    st.session_state["time_rows"].append({"hours": 0, "minutes": 0, "seconds": 0})

# Display each row of time input
for i, row in enumerate(st.session_state["time_rows"]):
    col1, col2, col3, col4 = st.columns([3, 3, 3, 1])  # Adding one more column for the "-" button
    with col1:
        row["hours"] = st.number_input(f"Row {i+1} - Hours", min_value=0, max_value=23, value=row["hours"], key=f"hours_{i}")
    with col2:
        row["minutes"] = st.number_input(f"Row {i+1} - Minutes", min_value=0, max_value=59, value=row["minutes"], key=f"minutes_{i}")
    with col3:
        row["seconds"] = st.number_input(f"Row {i+1} - Seconds", min_value=0, max_value=59, value=row["seconds"], key=f"seconds_{i}")
    with col4:
        if st.button(f"-", key=f"remove_row_{i}"):
            st.session_state["time_rows"].pop(i)  # Remove the row when "-" button is clicked
            st.experimental_rerun()  # Refresh the page to reflect changes
