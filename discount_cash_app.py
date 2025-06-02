import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct
from utils import parse_gr_number, format_number_gr, format_percentage_gr


def show_discount_cash_app():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    with st.form("discount_cash_form"):
        st.subheader("Εισαγωγή Δεδομένων")

        col1, col2 = st.columns(2)

        with col1:
            current_sales = parse_gr_number(st.text_input("Τρέχουσες Ετήσιες Πωλήσεις (€)", "500.000"))
            additional_sales = parse_gr_number(st.text_input("Επιπλέον Πωλήσεις από την Έκπτωση (€)", "50.000"))
            cost_ratio = parse_gr_number(st.text_input("Μεσοσταθμικό Κόστος (% επί των πωλήσεων)", "60")) / 100
            supplier_payment_days = int(st.number_input("Μέρες Πίστωσης από Προμηθευτές", value=30))
            current_collection_days = int(st.number_input("Τρέχοντες Μ.Ο. Ημέρες Είσπραξης", value=60))

        with col2:
            discount_rate = parse_gr_number(st.text_input("Ποσοστό Έκπτωσης (%)", "3")) / 100
            discount_acceptance_ratio = parse_gr_number(
                st.text_input("Ποσοστό Πελατών που Δέχονται την Έκπτωση (%)", "80")
            ) / 100
            annual_cost_of_capital = parse_gr_number(
                st.text_input("Ετήσιο Κόστος Κεφαλαίου (%)", "10")
            ) / 100
            days_full_payment = int(st.number_input("Μέρες Είσπραξης Χωρίς Έκπτωση", value=60))
            days_discount_payment = int(st.number_input("Μέρες Είσπραξης με Έκπτωση", value=10))

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_discount_cash_fixed_pct(
            discount_rate=discount_rate,
            current_sales=current_sales,
            additional_sales=additional_sales,
            days_full_payment=days_full_payment,
            days_discount_payment=days_discount_payment,
            cost_ratio=cost_ratio,
            annual_cost_of_capital=annual_cost_of_capital,
            supplier_payment_days=supplier_payment_days,
            current_collection_days=current_collection_days,
            discount_acceptance_ratio=discount_acceptance_ratio
        )

        st.subheader("Αποτελέσματα")

        st.metric("Καθαρή Παρούσα Αξία (NPV)", format_number_gr(results["npv"]) + " €")

        if results["break_even_discount"] is not None:
            st.metric(
                "Μέγιστο Αποδεκτό Ποσοστό Έκπτωσης",
                format_percentage_gr(results["break_even_discount"] * 100)
            )
        else:
            st.warning("Δεν ήταν δυνατός ο υπολογισμός του μέγιστου αποδεκτού ποσοστού έκπτωσης (NPV δεν μηδενίζεται).")
