import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct  # Βεβαιώσου ότι το path είναι σωστό

def show_discount_cash_app():
    st.title("Ανάλυση Έκπτωσης για Πληρωμή Τοις Μετρητοίς")

    current_sales = st.number_input("Τρέχουσες πωλήσεις", value=1000.0)
    extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης", value=250.0)
    cash_discount_rate = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0) / 100
    pct_customers_accept = st.number_input("% των πελατών που αποδέχεται την έκπτωση", value=50.0) / 100
    days_accept = st.number_input("Μέρες πληρωμής για πελάτες που αποδέχονται την έκπτωση", value=60)
    days_reject = st.number_input("Μέρες πληρωμής για πελάτες που δεν αποδέχονται την έκπτωση", value=120)
    cost_of_sales_pct = st.number_input("Κόστος πωλήσεων σε %", value=80.0) / 100
    cost_of_capital_annual = st.number_input("Κόστος κεφαλαίου σε %", value=20.0) / 100
    avg_supplier_pay_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών (ημέρες)", value=0)
    current_collection_days = st.number_input("Τρέχουσα μέση περίοδος είσπραξης (ημέρες)", value=90)

    if st.button("Υπολογισμός"):
        results = calculate_discount_cash_fixed_pct(
            current_sales=current_sales,
            extra_sales=extra_sales,
            cash_discount_rate=cash_discount_rate,
            pct_customers_accept=pct_customers_accept,
            days_accept=days_accept,
            days_reject=days_reject,
            cost_of_sales_pct=cost_of_sales_pct,
            cost_of_capital_annual=cost_of_capital_annual,
            avg_supplier_pay_days=avg_supplier_pay_days,
            current_collection_days=current_collection_days
        )

        st.subheader("Αποτελέσματα")
        st.metric("NPV", f"{results['NPV']} €")
        st.metric("Μέγιστη Επιτρεπόμενη Έκπτωση", f"{results['Max Discount %']} %")
        st.metric("Προτεινόμενη Έκπτωση", f"{results['Optimal Discount %']} %")
        st.metric("Μικτό Κέρδος από Επιπλέον Πωλήσεις", f"{results['Gross Profit Extra Sales']} €")
        st.metric("Σταθμισμένο Ποσοστό Πελατών που Αποδέχονται την Έκπτωση", f"{results['Weighted Acceptance Rate']} %")
