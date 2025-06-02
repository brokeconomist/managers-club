import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct

st.set_page_config(page_title="Ανάλυση Έκπτωσης για Πληρωμή Τοις Μετρητοίς", layout="centered")

st.title("Ανάλυση Έκπτωσης για Πληρωμή Τοις Μετρητοίς")

st.markdown("## Εισαγωγή Δεδομένων")

current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", min_value=0.0, value=1000.0)
additional_sales = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", min_value=0.0, value=250.0)
discount_pct = st.number_input("Ποσοστό Έκπτωσης (%)", min_value=0.0, max_value=100.0, value=2.0)
acceptance_rate = st.number_input("Ποσοστό Πελατών που Αποδέχονται την Έκπτωση (%)", min_value=0.0, max_value=100.0, value=50.0)
days_discount = st.number_input("Μέρες Πληρωμής για Έκπτωση", min_value=0, value=10)
days_no_discount = st.number_input("Μέρες Πληρωμής χωρίς Έκπτωση", min_value=0, value=120)
cost_pct = st.number_input("Κόστος Πωλήσεων (% επί των Πωλήσεων)", min_value=0.0, max_value=100.0, value=80.0)
wacc = st.number_input("Κόστος Κεφαλαίου (% Ετησίως)", min_value=0.0, max_value=100.0, value=20.0)
supplier_days = st.number_input("Μέση Περίοδος Αποπληρωμής Προμηθευτών (ημέρες)", min_value=0, value=0)
current_collection_days = st.number_input("Τρέχουσα Μέση Περίοδος Είσπραξης (ημέρες)", min_value=0, value=90)

if st.button("Υπολογισμός"):
    result = calculate_discount_cash_fixed_pct(
        current_sales=current_sales,
        additional_sales=additional_sales,
        discount_percentage=discount_pct,
        acceptance_rate=acceptance_rate,
        days_discount=days_discount,
        days_no_discount=days_no_discount,
        cost_percentage=cost_pct,
        wacc=wacc,
        supplier_days=supplier_days,
        current_collection_days=current_collection_days
    )

    st.subheader("Αποτελέσματα")
    st.write(f"**NPV (€):** {result['NPV']}")
    st.write(f"**Μέγιστη Δυνητική Έκπτωση (%):** {result['max_discount_pct']}%")
    st.write(f"**Βέλτιστη Έκπτωση (%):** {result['optimal_discount_pct']}%")