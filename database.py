import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
dashboard_data = pd.read_excel('data/arbo_dashboard.xlsx')
recommender_data = pd.read_csv('data/organization_recommender.csv')
data = pd.read_csv("data/programprediction.csv")

# Database
st.title("ARB Database 📁")
st.write("The database serves as a historical archive, spanning the years 1980 to 2012, documenting key milestones in the land redistribution efforts under the Department of Agrarian Reform (DAR). This period encompasses the leadership of various Philippine administrations, each contributing unique policies and programs to the agrarian reform agenda.The dataset highlights the evolution of land tenure instruments, transitioning from Emancipation Patents (EP) in the earlier years to Certificates of Land Ownership Award (CLOA), which became the primary mechanism for land transfer under the Comprehensive Agrarian Reform Program (CARP)")

st.dataframe(dashboard_data)

st.write("This archive not only records historical achievements but also serves as a tool for analysis and reflection, enabling a deeper understanding of the DAR's impact and progress over three decades.")

st.title("ARBO Database 📁")
st.dataframe(recommender_data)
st.write("Organizations Information")

st.title("Recommendation Database 📁")
st.dataframe(data)
st.write("The compilation of data beings used by the Model to make recommendation.")