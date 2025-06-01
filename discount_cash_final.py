import streamlit as st

def show_discount_cash_app():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")
    st.write("🔍 Ανάλυση καθαρής παρούσας αξίας (NPV) από την πολιτική παροχής έκπτωσης για άμεση πληρωμή.")

    st.header("📥 Εισαγωγή Δεδομένων")

    current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", min_value=0.0, value=1000.0, step=100.0)
    extra_sales = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", min_value=0.0, value=250.0, step=50.0)
    cash_discount_rate = st.number_input("Ποσοστό Έκπτωσης για Πληρωμή Τοις Μετρητοίς (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1) / 100
    pct_customers_accept = st.number_input("Ποσοστό Πελατών που Αποδέχεται την Έκπτωση (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0) / 100
    days_accept = st.number_input("Ημέρες Πληρωμής για Πελάτες που Αποδέχονται (μέρες)", min_value=0, value=10, step=1)
    days_reject = st.number_input("Ημέρες Πληρωμής για Πελάτες που Δεν Αποδέχονται (μέρες)", min_value=0, value=120, step=1)
    cost_of_sales_pct = st.number_input("Κόστος Πωλήσεων (%)", min_value=0.0, max_value=100.0, value=80.0, step=1.0) / 100
    cost_of_capital_annual = st.number_input("Κόστος Κεφαλαίου (% ετησίως)", min_value=0.0, max_value=100.0, value=20.0, step=0.5) / 100
    avg_supplier_pay_days = st.number_input("Μέση Περίοδος Αποπληρωμής Προμηθευτών (μέρες)", min_value=0, value=0, step=1)

    if st.button("💡 Υπολογισμός"):
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

        st.subheader("📈 Αποτελέσματα")
        st.metric("NPV", f"{results['NPV']} €")
        st.metric("Κέρδος από Επιπλέον Πωλήσεις", f"{results['Gross Profit Extra Sales']} €")
        st.metric("Μέγιστη Επιτρεπτή Έκπτωση", f"{results['Max Discount %']} %")
        st.metric("Βέλτιστη Έκπτωση", f"{results['Optimal Discount %']} %")
        st.metric("Πελάτες που Αποδέχονται Έκπτωση (Παλαιοί + Νέοι)", f"{results['Weighted Acceptance Rate']} %")
