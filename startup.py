import streamlit as st

# Logo
sidebar_logo = ("data/images/olgobetter.png")  #logo if open
main_body_logo = ("data/images/arblogo.png") #logo if closed
st.logo (sidebar_logo,icon_image = main_body_logo,size="large")

pages = {
"Menu":[
    st.Page("home.py",title="Home",icon="🏠"),
    st.Page("dashboard.py",title="Dashboard",icon="📊"),
    st.Page("recommender.py",title="Recommender",icon="🔧"),
    st.Page("database.py",title="Database",icon="📁"),
],
}

pg=st.navigation(pages)
pg.run()
#streamlit run startup.py