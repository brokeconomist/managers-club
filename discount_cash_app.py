import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct

def show_discount_cash_app():
    st.title("📉 Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")
    st.write("Αξιολογήστε την καθαρή παρούσα αξία (NPV) από την προσφορά έκπτωσης για πληρωμή τοις μετρητοίς.")

    with st.form("discount_cash_form"):
        current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", min_value=0.0, value=1000.0)
        extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", min_value=0.0, value=250.0)
        cash_discount_rate = st.number_input("Ποσοστό έκπτωσης (%)", min_value=0.0, max_value=100.0, value=2.0) / 100
        pct_customers_accept = st.number_input("% πελατών που αποδέχεται την έκπτωση", min_value=0.0, max_value=100.0, value=50.0) / 100
        days_accept = st.number_input("Μέρες αποπληρωμής για όσους αποδέχονται την έκπτωση", min_value=0, value=10)
        days_reject = st.number_input("Μέρες αποπληρωμής για όσους δεν αποδέχονται την έκπτωση", min_value=0, value=60)
        cost_of_sales_pct = st.number_input("Κόστος πωλήσεων σε %", min_value=0.0, max_value=100.0, value=80.0) / 100
        cost_of_capital_annual = st.number_input("Κόστος κεφαλαίου σε ετήσια βάση (%)", min_value=0.0, max_value=100.0, value=20.0) / 100
        avg_supplier_pay_days = st.number_input("Μέρες αποπληρωμής προμηθευτών (μέσος όρος)", min_value=0, value=0)

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_discount_cash_fixed_pct(
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

        st.subheader("📊 Αποτελέσματα")
        st.metric("NPV", f"€ {results['NPV']}")
        st.metric("Μέγιστη Έκπτωση που μπορεί να δοθεί", f"{results['Max Discount %']}%")
        st.metric("Βέλτιστη Έκπτωση (25% του οφέλους)", f"{results['Optimal Discount %']}%")
        st.metric("Κέρδος από Επιπλέον Πωλήσεις", f"€ {results['Gross Profit Extra Sales']}")
        st.metric("Σταθμισμένο Ποσοστό Πελατών που Παίρνουν Έκπτωση", f"{results['Weighted Acceptance Rate']}%")
