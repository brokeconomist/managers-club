import streamlit as st
from credit_policy_analysis import manosv_cash_credit_control

st.set_page_config(page_title="Ανάλυση Πολιτικής Πίστωσης", layout="centered")

st.title("📊 Ανάλυση Πολιτικής Πίστωσης (Μετρητοίς & Πίστωση)")

st.header("📌 Παρούσα Κατάσταση")
current_cash = st.number_input("Ποσοστό Μετρητοίς (%)", value=50.0) / 100
current_credit = st.number_input("Ποσοστό Πίστωσης (%)", value=50.0) / 100
current_days = st.number_input("Μέρες Πίστωσης", value=60)

st.header("📈 Νέα Πρόταση")
new_cash = st.number_input("Νέο Ποσοστό Μετρητοίς (%)", value=20.0) / 100
new_credit = st.number_input("Νέο Ποσοστό Πίστωσης (%)", value=80.0) / 100
new_days = st.number_input("Νέες Μέρες Πίστωσης", value=90)
sales_increase = st.number_input("Ποσοστό Αύξησης Πωλήσεων (%)", value=20.0) / 100

st.header("💼 Οικονομικά Δεδομένα")
sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=20_000_000)
price = st.number_input("Τιμή Μονάδας (€)", value=20.0)
total_cost = st.number_input("Συνολικό Κόστος ανά Μονάδα (€)", value=18.0)
variable_cost = st.number_input("Μεταβλητό Κόστος ανά Μονάδα (€)", value=14.0)
bad_debts = st.number_input("Ποσοστό Επισφαλειών (%)", value=2.0) / 100
interest_rate = st.number_input("Κόστος Κεφαλαίου (%)", value=10.0) / 100

if st.button("Υπολογισμός"):
    results = manosv_cash_credit_control(
        current_cash,
        current_credit,
        current_days,
        new_cash,
        new_credit,
        new_days,
        sales_increase,
        sales,
        price,
        total_cost,
        variable_cost,
        bad_debts,
        interest_rate
    )

    st.header("📊 Αποτελέσματα")
    st.metric("Καθαρό Κέρδος (€)", f"{results['Net Profit']:,.2f}")
    st.metric("Κόστος Κεφαλαίου (€)", f"{results['Capital Cost']:,.2f}")
    st.metric("Κόστος Επισφαλειών (€)", f"{results['Bad Debts Cost']:,.2f}")
    st.metric("Συνολικό Κόστος (€)", f"{results['Total Cost']:,.2f}")
    st.metric("Καθαρό Όφελος (€)", f"{results['Anticipated Gain']:,.2f}")
    st.success(f"Πρόταση: {results['Suggestion']}")
