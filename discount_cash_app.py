import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct

def show_discount_cash_app():
    st.title("Ανάλυση Έκπτωσης για Πληρωμή Τοις Μετρητοίς")

    current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=1000.0)
    extra_sales = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", value=250.0)
    cash_discount_rate = st.number_input("Ποσοστό Έκπτωσης (%)", value=2.0) / 100
    pct_customers_accept = st.number_input("Ποσοστό Πελατών που Αποδέχονται την Έκπτωση (%)", value=50.0) / 100
    days_cash = st.number_input("Μέρες Πληρωμής για Έκπτωση", value=10)
    days_reject = st.number_input("Μέρες Πληρωμής χωρίς Έκπτωση", value=120)
    cost_of_sales_pct = st.number_input("Κόστος Πωλήσεων (% επί των Πωλήσεων)", value=80.0) / 100
    cost_of_capital_annual = st.number_input("Κόστος Κεφαλαίου (% Ετησίως)", value=20.0) / 100
    avg_supplier_pay_days = st.number_input("Μέση Περίοδος Αποπληρωμής Προμηθευτών (ημέρες)", value=30)
    current_collection_days = st.number_input("Τρέχουσα Μέση Περίοδος Είσπραξης (ημέρες)", value=90)

    if st.button("Υπολογισμός"):
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

        st.write(f"**NPV (€):** {results['NPV']}")
        st.write(f"**Μέγιστη έκπτωση που μπορεί να δοθεί επί των πωλήσεων (NPV Break Even):** {results['Break-even Discount %']}%")
        st.write(f"**Βέλτιστη Έκπτωση (%):** {results['Optimal Discount %']}%")
