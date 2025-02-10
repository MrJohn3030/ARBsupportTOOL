import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
dashboard_data = pd.read_excel('data/arbo_dashboard.xlsx')
recommender_data = pd.read_csv('backups/organization_recommender.csv')

# Logo
st.logo("data/images/darlogo.jpg",title="DAR' ARB SUPPORT SYSTEM")

# Sidebar menu
menu = st.sidebar.radio(
    "MENU",
    ["Home","Database","Dashboard","Recommender"]
   
)
# Home Page
if menu == "Home":
    st.title("Welcome to DAR's ARB Support System")
    st.image("data/images/placeholder.png", caption="DAR Initiative")
    st.markdown("### About the Program")
    st.write("DAR's ARB program supports agricultural reform beneficiaries in Quirino province.")

    # Counters
    st.markdown("### Key Metrics")
    total_arbo = dashboard_data['ARBO'].nunique()
    total_land = dashboard_data['Area of land given'].sum()
    st.write(f"**Number of Active Organizations:** {total_arbo}")
    st.write(f"**Year Latest Title Registered: 2012** ")
    st.write(f"**Total Land Distributed (hectares):** {total_land}")

# Database
elif menu == "Database":
    st.title("ARBO Database ")
    st.image("data/images/placeholder.jpg", caption="Dashboard Overview")
    st.dataframe(dashboard_data)

# Dashboard
elif menu == "Dashboard":
    st.title("Graphs and Visualizations")

    # Bar Graph
    bar_data = dashboard_data.groupby("Municipality").size().reset_index(name="Count")
    bar_fig = px.bar(bar_data, x="Municipality", y="Count", title="Number of Titles Given Per Municipality", color="Municipality")
    st.plotly_chart(bar_fig, use_container_width=True)

    # Line Graph
    line_data = dashboard_data.groupby("Year Registered").size().reset_index(name="Count")
    line_fig = px.line(line_data, x="Year Registered", y="Count", markers=True, title="Titles Registered Per Year")
    st.plotly_chart(line_fig, use_container_width=True)
    
    # Bar Graph
    bar_data = dashboard_data.groupby("ARBO").size().reset_index(name="Count")
    bar_fig = px.bar(bar_data, x="ARBO", y="Count", title="Number of Memebers Per Organization", color="ARBO")
    st.plotly_chart(bar_fig, use_container_width=True)

    # Bar Graph
    bar_data = dashboard_data.groupby("Administration").size().reset_index(name="Count")
    bar_fig = px.bar(bar_data, x="Administration", y="Count", title="Titles Given By Administration", color="Administration")
    st.plotly_chart(bar_fig, use_container_width=True)

# Recommender
elif menu == "Recommender":
    st.title("ARBO Recommender System")
    st.image("data/images/placeholder.jpg", caption="Recommendation System")
    st.markdown("### Enter Details to Get Organization Recommendations")

    #Input Fields
    municipality = st.selectbox("Select Municipality", recommender_data['Municipality'].unique())

    barangays_list = recommender_data[recommender_data['Municipality'] == municipality]['Barangays']
    barangays_split = set()
    for barangays in barangays_list:
        barangays_split.update(barangays.split(","))
        
    barangay = st.selectbox("Select Barangay", sorted (barangays_split))
    services = st.text_input ("Services (optional)")
    
        
    # Filter data
    filtered_data = recommender_data[
        (recommender_data['Municipality'] == municipality) & 
        (recommender_data['Barangays'].str.contains  (barangay)) ]
    
    if services:
        filtered_data= filtered_data[filtered_data['Services'].str.contains(services, case=False, na=False)]
   
    st.write("### Organization Recommendations:")
    st.dataframe(filtered_data)
