# discount_cash_app.py

import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct
from utils import parse_gr_number, format_number_gr, format_percentage_gr

def show_discount_cash_app():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς (60% σταθμισμένο)")

    with st.form("discount_cash_form"):
        col1, col2 = st.columns(2)
        with col1:
            current_sales = parse_gr_number(st.text_input("Τρέχουσες Πωλήσεις (€)", "1.000"))
            extra_sales = parse_gr_number(st.text_input("Επιπλέον Πωλήσεις από την Έκπτωση (€)", "250"))
            cash_discount_rate = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", 0.0, 100.0, 2.0) / 100
            pct_customers_accept = st.slider("% των πελατών που αποδέχονται την έκπτωση", 0, 100, 50)
        with col2:
            days_accept = st.number_input("Ημέρες είσπραξης (με έκπτωση)", 1, 180, 10)
            days_reject = st.number_input("Ημέρες είσπραξης (χωρίς έκπτωση)", 1, 365, 120)
            cost_of_sales_pct = st.number_input("Κόστος Πωλήσεων (%)", 0.0, 100.0, 80.0) / 100
            cost_of_capital_annual = st.number_input("Κόστος Κεφαλαίου (%)", 0.0, 100.0, 20.0) / 100
            avg_supplier_pay_days = st.number_input("Μέρες αποπληρωμής Προμηθευτών", 0, 365, 0)

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_discount_cash_fixed_pct(
            current_sales=current_sales,
            extra_sales=extra_sales,
            cash_discount_rate=cash_discount_rate,
            pct_customers_accept=pct_customers_accept,  # διατηρείται για συμβατότητα, δεν επηρεάζει
            days_accept=days_accept,
            days_reject=days_reject,
            cost_of_sales_pct=cost_of_sales_pct,
            cost_of_capital_annual=cost_of_capital_annual,
            avg_supplier_pay_days=avg_supplier_pay_days
        )

        st.subheader("📊 Αποτελέσματα")
        st.metric("Κέρδος από Επιπλέον Πωλήσεις", format_number_gr(results["Gross Profit Extra Sales"]) + " €")
        st.metric("NPV", format_number_gr(results["NPV"]) + " €")
        st.metric("Μέγιστη Έκπτωση που μπορεί να δοθεί (Break-even)", format_percentage_gr(results["Max Discount %"]))
        st.metric("Βέλτιστη Έκπτωση που πρέπει να δοθεί", format_percentage_gr(results["Optimal Discount %"]))
