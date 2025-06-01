import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct

def show_discount_cash_app():
    st.header("📉 Υπολογισμός Έκπτωσης για Πληρωμή Τοις Μετρητοίς")

    current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", value=1000.0)
    extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", value=250.0)
    cash_discount_rate = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0) / 100
    pct_customers_accept = st.number_input("% πελατών που αποδέχεται την έκπτωση", value=50.0) / 100
    days_cash = st.number_input("Μέρες πληρωμής με έκπτωση", value=10)
    days_reject = st.number_input("Μέρες πληρωμής χωρίς έκπτωση", value=120)
    cost_of_sales_pct = st.number_input("Κόστος πωλήσεων (%)", value=80.0) / 100
    cost_of_capital_annual = st.number_input("Κόστος κεφαλαίου (%)", value=20.0) / 100
    avg_supplier_pay_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών (μέρες)", value=0)
    current_collection_days = st.number_input("Μέση περίοδος είσπραξης απαιτήσεων (μέρες)", value=60)

    if st.button("🔍 Υπολογισμός"):
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

        st.success("✅ Υπολογισμός Ολοκληρώθηκε")
        st.write(f"**NPV (€):** {results['NPV']}")
        st.write(f"**Μέγιστη Δυνητική Έκπτωση (%):** {results['Max Discount %']}%")
        st.write(f"**Βέλτιστη Έκπτωση (%):** {results['Optimal Discount %']}%")
        st.write(f"**Μικτό Κέρδος από Extra Πωλήσεις (€):** {results['Gross Profit Extra Sales']}")
        st.write(f"**Σταθμισμένο Ποσοστό Αποδοχής (%):** {results['Weighted Acceptance Rate']}%")
