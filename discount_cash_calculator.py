import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct as calculate_discount_cash
from utils import parse_gr_number, format_number_gr, format_percentage_gr

def show_discount_cash_calculator():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    with st.form("discount_cash_form"):
        current_sales = parse_gr_number(st.text_input("Τρέχουσες Πωλήσεις (€)", "100000"))
        extra_sales = parse_gr_number(st.text_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", "20000"))
        cash_discount_rate = st.slider("Ποσοστό Έκπτωσης", 0.0, 0.1, 0.02, step=0.005)

        pct_customers_accept = st.slider(
            "Ποσοστό Παλαιών Πελατών που αποδέχονται την έκπτωση (%)",
            0.0, 1.0, 0.5, step=0.05
        )

        days_accept = st.number_input("Ημέρες πληρωμής με έκπτωση", min_value=0, value=10)
        days_reject = st.number_input("Ημέρες πληρωμής χωρίς έκπτωση", min_value=0, value=120)
        avg_supplier_pay_days = st.number_input("Μέρες αποπληρωμής Προμηθευτών", min_value=0, value=0)

        cost_of_sales_pct = st.slider("Κόστος Πωληθέντων (%)", 0.0, 1.0, 0.8, step=0.05)
        cost_of_capital_annual = st.slider("Ετήσιο Κόστος Κεφαλαίου (%)", 0.0, 1.0, 0.2, step=0.01)

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        result = calculate_discount_cash(
            current_sales=current_sales,
            extra_sales=extra_sales,
            cash_discount_rate=cash_discount_rate,
            pct_customers_accept=pct_customers_accept,
            days_accept=days_accept,
            days_reject=days_reject,
            cost_of_sales_pct=cost_of_sales_pct,
            cost_of_capital_annual=cost_of_capital_annual,
            avg_supplier_pay_days=avg_supplier_pay_days
        )

        st.subheader("Αποτελέσματα")
        st.metric("Καθαρή Παρούσα Αξία (NPV)", format_number_gr(result["NPV"]) + " €")
        st.metric("Μέγιστο Επιτρεπτό Ποσοστό Έκπτωσης", format_percentage_gr(result["Max Discount %"]))
        st.metric("Βέλτιστο Ποσοστό Έκπτωσης", format_percentage_gr(result["Optimal Discount %"]))

        st.caption(
            f"📊 Μεσοσταθμικά, το {format_percentage_gr(result['Weighted Customer Acceptance %'])} των πελατών πληρώνει με έκπτωση."
        )
