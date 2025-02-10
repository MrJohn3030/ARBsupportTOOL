import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
dashboard_data = pd.read_excel('data/arbo_dashboard.xlsx')
recommender_data = pd.read_csv('data/organization_recommender.csv')

st.title("Dashboard 📊")
st.image("data/images/handtractor.jpg")

# Counters
total_arbo = dashboard_data['ARBO'].nunique()
total_land = dashboard_data['Area of land given'].sum()

# Create centered and large icons with metrics
st.markdown("### Program Statistics")
metric_col1, metric_col2, metric_col3 = st.columns([1, 1, 1])

with metric_col1:
    st.markdown(
        """
        <div style="text-align: center;">
            <span style="font-size: 50px;">🏢</span>
            <h3>Number of Organizations</h3>
            <p style="font-size: 24px; font-weight: bold;">{}</p>
        </div>
        """.format(total_arbo), 
        unsafe_allow_html=True
    )

with metric_col2:
    st.markdown(
        """
        <div style="text-align: center;">
            <span style="font-size: 50px;">🗓️</span>
            <h3>Year Latest Title Registered</h3>
            <p style="font-size: 24px; font-weight: bold;">2012</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric_col3:
    st.markdown(
        """
        <div style="text-align: center;">
            <span style="font-size: 50px;">🌾</span>
            <h3>Total Land Distributed</h3>
            <p style="font-size: 24px; font-weight: bold;">{}(hectare)</p>
        </div>
        """.format(total_land), 
        unsafe_allow_html=True
    )


# Horizontal bar graph
bar_data = dashboard_data.groupby("Municipality").size().reset_index(name="Count")
bar_fig = px.bar(
    bar_data, 
    x="Count", 
    y="Municipality", 
    title="Number of Titles Given Per Municipality",
    orientation="h",  # Horizontal bar graph
    color="Municipality",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(bar_fig, use_container_width=True)


# Bar Graph
bar_data = dashboard_data.groupby("Program Type").size().reset_index(name="Count")
bar_fig = px.bar(bar_data, x="Program Type", y="Count", title="Program Type", color="Program Type")
st.plotly_chart(bar_fig, use_container_width=True)

# Line Graph
line_data = dashboard_data.groupby("Year Registered").size().reset_index(name="Count")
line_fig = px.line(line_data, x="Year Registered", y="Count", markers=True, title="Titles Registered From 1980-2012")
st.plotly_chart(line_fig, use_container_width=True)

# Bar Graph
bar_data = dashboard_data.groupby("ARBO").size().reset_index(name="Count")
bar_fig = px.bar(bar_data, x="ARBO", y="Count", title="Number of Memebers Per Organization", color="ARBO")
st.plotly_chart(bar_fig, use_container_width=True)

# Horizontal bar graph
bar_data = dashboard_data.groupby("MOA").size().reset_index(name="Count")
bar_fig = px.bar(
    bar_data, 
    x="Count", 
    y="MOA", 
    title="Mode of Acquisition",
    orientation="h",  # Horizontal bar graph
    color="MOA",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(bar_fig, use_container_width=True)

# Bar Graph
bar_data = dashboard_data.groupby("Administration").size().reset_index(name="Count")
bar_fig = px.bar(bar_data, x="Administration", y="Count", title="Titles Given By Administration", color="Administration")
st.plotly_chart(bar_fig, use_container_width=True)

st.image("data/images/farming.jpg",)
