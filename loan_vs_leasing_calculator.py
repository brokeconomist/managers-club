import streamlit as st
from loan_vs_leasing_logic import pv, limited_depreciation, tax_savings, total_cost
from utils import format_number_gr

def loan_vs_leasing_ui():
    st.header("📊 Σύγκριση Δανείου vs Leasing με Παρούσα Αξία")

    st.subheader("🔢 Εισαγωγή Δεδομένων")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💰 Δάνειο")
        loan_rate = st.number_input("Επιτόκιο Δανείου (%)", value=6.0) / 100
        duration_years = st.number_input("Διάρκεια (έτη)", value=15)
        loan_monthly = st.number_input("Μηνιαία Δόση Δανείου (€)", value=2099.0)
        working_capital = st.number_input("Μηνιαία Δόση Κεφαλαίου Κίνησης (€)", value=300.0)
        loan_extra = st.number_input("Εφάπαξ Έξοδα (€)", value=5000.0)
        loan_interest = st.number_input("Συνολικοί Τόκοι (€)", value=40000.0)
        loan_asset_value = st.number_input("Εμπορική Αξία Παγίου (€)", value=250000.0)
        loan_dep_years = st.number_input("Έτη Απόσβεσης Παγίου", value=25)
        loan_additional_costs = st.number_input("Επιπλέον Κόστη Απόκτησης (€)", value=35000.0)

    with col2:
        st.markdown("### 🚗 Leasing")
        leasing_rate = st.number_input("Επιτόκιο Leasing (%)", value=6.0) / 100
        leasing_monthly = st.number_input("Μηνιαία Δόση Leasing (€)", value=2099.0)
        residual_value = st.number_input("Υπολειμματική Αξία (€)", value=50000.0)
        leasing_extra = st.number_input("Εφάπαξ Έξοδα Leasing (€)", value=2000.0)
        leasing_working_capital = st.number_input("Δόση Κεφ. Κίνησης Leasing (€)", value=0.0)
        leasing_interest = st.number_input("Συνολικοί Τόκοι Leasing (€)", value=30000.0)
        leasing_asset_value = st.number_input("Αξία Leasing Asset (€)", value=285000.0)

    tax_rate = st.number_input("Φορολογικός Συντελεστής (%)", value=35.0) / 100

    st.subheader("📉 Υπολογισμός Παρούσας Αξίας")

    # Δάνειο
    pv_loan = pv(loan_rate / 12, duration_years * 12, -loan_monthly, 0, 1)
    pv_wc_loan = pv(loan_rate / 12, duration_years * 12, -working_capital, 0, 1)
    depreciation_loan = limited_depreciation(loan_asset_value, loan_additional_costs, loan_dep_years, duration_years)
    tax_benefit_loan = tax_savings(loan_rate, duration_years, loan_interest, depreciation_loan, tax_rate)
    total_loan = total_cost(pv_loan, pv_wc_loan, loan_extra, tax_benefit_loan)

    # Leasing
    pv_leasing = pv(leasing_rate / 12, duration_years * 12, -leasing_monthly, residual_value, 1)
    pv_wc_leasing = pv(leasing_rate / 12, duration_years * 12, -leasing_working_capital, 0, 1)
    # Leasing depreciation is the full amount
    depreciation_leasing = leasing_asset_value
    tax_benefit_leasing = tax_savings(leasing_rate, duration_years, leasing_interest, depreciation_leasing, tax_rate)
    total_leasing = total_cost(pv_leasing, pv_wc_leasing, leasing_extra, tax_benefit_leasing)

    st.subheader("📋 Σύγκριση Αποτελεσμάτων")

    col1, col2 = st.columns(2)
    col1.metric("📉 Τελική Επιβάρυνση Δανείου (PV)", f"{format_number_gr(total_loan)} €")
    col2.metric("📉 Τελική Επιβάρυνση Leasing (PV)", f"{format_number_gr(total_leasing)} €")

    st.write("---")
    st.markdown("✅ Η μικρότερη παρούσα αξία δείχνει την οικονομικά συμφερότερη επιλογή.")
