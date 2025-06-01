# discount_cash_app.py

import streamlit as st

def show_discount_cash_app():
    st.title("Υπολογισμός Αποδοτικότητας Έκπτωσης Τοις Μετρητοίς")

    st.header("📊 Είσοδος Δεδομένων")

    current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", min_value=0.0, value=1000.0)
    extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", min_value=0.0, value=250.0)
    cash_discount_rate = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", min_value=0.0, max_value=100.0, value=2.0) / 100
    pct_customers_accept = st.number_input("% των πελατών που αποδέχεται την έκπτωση", min_value=0.0, max_value=100.0, value=50.0) / 100
    days_cash = st.number_input("Μέρες για πληρωμή με έκπτωση", min_value=0, value=10)
    days_reject = st.number_input("Μέρες για πληρωμή χωρίς έκπτωση", min_value=0, value=120)
    cost_of_sales_pct = st.number_input("Κόστος πωλήσεων σε %", min_value=0.0, max_value=100.0, value=80.0) / 100
    cost_of_capital_annual = st.number_input("Κόστος κεφαλαίου ετησίως (%)", min_value=0.0, max_value=100.0, value=20.0) / 100
    avg_supplier_pay_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών (ημέρες)", min_value=0, value=0)
    current_collection_days = st.number_input("Τρέχουσα μέση περίοδος είσπραξης (ημέρες)", min_value=0, value=90)

    if st.button("Υπολογισμός NPV"):
        results = calculate_discount_cash_fixed_pct(
            current_sales=current_sales,
            extra_sales=extra_sales,
            cash_discount_rate=cash_discount_rate,
            pct_customers_accept=pct_customers_accept,
            days_cash=days_cash,
            days_reject=days_reject,
            cost_of_sales_pct=cost_of_sales_pct,
            cost_of_capital_annual=cost_of_capital_annual,
            avg_supplier_pay_days=avg_supplier_pay_days,
            current_collection_days=current_collection_days
        )

        st.success("Αποτελέσματα Υπολογισμού")
        st.metric("Καθαρή Παρούσα Αξία (NPV)", f"{results['NPV']} €")
        st.metric("Μέγιστη Δυνατή Έκπτωση", f"{results['Max Discount %']} %")
        st.metric("Βέλτιστη Έκπτωση", f"{results['Optimal Discount %']} %")
        st.metric("Μικτό Κέρδος από Extra Πωλήσεις", f"{results['Gross Profit Extra Sales']} €")
        st.metric("Σταθμισμένο Ποσοστό Αποδοχής Έκπτωσης", f"{results['Weighted Acceptance Rate']} %")
