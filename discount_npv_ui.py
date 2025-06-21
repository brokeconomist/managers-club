# discount_npv_ui.py
import streamlit as st
from discount_npv_logic import calculate_discount_npv
from utils import format_number_gr, format_percentage_gr

def show_discount_npv_ui():
    st.title("Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς - NPV")

    with st.form("discount_npv_form"):
        col1, col2 = st.columns(2)

        with col1:
            current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=1000.0, step=100.0)
            extra_sales = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", value=250.0, step=50.0)
            discount_trial = st.number_input("Προτεινόμενη Έκπτωση (%)", value=2.0, step=0.1) / 100
            prc_clients_take_disc = st.number_input("% Πελατών που Αποδέχονται την Έκπτωση", value=40.0, step=1.0) / 100
            days_clients_take_discount = st.number_input("Ημέρες Πληρωμής για Πελάτες με Έκπτωση", value=60, step=1)

        with col2:
            days_clients_no_discount = st.number_input("Ημέρες Πληρωμής για Πελάτες χωρίς Έκπτωση", value=120, step=1)
            new_days_cash_payment = st.number_input("Νέες Ημέρες Πληρωμής για Έκπτωση Τοις Μετρητοίς", value=10, step=1)
            cogs = st.number_input("Κόστος Πωληθέντων (€)", value=800.0, step=100.0)
            wacc = st.number_input("Κόστος Κεφαλαίου (WACC %)", value=20.0, step=0.1) / 100
            avg_days_pay_suppliers = st.number_input("Μέσες Ημέρες Πληρωμής Προμηθευτών", value=30, step=1)

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_discount_npv(
            current_sales,
            extra_sales,
            discount_trial,
            prc_clients_take_disc,
            days_clients_take_discount,
            days_clients_no_discount,
            new_days_cash_payment,
            cogs,
            wacc,
            avg_days_pay_suppliers
        )

        st.subheader("Αποτελέσματα")
        st.write(f"Μέση Περίοδος Είσπραξης (Τρέχουσα): {results['avg_current_collection_days']} ημέρες")
        st.write(f"Τρέχουσες Απαιτήσεις: {format_number_gr(results['current_receivables'])} €")
        st.write(f"Νέα Μέση Περίοδος Είσπραξης: {results['new_avg_collection_period']} ημέρες")
        st.write(f"Νέες Απαιτήσεις: {format_number_gr(results['new_receivables'])} €")
        st.write(f"Αποδέσμευση Κεφαλαίου: {format_number_gr(results['free_capital'])} €")
        st.write(f"Κέρδος από Επιπλέον Πωλήσεις: {format_number_gr(results['profit_from_extra_sales'])} €")
        st.write(f"Κέρδος από Αποδέσμευση Κεφαλαίου: {format_number_gr(results['profit_from_free_capital'])} €")
        st.write(f"Κόστος Έκπτωσης: {format_number_gr(results['discount_cost'])} €")
        st.markdown("---")
        st.write(f"💰 **Καθαρή Παρούσα Αξία (NPV): {format_number_gr(results['npv'])} €**")
        st.write(f"📉 **Μέγιστη Έκπτωση (Break-Even NPV): {format_percentage_gr(results['max_discount'])}**")
        st.write(f"📈 **Βέλτιστη Έκπτωση (Optimum): {format_percentage_gr(results['optimum_discount'])}**")
