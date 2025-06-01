
import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct
from utils import parse_gr_number, format_number_gr, format_percentage_gr

def show_discount_cash_app():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς (με σταθερό 60%)")

    with st.form("discount_cash_form"):
        current_sales = parse_gr_number(st.text_input("Τρέχουσες πωλήσεις (€)", "1.000"))
        extra_sales = parse_gr_number(st.text_input("Επιπλέον πωλήσεις από την έκπτωση (€)", "250"))
        cash_discount_rate = st.slider("Έκπτωση για πληρωμή τοις μετρητοίς (%)", 0.0, 10.0, 2.0) / 100

        days_accept = st.number_input("Ημέρες πληρωμής μετρητοίς (με έκπτωση)", value=10)
        days_reject = st.number_input("Ημέρες πληρωμής χωρίς έκπτωση", value=120)
        cost_of_sales_pct = st.slider("Κόστος πωληθέντων (%)", 0.0, 100.0, 80.0) / 100
        cost_of_capital_annual = st.slider("Ετήσιο κόστος κεφαλαίου (%)", 0.0, 50.0, 20.0) / 100
        avg_supplier_pay_days = st.number_input("Μέρες αποπληρωμής προμηθευτών", value=0)

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_discount_cash_fixed_pct(
            current_sales=current_sales,
            extra_sales=extra_sales,
            cash_discount_rate=cash_discount_rate,
            days_accept=days_accept,
            days_reject=days_reject,
            cost_of_sales_pct=cost_of_sales_pct,
            cost_of_capital_annual=cost_of_capital_annual,
            avg_supplier_pay_days=avg_supplier_pay_days
        )

        st.subheader("📊 Αποτελέσματα")
        st.metric("NPV (€)", format_number_gr(results["NPV"]))
        st.metric("Μέγιστη αποδεκτή έκπτωση (%)", format_percentage_gr(results["Max Discount %"]))
        st.metric("Βέλτιστη προτεινόμενη έκπτωση (%)", format_percentage_gr(results["Optimal Discount %"]))

