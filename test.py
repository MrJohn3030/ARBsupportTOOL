import streamlit as st
import pandas as pd
import pickle
import plotly.express as px

# Load trained model
with open("program_recommender_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Load organization data
organization_data = pd.read_csv("data/organization_recommender.csv")

# Path to store the results
results_database_path = "data/programprediction.csv"

# Function to save results to the database
def save_to_database(data: pd.DataFrame, file_path: str):
    try:
        # Append data to the existing file if it exists
        existing_data = pd.read_csv(file_path)
        combined_data = pd.concat([existing_data, data], ignore_index=True)
        combined_data.to_csv(file_path, index=False)
    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        data.to_csv(file_path, index=False)

# Streamlit app
st.title("ARBO Program Recommender System 🌾")
st.markdown("A tool to recommend ARBO programs and organizations based on user data.")

# Horizontal radio button for mode selection
st.markdown("### Choose Input Mode:")
mode = st.radio("", ["Single Entry", "Batch Upload"], horizontal=True)

if mode == "Single Entry":
    # Input fields for single entry
    st.markdown("### Enter User Information")
    municipality = st.selectbox("Municipality 📍", organization_data['Municipality'].unique())
    
    # Parse and filter barangays dynamically
    barangays_list = organization_data[organization_data['Municipality'] == municipality]['Barangay']
    barangay_set = set()
    for barangays in barangays_list:
        barangay_set.update(barangays.split(", "))
    barangay = st.selectbox("Barangay 📍", sorted(barangay_set))
    
    land_size = st.number_input("Land Size (in hectares)", min_value=0.0, step=0.1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    ownership_type = st.selectbox("Ownership Type", ["Individual", "Co-Ownership", "Collective", "Cooperative"])
    organization_membership = st.selectbox("Organization Membership", ["Yes", "No"])

    if st.button("Get Recommendations"):
        # Prepare input for prediction
        input_data = pd.DataFrame({
            'Municipality': [municipality],
            'Barangay': [barangay],
            'Land Size': [land_size],
            'Gender': [gender],
            'Ownership Type': [ownership_type],
            'Organization Membership': [organization_membership]
        })
        
        # Predict programs using the model
        recommended_programs = model.predict(input_data[['Land Size', 'Gender', 'Ownership Type', 'Organization Membership']])[0]
        
        # Add the recommendation to the input data
        input_data['Recommended Programs'] = recommended_programs
        
        # Save to database
        save_to_database(input_data, results_database_path)
        
        # Organization details
        if organization_membership == "Yes":
            member_orgs = organization_data[
                (organization_data['Municipality'] == municipality) & 
                (organization_data['Barangay'].str.contains(barangay))
            ]
            org_message = (
                f"### Organization Membership Details:\n"
                f"You are a member of the following organizations in {barangay}, {municipality}:\n\n"
            )
            for _, row in member_orgs.iterrows():
                org_message += f"- **{row['Organization']}**: {row['Services']}\n"
        else:
            suggestions = organization_data[
                (organization_data['Municipality'] == municipality) & 
                (organization_data['Barangay'].str.contains(barangay))
            ]
            org_message = (
                f"### Suggested Organizations to Join:\n"
                f"Based on your location in {barangay}, {municipality}, consider joining:\n\n"
            )
            for _, row in suggestions.iterrows():
                org_message += f"- **{row['Organization']}**: {row['Services']}\n"

        # Generate program details
        program_message = f"### Recommended Programs Based on Your Inputs:\n{recommended_programs}\n\n"
        
        # Display the report
        st.markdown("## Recommendation Report 📝")
        with st.expander("View Recommendation Report"):
            st.markdown(f"#### Summary for {barangay}, {municipality}")
            st.markdown(org_message)
            st.markdown(program_message)

        # Popup-like alerts
        st.success("Your personalized recommendation report has been saved and is ready! Scroll down to view it.")

elif mode == "Batch Upload":
    st.markdown("### Upload CSV File for Batch Processing")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read the uploaded file
        user_data = pd.read_csv(uploaded_file)
        
        # Check required columns
        required_columns = ['Municipality', 'Barangay', 'Land Size', 'Gender', 'Ownership Type', 'Organization Membership']
        if not all(col in user_data.columns for col in required_columns):
            st.error(f"CSV file must contain the following columns: {', '.join(required_columns)}")
        else:
            # Predict for each row in the dataset
            predictions = []
            for _, row in user_data.iterrows():
                input_data = pd.DataFrame({
                    'Land Size': [row['Land Size']],
                    'Gender': [row['Gender']],
                    'Ownership Type': [row['Ownership Type']],
                    'Organization Membership': [row['Organization Membership']]
                })
                predicted_program = model.predict(input_data)[0]
                predictions.append(predicted_program)
            
            # Add predictions to the dataframe
            user_data['Recommended Programs'] = predictions
            
            # Save to database
            save_to_database(user_data, results_database_path)
            
            # Display results
            st.success("Batch processing complete! The results have been saved.")
            st.dataframe(user_data)
            
            # Dashboard Insights
            st.markdown("## Dashboard Insights 📈")
            
            # Visualization 1: Distribution of Recommended Programs
            st.markdown("### Distribution of Recommended Programs")
            fig1 = px.histogram(user_data, x="Recommended Programs", title="Program Recommendation Distribution")
            st.plotly_chart(fig1)
            
            # Visualization 2: Program Recommendations by Ownership Type
            st.markdown("### Program Recommendations by Ownership Type")
            fig2 = px.bar(user_data, x="Ownership Type", color="Recommended Programs",
                          title="Program Recommendations by Ownership Type", barmode="group")
            st.plotly_chart(fig2)
            
            # Visualization 3: Gender Distribution in Recommendations
            st.markdown("### Gender Distribution in Recommendations")
            fig3 = px.pie(user_data, names="Gender", title="Gender Distribution in Recommendations")
            st.plotly_chart(fig3)
            
            # Download results
            csv = user_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="batch_recommendations.csv",
                mime="text/csv"
            )
