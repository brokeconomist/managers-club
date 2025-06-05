import streamlit as st
from credit_extension_analysis import calculate_credit_extension_impact
from utils import format_number_gr, format_percentage_gr

st.set_page_config(page_title="Ανάλυση Επέκτασης Πίστωσης", layout="centered")

st.title("📊 Ανάλυση Επέκτασης Χρόνου Πίστωσης")

st.header("📌 Τρέχουσα Κατάσταση")
current_credit_days = st.number_input("Μέρες Πίστωσης", value=60, min_value=1)

st.header("📈 Νέα Πρόταση")
new_credit_days = st.number_input("Νέες Μέρες Πίστωσης", value=90, min_value=1)
sales_increase_pct = st.number_input("Ποσοστό Αύξησης Πωλήσεων (%)", value=20.0, step=1.0)

st.header("💼 Οικονομικά Δεδομένα")
current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=20_000_000, step=100_000)
unit_price = st.number_input("Τιμή Μονάδας (€)", value=20.0)
total_unit_cost = st.number_input("Συνολικό Κόστος ανά Μονάδα (€)", value=18.0)
variable_unit_cost = st.number_input("Μεταβλητό Κόστος ανά Μονάδα (€)", value=14.0)
bad_debt_pct = st.number_input("Ποσοστό Επισφαλειών (%)", value=2.0)
capital_cost_pct = st.number_input("Κόστος Κεφαλαίου (%)", value=10.0)

if st.button("Υπολογισμός"):
    results = calculate_credit_extension_impact(
        current_sales,
        unit_price,
        variable_unit_cost,
        sales_increase_pct,
        bad_debt_pct,
        capital_cost_pct,
        new_credit_days - current_credit_days,
    )

    if "error" in results:
        st.error(f"❌ Σφάλμα: {results['error']}")
    else:
        st.header("📊 Αποτελέσματα")
        st.metric("Καθαρό Κέρδος (€)", format_number_gr(results["Net Profit"]))
        st.metric("Συνολικό Κόστος (€)", format_number_gr(results["Total Cost from Increase"]))
        st.metric("Εκτιμώμενο Κέρδος (€)", format_number_gr(results["Anticipated Gain"]))

        if results["Suggestion"] == "Αύξησε την Πίστωση":
            st.success(f"📌 Πρόταση: ✅ {results['Suggestion']}")
        else:
            st.warning(f"📌 Πρόταση: ⛔️ {results['Suggestion']}")
