
import streamlit as st
from utils import parse_gr_number, format_number_gr, format_percentage_gr
from discount_efficiency_growth_chart import calculate_discount_efficiency

def discount_efficiency_ui():
    st.subheader("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    default_values = {
        "current_sales": "120.000",
        "extra_sales": "15.000",
        "discount_rate": "3,5",
        "discount_acceptance": "70",
        "discount_days": "10",
        "non_discount_days": "40",
        "cash_days": "5",
        "cost_percent": "60",
        "wacc": "12",
        "suppliers_days": "30",
        "current_collection_days": "50"
    }

    col1, col2 = st.columns(2)

    with col1:
        current_sales_input = st.text_input("Τρέχουσες Πωλήσεις (€)", default_values["current_sales"])
        extra_sales_input = st.text_input("Επιπλέον Πωλήσεις (€)", default_values["extra_sales"])
        discount_rate_input = st.text_input("Ποσοστό Έκπτωσης (%)", default_values["discount_rate"])
        discount_acceptance_input = st.text_input("Ποσοστό Αποδοχής (%)", default_values["discount_acceptance"])
        discount_days_input = st.text_input("Ημέρες με Έκπτωση", default_values["discount_days"])
        non_discount_days_input = st.text_input("Ημέρες χωρίς Έκπτωση", default_values["non_discount_days"])

    with col2:
        cash_days_input = st.text_input("Ημέρες Πληρωμής Τοις Μετρητοίς", default_values["cash_days"])
        cost_percent_input = st.text_input("Μέσο Κόστος (%)", default_values["cost_percent"])
        wacc_input = st.text_input("WACC (%)", default_values["wacc"])
        suppliers_days_input = st.text_input("Ημέρες Πληρωμής Προμηθευτών", default_values["suppliers_days"])
        current_collection_days_input = st.text_input("Τρέχουσα Περίοδος Είσπραξης", default_values["current_collection_days"])

    current_sales = parse_gr_number(current_sales_input)
    extra_sales = parse_gr_number(extra_sales_input)
    discount_rate = parse_gr_number(discount_rate_input)
    discount_acceptance = parse_gr_number(discount_acceptance_input)
    discount_days = parse_gr_number(discount_days_input)
    non_discount_days = parse_gr_number(non_discount_days_input)

    cash_days = parse_gr_number(cash_days_input)
    cost_percent = parse_gr_number(cost_percent_input)
    wacc = parse_gr_number(wacc_input)
    suppliers_days = parse_gr_number(suppliers_days_input)
    current_collection_days = parse_gr_number(current_collection_days_input)

    if st.button("Υπολογισμός"):
        result = calculate_discount_efficiency(
            current_sales,
            extra_sales,
            discount_rate,
            discount_acceptance,
            discount_days,
            non_discount_days,
            cash_days,
            cost_percent,
            wacc,
            suppliers_days,
            current_collection_days
        )

        st.success(f"Αξία Προσαύξησης: {format_number_gr(result['value_of_growth'])} €")
        st.info(f"Καθαρό Όφελος: {format_number_gr(result['net_benefit'])} €")
        st.metric("Απόδοση (%)", format_percentage_gr(result["efficiency_percent"]))
