import streamlit as st
from utils import format_number_gr
from math import ceil

from financial_tools import pv, limited_depreciation, tax_savings, total_cost  # Αν τα έχεις αλλού, άλλαξε import

st.header("📊 Σύγκριση Τραπεζικού Δανεισμού με Leasing")

st.markdown("**Οικονομικά στοιχεία**")
col1, col2 = st.columns(2)
with col1:
    interest_loan = st.number_input("Επιτόκιο Δανείου (%)", value=6.0) / 100
    interest_wc = st.number_input("Επιτόκιο Κεφαλαίου Κίνησης (%)", value=8.0) / 100
    years = st.number_input("Διάρκεια Χρηματοδότησης (έτη)", value=15, step=1)
    dep_years = st.number_input("Συνολικός χρόνος απόσβεσης (έτη)", value=30, step=1)
    tax_rate = st.number_input("Φορολογικός Συντελεστής (%)", value=35.0) / 100
    when = st.selectbox("Πληρωμή στην αρχή του μήνα;", options=["Όχι", "Ναι"]) == "Ναι"

with col2:
    months = years * 12
    fv_leasing = st.number_input("Υπολειμματική αξία Leasing", value=3530.0)
    rate_loan_monthly = interest_loan / 12
    rate_wc_monthly = interest_wc / 12

st.markdown("### Δεδομένα")

def input_option(label):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{label}**")
    with col2:
        return {
            "value_asset": st.number_input(f"{label} - Εμπορική αξία ακινήτου", value=250_000),
            "financing_percent": st.number_input(f"{label} - Ποσοστό Χρηματοδότησης (%)", value=100.0) / 100,
            "monthly_installment": st.number_input(f"{label} - Μηνιαία Δόση", value=2000),
            "extra_costs": st.number_input(f"{label} - Επιπλέον έξοδα", value=30_000),
            "working_capital": st.number_input(f"{label} - Δάνειο για Κεφάλαιο Κίνησης", value=30_000),
            "working_cap_installment": st.number_input(f"{label} - Μηνιαία δόση για κεφάλαιο κίνησης", value=285),
        }

leasing = input_option("Leasing")
loan = input_option("Τραπεζικός Δανεισμός")

def calculate(option, rate_main, rate_wc, fv=0):
    when_val = int(when)
    pv_inst = pv(rate_main, months, option["monthly_installment"], fv, when_val)
    pv_wc = pv(rate_wc, months, option["working_cap_installment"], 0, when_val)
    total_investment = option["value_asset"] + option["extra_costs"]
    depreciation = limited_depreciation(option["value_asset"], option["extra_costs"], dep_years, years)
    interest_total = option["monthly_installment"] * months - (option["financing_percent"] * option["value_asset"])
    tax = tax_savings(interest_loan, years, interest_total, depreciation, tax_rate)
    total = total_cost(pv_inst, pv_wc, option["extra_costs"], tax)

    return {
        "pv_installments": pv_inst,
        "pv_working_cap": pv_wc,
        "depreciation": depreciation,
        "interest_total": interest_total,
        "tax_savings": tax,
        "total_cost": total
    }

res_leasing = calculate(leasing, rate_loan_monthly, rate_wc_monthly, fv=fv_leasing)
res_loan = calculate(loan, rate_loan_monthly, rate_wc_monthly)

st.markdown("---")
st.subheader("📉 Αποτελέσματα Σύγκρισης")

def show_results(label, results):
    st.markdown(f"#### {label}")
    st.write(f"• Παρούσα αξία δόσεων: **{format_number_gr(results['pv_installments'])} €**")
    st.write(f"• Παρούσα αξία κεφαλαίου κίνησης: **{format_number_gr(results['pv_working_cap'])} €**")
    st.write(f"• Αποσβέσεις: **{format_number_gr(results['depreciation'])} €**")
    st.write(f"• Συνολικοί τόκοι: **{format_number_gr(results['interest_total'])} €**")
    st.write(f"• Φορολογικό όφελος: **{format_number_gr(results['tax_savings'])} €**")
    st.write(f"✅ **Τελική Επιβάρυνση: {format_number_gr(results['total_cost'])} €**")

col1, col2 = st.columns(2)
with col1:
    show_results("📌 Leasing", res_leasing)
with col2:
    show_results("🏦 Τραπεζικός Δανεισμός", res_loan)

diff = res_loan["total_cost"] - res_leasing["total_cost"]
st.markdown("---")
st.success(f"Διαφορά υπέρ **{ 'Leasing' if diff > 0 else 'Τραπεζικού Δανεισμού' }**: {format_number_gr(abs(diff))} €")
