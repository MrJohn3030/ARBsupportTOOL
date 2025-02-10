import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
dashboard_data = pd.read_excel('data/arbo_dashboard.xlsx')

st.title("Welcome to DAR's ARB Support System")
st.image("data/images/darlogo.jpeg")
st.markdown("### About the Program")
st.write("The Department of Agrarian Reform’s Agrarian Reform Beneficiaries (ARB) Program is a cornerstone initiative aimed at empowering farmers by granting them access to land ownership, resources, and support services. Through this program, DAR facilitates the distribution of agricultural lands, ensures security of tenure, and provides capacity-building measures to enhance agricultural productivity. The program also fosters the development of Agrarian Reform Beneficiaries Organizations (ARBOs), promoting cooperative management and sustainable development within farming communities. By addressing rural poverty and improving livelihoods, the ARB program plays a critical role in advancing equitable and inclusive growth in the agricultural sector.")

st.image("data/images/kubota.jpg")