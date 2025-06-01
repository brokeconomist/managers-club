import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct

st.set_page_config(page_title="Αποδοτικότητα Έκπτωσης", page_icon="💶")
st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

st.markdown("""
Ανάλυση της καθαρής παρούσας αξίας (NPV) μιας πολιτικής έκπτωσης για πληρωμές τοις μετρητοίς. 
Το 60% των πελατών θεωρείται ότι αποδέχεται την έκπτωση κατά μέσο όρο (παλιοί + νέοι).
""")

with st.form("discount_form"):
    col1, col2 = st.columns(2)
    with col1:
        current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", value=1000.0, step=100.0)
        extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", value=250.0, step=50.0)
        cash_discount_rate = st.number_input("Έκπτωση (%)", value=2.0, step=0.5) / 100
        days_accept = st.number_input("Μέρες είσπραξης (με έκπτωση)", value=10)
        days_reject = st.number_input("Μέρες είσπραξης (χωρίς έκπτωση)", value=120)

    with col2:
        cost_of_sales_pct = st.number_input("Κόστος Πωλήσεων (%)", value=80.0, step=1.0) / 100
        cost_of_capital_annual = st.number_input("Κόστος Κεφαλαίου (%)", value=20.0, step=1.0) / 100
        avg_supplier_pay_days = st.number_input("Μέρες αποπληρωμής προμηθευτών", value=0.0)

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
    st.metric("NPV (Καθαρή Παρούσα Αξία)", f"€ {results['NPV']}")
    st.metric("Μέγιστη Έκπτωση που μπορεί να δοθεί", f"{results['Max Discount %']}%")
    st.metric("Βέλτιστη Έκπτωση (25% της μέγιστης)", f"{results['Optimal Discount %']}%")
    st.metric("% Πελατών με Έκπτωση (μέσος όρος)", f"{results['% Πελατών με Έκπτωση']}%")
