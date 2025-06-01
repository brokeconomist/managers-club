import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct

def show_discount_cash_app():
    st.title("Υπολογισμός Αποδοτικότητας Έκπτωσης Τοις Μετρητοίς")

    st.header("Είσοδος δεδομένων")

    current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", value=1000.0)
    extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", value=250.0)
    cash_discount_rate = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0) / 100
    pct_customers_accept = st.number_input("% των πελατών που αποδέχεται την έκπτωση (%)", value=50.0) / 100
    days_accept = st.number_input("Μέρες για πληρωμή τοις μετρητοίς (π.χ. 10)", value=10)
    days_reject = st.number_input("Μέρες πληρωμής πελατών που δεν αποδέχονται (%)", value=120)
    cost_of_sales_pct = st.number_input("Κόστος πωλήσεων σε %", value=80.0) / 100
    cost_of_capital_annual = st.number_input("Κόστος κεφαλαίου ετησίως (%)", value=20.0) / 100
    avg_supplier_pay_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών (ημέρες)", value=0.0)
    current_collection_days = st.number_input("Τρέχουσα μέση περίοδος είσπραξης (ημέρες)", value=90.0)

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

        st.success("Αποτελέσματα Υπολογισμού:")
        st.metric("NPV (€)", results["NPV"])
        st.metric("Μέγιστο επιτρεπτό ποσοστό έκπτωσης (%)", results["Max Discount %"])
        st.metric("Βέλτιστο προτεινόμενο ποσοστό έκπτωσης (%)", results["Optimal Discount %"])
        st.metric("Μικτό κέρδος από επιπλέον πωλήσεις (€)", results["Gross Profit Extra Sales"])
        st.metric("Σταθμισμένο ποσοστό αποδοχής νέας πολιτικής (%)", results["Weighted Acceptance Rate"])

if __name__ == "__main__":
    show_discount_cash_app()
