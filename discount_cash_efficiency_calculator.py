import streamlit as st
from discount_cash_efficiency_logic import calculate_discount_cash_efficiency
from utils import format_number_gr, parse_gr_number, format_percentage_gr

def render_discount_cash_efficiency():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")
    st.write("Υπολογισμός καθαρής παρούσας αξίας (NPV) από παροχή έκπτωσης μετρητοίς με παράλληλη αύξηση πωλήσεων.")

    col1, col2 = st.columns(2)

    with col1:
        current_sales = parse_gr_number(st.text_input("Τρέχουσες πωλήσεις", "1.000"))
        extra_sales = parse_gr_number(st.text_input("Επιπλέον πωλήσεις λόγω έκπτωσης", "250"))
        cash_discount_rate = parse_gr_number(st.text_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", "2")) / 100
        pct_customers_accept = parse_gr_number(st.text_input("% πελατών που αποδέχεται την έκπτωση", "50")) / 100
        cost_of_sales_pct = parse_gr_number(st.text_input("Κόστος πωλήσεων σε %", "80")) / 100

    with col2:
        days_cash = parse_gr_number(st.text_input("Μέρες για πληρωμή τοις μετρητοίς", "10"))
        days_reject = parse_gr_number(st.text_input("Μέρες πληρωμής για όσους απορρίπτουν την έκπτωση", "120"))
        cost_of_capital_annual = parse_gr_number(st.text_input("Ετήσιο κόστος κεφαλαίου (WACC %)", "20")) / 100
        avg_supplier_pay_days = parse_gr_number(st.text_input("Μέση περίοδος αποπληρωμής προμηθευτών", "30"))
        current_collection_days = parse_gr_number(st.text_input("Τρέχουσα μέση περίοδος είσπραξης", "90"))

    if st.button("Υπολογισμός"):
        results = calculate_discount_cash_efficiency(
            current_sales,
            extra_sales,
            cash_discount_rate,
            pct_customers_accept,
            days_cash,
            days_reject,
            cost_of_sales_pct,
            cost_of_capital_annual,
            avg_supplier_pay_days,
            current_collection_days
        )

        st.success("Αποτελέσματα Υπολογισμού:")
        st.write(f"**Καθαρή Παρούσα Αξία (NPV):** € {format_number_gr(results['NPV'])}")
        st.write(f"**Μέγιστη έκπτωση (Break-even %):** {format_percentage_gr(results['BreakEvenDiscount'])}")
        st.write(f"**Βέλτιστη έκπτωση (1/4 του break-even):** {format_percentage_gr(results['OptimalDiscount'])}")
