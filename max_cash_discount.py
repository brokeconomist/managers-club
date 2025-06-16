# max_cash_discount.py
import streamlit as st
from dmax_logic import calculate_max_cash_discount
from utils import format_percentage_gr, parse_gr_number

def show_max_cash_discount_ui():
    st.header("📉 Μέγιστη Αποδεκτή Έκπτωση Τοις Μετρητοίς")
    st.markdown(
        """
        Υπολογισμός της **μέγιστης έκπτωσης** που μπορεί να προσφέρει μια επιχείρηση 
        σε πελάτες για **πρόωρη πληρωμή**, ώστε η απόφαση να είναι οικονομικά συμφέρουσα 
        (χωρίς ζημία από την απώλεια του οφέλους πίστωσης).
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        days_saved_str = st.text_input("📆 Ημέρες που κερδίζονται με πρόωρη πληρωμή", value="30")
    with col2:
        annual_rate_str = st.text_input("💰 Ετήσιο Κόστος Κεφαλαίου (WACC, %)", value="12,00")

    try:
        days_saved = parse_gr_number(days_saved_str)
        annual_rate = parse_gr_number(annual_rate_str) / 100

        if days_saved <= 0 or annual_rate <= 0:
            st.warning("🔎 Παρακαλώ εισάγετε θετικές τιμές.")
            return

        max_discount = calculate_max_cash_discount(days_saved, annual_rate)

        st.success(f"✅ Μέγιστη αποδεκτή έκπτωση: **{format_percentage_gr(max_discount)}**")
        st.caption("Πέραν αυτής της έκπτωσης, συμφέρει περισσότερο να χρηματοδοτείται ο πελάτης μέσω της πίστωσης.")

    except Exception:
        st.error("❌ Σφάλμα στους υπολογισμούς. Ελέγξτε τα δεδομένα.")
