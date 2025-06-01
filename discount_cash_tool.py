import streamlit as st
from discount_cash_chart import calculate_discount_cash
from utils import parse_gr_number, format_number_gr, format_percentage_gr

def show_discount_cash_calculator():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    with st.form("discount_cash_form"):
        col1, col2 = st.columns(2)
        with col1:
            current_sales = parse_gr_number(st.text_input("📦 Τρέχουσες πωλήσεις (€)", "1.000"))
            extra_sales = parse_gr_number(st.text_input("➕ Επιπλέον πωλήσεις λόγω πολιτικής (€)", "250"))
            cash_discount_rate = parse_gr_number(st.text_input("🏷️ Ποσοστό έκπτωσης (%)", "2")) / 100
            pct_customers_discount_total = parse_gr_number(
                st.text_input("👥 Ποσοστό όλων των πελατών που πληρώνουν μετρητοίς (%)", "60")
            ) / 100
            cost_of_sales_pct = parse_gr_number(st.text_input("⚙️ Κόστος πωληθέντων (%)", "80")) / 100

        with col2:
            days_accept = parse_gr_number(st.text_input("⏱️ Ημέρες είσπραξης για πληρωμή μετρητοίς", "10"))
            days_reject = parse_gr_number(st.text_input("⏳ Ημέρες είσπραξης χωρίς έκπτωση", "120"))
            cost_of_capital_annual = parse_gr_number(st.text_input("📉 Ετήσιο κόστος κεφαλαίου (%)", "20")) / 100
            avg_supplier_pay_days = parse_gr_number(st.text_input("🧾 Μέρες αποπληρωμής προμηθευτών", "0"))

        submitted = st.form_submit_button("📊 Υπολογισμός")

    if submitted:
        results = calculate_discount_cash(
            current_sales,
            extra_sales,
            cash_discount_rate,
            pct_customers_discount_total,
            days_accept,
            days_reject,
            cost_of_sales_pct,
            cost_of_capital_annual,
            avg_supplier_pay_days
        )

        st.subheader("📈 Αποτελέσματα")
        st.write("💶 **Καθαρή Παρούσα Αξία (NPV)**:", format_number_gr(results["NPV"]), "€")
        st.write("🔝 **Μέγιστο επιτρεπτό ποσοστό έκπτωσης**:", format_percentage_gr(results["Max Discount %"] / 100))
        st.write("✅ **Προτεινόμενο ποσοστό έκπτωσης (25% του max)**:", format_percentage_gr(results["Optimal Discount %"] / 100))

