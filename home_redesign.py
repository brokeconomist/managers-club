import streamlit as st

# Εδώ κάνουμε import όλα τα modules σου
from break_even import break_even_ui
from clv_calculator import clv_ui
from substitution_analysis import substitution_ui
from complementary_analysis import complementary_ui
from price_impact import price_impact_ui
from cash_discount import cash_discount_ui

def show_homepage():
    st.title("👋 Καλώς ήρθες στο Managers’ Club")

    st.write("""
    Αυτό είναι το προσωπικό σου dashboard.  
    Εδώ μπορείς να επιλέξεις γρήγορα ποιο εργαλείο θέλεις να χρησιμοποιήσεις.
    """)

    # Tabs για κάθε ομάδα εργαλείων
    tab1, tab2, tab3 = st.tabs(["Οικονομικά & CLV", "Ανάλυση προϊόντων", "Ταμειακά & Τιμές"])

    # --- Οικονομικά & CLV ---
    with tab1:
        if st.button("Break-Even"):
            break_even_ui()
        if st.button("CLV - Αξία Πελάτη"):
            clv_ui()

    # --- Ανάλυση προϊόντων ---
    with tab2:
        if st.button("Υποκατάστατα"):
            substitution_ui()
        if st.button("Συμπληρωματικά"):
            complementary_ui()

    # --- Ταμειακά & Τιμές ---
    with tab3:
        if st.button("Επίδραση Τιμής"):
            price_impact_ui()
        if st.button("Αποδοτικότητα Έκπτωσης Μετρητοίς"):
            cash_discount_ui()
