import streamlit as st
from credit_extension_analysis import show_credit_extension_analysis
show_credit_extension_analysis()
st.set_page_config(page_title="Ανάλυση Επέκτασης Πίστωσης", layout="centered")

st.title("📊 Ανάλυση Επέκτασης Χρόνου Πίστωσης")

st.header("📌 Τρέχουσα Κατάσταση")
current_credit_days = st.number_input("Μέρες Πίστωσης", value=60, min_value=1)

st.header("📈 Νέα Πρόταση")
new_credit_days = st.number_input("Νέες Μέρες Πίστωσης", value=90, min_value=1)
sales_increase_pct_input = st.number_input("Ποσοστό Αύξησης Πωλήσεων (%)", value=20.0, step=1.0)

st.header("💼 Οικονομικά Δεδομένα")
current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=20_000_000, step=100_000)
unit_price = st.number_input("Τιμή Μονάδας (€)", value=20.0)
total_unit_cost = st.number_input("Συνολικό Κόστος ανά Μονάδα (€)", value=18.0)
variable_unit_cost = st.number_input("Μεταβλητό Κόστος ανά Μονάδα (€)", value=14.0)
bad_debt_pct_input = st.number_input("Ποσοστό Επισφαλειών (%)", value=2.0)
capital_cost_pct_input = st.number_input("Κόστος Κεφαλαίου (%)", value=10.0)

if st.button("📊 Υπολογισμός"):
    results = calculate_credit_extension_simple(
        current_credit_days,
        new_credit_days,
        sales_increase_pct_input / 100,
        current_sales,
        unit_price,
        total_unit_cost,
        variable_unit_cost,
        bad_debt_pct_input / 100,
        capital_cost_pct_input / 100,
    )

    st.header("📊 Αποτελέσματα")
    st.metric("Καθαρό Κέρδος (€)", results["Formatted"]["Net Profit"])
    st.metric("Συνολικό Κόστος (€)", results["Formatted"]["Total Cost from Increase"])
    st.metric("Εκτιμώμενο Κέρδος (€)", results["Formatted"]["Anticipated Gain"])
    if "✅" in results["Suggestion"]:
        st.success(f"Πρόταση: {results['Suggestion']}")
    else:
        st.warning(f"Πρόταση: {results['Suggestion']}")
