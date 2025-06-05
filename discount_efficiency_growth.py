import streamlit as st
from utils import parse_gr_number, format_number_gr, format_percentage_gr

def calculate_discount_efficiency(current_sales, projected_sales, price_per_unit, unit_cost, receivables_before, receivables_after, wacc):
    cash_flow_before = (current_sales * (price_per_unit - unit_cost)) - receivables_before
    cash_flow_after = (projected_sales * (price_per_unit - unit_cost)) - receivables_after
    capital_release = receivables_before - receivables_after
    capital_productivity = (cash_flow_after - cash_flow_before) / capital_release if capital_release != 0 else 0
    decision = "Συμφέρει" if capital_productivity > wacc else "Δεν συμφέρει"

    return {
        "Απελευθέρωση Κεφαλαίου": capital_release,
        "Απόδοση Κεφαλαίου": capital_productivity,
        "Απόφαση": decision
    }

def discount_efficiency_ui():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς λόγω Ανάπτυξης")

    default_values = {
        "current_sales": "100.000",
        "projected_sales": "120.000",
        "price_per_unit": "15,00",
        "unit_cost": "9,00",
        "receivables_before": "30.000",
        "receivables_after": "24.000",
        "wacc": "8,00"
    }

    col1, col2 = st.columns(2)

    with col1:
        current_sales = st.text_input("Τρέχουσες Πωλήσεις (€)", value=default_values["current_sales"])
        projected_sales = st.text_input("Αναμενόμενες Πωλήσεις (€)", value=default_values["projected_sales"])
        price_per_unit = st.text_input("Τιμή Μονάδας (€)", value=default_values["price_per_unit"])
        unit_cost = st.text_input("Μοναδιαίο Κόστος (€)", value=default_values["unit_cost"])

    with col2:
        receivables_before = st.text_input("Απαιτήσεις Πριν (€)", value=default_values["receivables_before"])
        receivables_after = st.text_input("Απαιτήσεις Μετά (€)", value=default_values["receivables_after"])
        wacc = st.text_input("Κόστος Κεφαλαίου WACC (%)", value=default_values["wacc"])

    if st.button("Υπολογισμός"):
        try:
            results = calculate_discount_efficiency(
                parse_gr_number(current_sales),
                parse_gr_number(projected_sales),
                parse_gr_number(price_per_unit),
                parse_gr_number(unit_cost),
                parse_gr_number(receivables_before),
                parse_gr_number(receivables_after),
                parse_gr_number(wacc) / 100
            )

            st.subheader("Αποτελέσματα")
            st.write(f"**Απελευθέρωση Κεφαλαίου:** {format_number_gr(results['Απελευθέρωση Κεφαλαίου'])} €")
            st.write(f"**Απόδοση Κεφαλαίου:** {format_percentage_gr(results['Απόδοση Κεφαλαίου'])}")
            st.write(f"**Απόφαση:** {results['Απόφαση']}")

        except Exception as e:
            st.error(f"Παρουσιάστηκε σφάλμα: {e}")
