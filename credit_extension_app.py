import streamlit as st
from credit_extension_analysis import calculate_credit_extension_simple

st.set_page_config(page_title="Ανάλυση Επέκτασης Πίστωσης", layout="centered")

st.title("📊 Ανάλυση Επέκτασης Χρόνου Πίστωσης")

st.header("📌 Τρέχουσα Κατάσταση")
current_credit_days = st.number_input("Μέρες Πίστωσης", value=60, min_value=1)

st.header("📈 Νέα Πρόταση")
new_credit_days = st.number_input("Νέες Μέρες Πίστωσης", value=90, min_value=1)
sales_increase_pct = st.number_input("Ποσοστό Αύξησης Πωλήσεων (%)", value=20.0, step=1.0) / 100

st.header("💼 Οικονομικά Δεδομένα")
current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=20_000_000, step=100_000)
unit_price = st.number_input("Τιμή Μονάδας (€)", value=20.0)
total_unit_cost = st.number_input("Συνολικό Κόστος ανά Μονάδα (€)", value=18.0)
variable_unit_cost = st.number_input("Μεταβλητό Κόστος ανά Μονάδα (€)", value=14.0)
bad_debt_pct = st.number_input("Ποσοστό Επισφαλειών (%)", value=2.0) / 100
capital_cost_pct = st.number_input("Κόστος Κεφαλαίου (%)", value=10.0) / 100

if st.button("Υπολογισμός"):
    results = calculate_credit_extension_simple(
        current_credit_days,
        new_credit_days,
        sales_increase_pct,
        current_sales,
        unit_price,
        total_unit_cost,
        variable_unit_cost,
        bad_debt_pct,
        capital_cost_pct,
    )

    st.header("📊 Αποτελέσματα")
    st.metric("Καθαρό Κέρδος (€)", f"{results['Net Profit']:,.2f}")
    st.metric("Συνολικό Κόστος (€)", f"{results['Total Cost from Increase']:,.2f}")
    st.metric("Εκτιμώμενο Κέρδος (€)", f"{results['Anticipated Gain']:,.2f}")
    st.success(f"Πρόταση: {results['Suggestion']}")
