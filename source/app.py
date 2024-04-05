import streamlit as st
from data_collection import *
from data_summary import *
import os


# Function to load JSON data
def load_json_data(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        return None
    

# Define the main function to run the Streamlit app
def main():
    # Set the title of the web app
    st.title("Discussion Analysis Dashboard")

    # Create a form to accept inputs from the user
    city_name = st.text_input("Enter the city name:")
    
    # Add a button to trigger the analysis
    if st.button("Analyze Discussions"):
        # Collect NEWS of city & save it as json
        st.write("Getting NEWS headings...")
        save_data(city_name)
        st.write("NEWS data saved...")
        st.write("Data Loading...")

        # Load JSON data
        json_file_path = 'data\city_data.json'
        data = load_json_data(json_file_path)

        # Check if data is available
        if data:
            st.write(f"Analysis Result of: {city_name}")
            for topic, comments_info in data.items():
                # Summarize diverse viewpoints
                positive_summary, negative_summary, neutral_summary = summarize_viewpoints(comments_info)

                # Present the information
                with st.container():
                    st.markdown(f"<h5 style='text-align: center; background-color: #dff9ff; color: black; border-radius: 10px; margin-bottom: 25px;'>Topic: {topic}<br><br>Positive Viewpoints:<br>{positive_summary}<br><br>Negative Viewpoints:<br>{negative_summary}<br><br>Neutral Viewpoints:<br>{neutral_summary}</h5>", unsafe_allow_html=True)
        else:
            st.error("Failed to load JSON data.")

# Run the main function to start the Streamlit app
if __name__ == "__main__":
    main()