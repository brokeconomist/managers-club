import streamlit as st
from discount_cash_chart import calculate_discount_cash
from utils import format_number_gr, parse_gr_number, format_percentage_gr

def discount_cash_ui():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    col1, col2 = st.columns(2)

    with col1:
        current_sales = parse_gr_number(st.text_input("Τρέχουσες Πωλήσεις (€)", "1.000"))
        extra_sales = parse_gr_number(st.text_input("Επιπλέον Πωλήσεις από την Έκπτωση (€)", "250"))
        cash_discount_rate = st.slider("Ποσοστό Έκπτωσης (%)", 0.0, 10.0, 2.0, step=0.25) / 100
        pct_customers_discount_total = st.slider("Ποσοστό Πελατών που Πληρώνουν με Έκπτωση (%)", 0.0, 100.0, 60.0, step=1.0) / 100

    with col2:
        days_accept = st.number_input("Μέρες Είσπραξης για Πελάτες με Έκπτωση", min_value=1, value=10)
        days_reject = st.number_input("Μέρες Είσπραξης για Υπόλοιπους Πελάτες", min_value=1, value=120)
        cost_of_sales_pct = st.slider("Κόστος Πωληθέντων (% επί των πωλήσεων)", 0.0, 100.0, 80.0, step=1.0) / 100
        cost_of_capital_annual = st.slider("Ετήσιο Κόστος Κεφαλαίου (%)", 0.0, 50.0, 20.0, step=0.5) / 100
        avg_supplier_pay_days = st.number_input("Μέρες Αποπληρωμής Προμηθευτών", min_value=0, value=0)

    if st.button("Υπολογισμός"):
        results = calculate_discount_cash(
            current_sales,
            extra_sales,
            cash_discount_rate,
            pct_customers_discount_total,
            days_accept,
            days_reject,
            cost_of_sales_pct,
            cost_of_capital_annual,
            avg_supplier_pay_days
        )

        st.success("Αποτελέσματα:")
        st.metric("Καθαρή Παρούσα Αξία (NPV)", format_number_gr(results["NPV"]) + " €")
        st.metric("Μέγιστο Ποσοστό Έκπτωσης", format_percentage_gr(results["Max Discount %"]))
        st.metric("Βέλτιστο Ποσοστό Έκπτωσης", format_percentage_gr(results["Optimal Discount %"]))
