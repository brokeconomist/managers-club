import streamlit as st
from loan_vs_leasing_logic import pv, limited_depreciation, tax_savings, total_cost
from utils import format_number_gr, parse_gr_number

def loan_vs_leasing_ui():
    st.header("📊 Σύγκριση: Τραπεζικός Δανεισμός vs Leasing")

    st.subheader("⚙️ Γενικές Παράμετροι")
    interest_rate_loan = st.number_input("Επιτόκιο Δανείου (%)", value=6.0) / 100
    interest_rate_working = st.number_input("Επιτόκιο Κεφαλαίου Κίνησης (%)", value=8.0) / 100
    years = st.number_input("Διάρκεια (έτη)", value=15, step=1)
    months = st.number_input("Μήνες ανά έτος", value=12, step=1)
    total_periods = int(years * months)
    dep_years = st.number_input("Χρόνος Απόσβεσης", value=30, step=1)
    tax_rate = st.number_input("Φορολογικός Συντελεστής (%)", value=35.0) / 100
    when = st.selectbox("Πληρωμή στην αρχή (1) ή στο τέλος (0);", options=[1, 0])

    st.subheader("🏦 Δανεισμός")
    loan_asset = st.number_input("Αξία Ακινήτου (Δάνειο)", value=250000)
    loan_rate = st.number_input("Ποσοστό Χρηματοδότησης Δανείου (%)", value=70.0) / 100
    loan_monthly = st.number_input("Μηνιαία Δόση Δανείου", value=1469.0)
    loan_extra_costs = st.number_input("Επιπλέον Έξοδα Δανείου", value=35000)
    working_capital_loan = st.number_input("Δάνειο Κεφαλαίου Κίνησης (Δάνειο)", value=110000.0)
    working_capital_monthly_loan = st.number_input("Μηνιαία Δόση Κεφαλαίου Κίνησης (Δάνειο)", value=1044.0)

    st.subheader("📄 Leasing")
    leasing_asset = st.number_input("Αξία Ακινήτου (Leasing)", value=250000)
    leasing_rate = 1.0  # 100%
    leasing_monthly = st.number_input("Μηνιαία Δόση Leasing", value=2099.0)
    leasing_extra_costs = st.number_input("Επιπλέον Έξοδα Leasing", value=30000)
    working_capital_leasing = st.number_input("Δάνειο Κεφαλαίου Κίνησης (Leasing)", value=30000.0)
    working_capital_monthly_leasing = st.number_input("Μηνιαία Δόση Κεφαλαίου Κίνησης (Leasing)", value=285.0)
    residual_value = st.number_input("Υπολειμματική Αξία Leasing", value=3530.0)

    st.markdown("---")

    # Υπολογισμοί Δανείου
    loan_financed = loan_asset * loan_rate
    pv_loan_installments = pv(interest_rate_loan / months, total_periods, loan_monthly, 0, when)
    pv_working_loan = pv(interest_rate_working / months, total_periods, working_capital_monthly_loan, 0, when)
    loan_depr = limited_depreciation(loan_asset, loan_extra_costs, dep_years, years)
    loan_interest_total = loan_monthly * total_periods - loan_financed
    loan_tax = tax_savings(interest_rate_loan / months, total_periods, loan_interest_total, loan_depr, tax_rate)
    loan_total = total_cost(pv_loan_installments, pv_working_loan, loan_extra_costs, loan_tax)

    # Υπολογισμοί Leasing
    leasing_financed = leasing_asset * leasing_rate
    pv_leasing_installments = pv(interest_rate_loan / months, total_periods, leasing_monthly, -residual_value, when)
    pv_working_leasing = pv(interest_rate_working / months, total_periods, working_capital_monthly_leasing, 0, when)
    leasing_depr = limited_depreciation(leasing_asset, leasing_extra_costs, dep_years, years)
    leasing_interest_total = leasing_monthly * total_periods - leasing_financed
    leasing_tax = tax_savings(interest_rate_loan / months, total_periods, leasing_interest_total, leasing_depr, tax_rate)
    leasing_total = total_cost(pv_leasing_installments, pv_working_leasing, leasing_extra_costs, leasing_tax)

    # Εμφάνιση
    st.subheader("💰 Τελικά Αποτελέσματα")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Τελική Επιβάρυνση Δανείου", format_number_gr(loan_total))
    with col2:
        st.metric("Τελική Επιβάρυνση Leasing", format_number_gr(leasing_total))

    diff = loan_total - leasing_total
    if abs(diff) > 1:
        st.success(f"👉 **Πλεονέκτημα έχει το {'Leasing' if diff > 0 else 'Δάνειο'}** κατά περίπου {format_number_gr(abs(diff))} ευρώ.")
