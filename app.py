# app.py (home)
import streamlit as st

# Import το περιεχόμενο της αρχικής (μπορεί να είναι και σε home.py)
from home import show_home

st.set_page_config(page_title="Managers’ Club", page_icon="📊", layout="wide")

# Αν θέλεις, show_home() περιέχει τα κουμπιά που κάνουν switch_page.
show_home()
