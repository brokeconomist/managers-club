import streamlit as st
from utils import format_number_gr
from loan_vs_leasing_logic import calculate_loan_or_leasing

def loan_vs_leasing_ui():
    st.header("📊 Σύγκριση Τραπεζικού Δανεισμού με Leasing")

    st.markdown("**Γενικές Παράμετροι**")
    col1, col2 = st.columns(2)
    with col1:
        interest_loan = st.number_input("Επιτόκιο Δανείου (%)", value=6.0) / 100
        interest_wc = st.number_input("Επιτόκιο Κεφαλαίου Κίνησης (%)", value=8.0) / 100
        years = st.number_input("Διάρκεια Χρηματοδότησης (έτη)", value=15, step=1)
        dep_years = st.number_input("Συνολικός Χρόνος Απόσβεσης (έτη)", value=30, step=1)
        tax_rate = st.number_input("Φορολογικός Συντελεστής (%)", value=35.0) / 100
        when_val = st.selectbox("Πληρωμή στην αρχή του μήνα;", ["Όχι", "Ναι"]) == "Ναι"

    with col2:
        fv_leasing = st.number_input("Υπολειμματική αξία Leasing", value=3530.0)
        months = years * 12
        rate_loan_monthly = interest_loan / 12
        rate_wc_monthly = interest_wc / 12
        when_val = int(when_val)

    def input_option(label, defaults):
        st.markdown(f"### {label}")
        return {
            "value_asset": st.number_input(f"{label} - Εμπορική αξία ακινήτου", value=defaults["value_asset"]),
            "financing_percent": st.number_input(f"{label} - Ποσοστό Χρηματοδότησης (%)", value=defaults["financing_percent"]) / 100,
            "monthly_installment": st.number_input(f"{label} - Μηνιαία Δόση", value=defaults["monthly_installment"]),
            "extra_costs": st.number_input(f"{label} - Επιπλέον Έξοδα", value=defaults["extra_costs"]),
            "working_capital": st.number_input(f"{label} - Δάνειο Κεφαλαίου Κίνησης", value=defaults["working_capital"]),
            "working_cap_installment": st.number_input(f"{label} - Δόση Κεφαλαίου Κίνησης", value=defaults["working_cap_installment"]),
        }

    loan_defaults = {
        "value_asset": 250_000,
        "financing_percent": 70.0,
        "monthly_installment": 1469,
        "extra_costs": 35_000,
        "working_capital": 110_000,
        "working_cap_installment": 1044,
    }

    leasing_defaults = {
        "value_asset": 250_000,
        "financing_percent": 100.0,
        "monthly_installment": 2099,
        "extra_costs": 30_000,
        "working_capital": 30_000,
        "working_cap_installment": 285,
    }

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        loan_data = input_option("🏦 Τραπεζικός Δανεισμός", loan_defaults)
    with col2:
        leasing_data = input_option("📌 Leasing", leasing_defaults)

    st.markdown("---")
    st.subheader("📉 Αποτελέσματα")

    res_loan = calculate_loan_or_leasing(
        option=loan_data,
        months=months,
        rate_main=rate_loan_monthly,
        rate_wc=rate_wc_monthly,
        when_val=when_val,
        dep_years=dep_years,
        years=years,
        tax_rate=tax_rate,
        fv=0
    )

    res_leasing = calculate_loan_or_leasing(
        option=leasing_data,
        months=months,
        rate_main=rate_loan_monthly,
        rate_wc=rate_wc_monthly,
        when_val=when_val,
        dep_years=dep_years,
        years=years,
        tax_rate=tax_rate,
        fv=fv_leasing
    )

    def show_results(label, result):
        st.markdown(f"#### {label}")
        st.write(f"• Παρούσα αξία δόσεων: **{format_number_gr(result['pv_installments'])} €**")
        st.write(f"• Παρούσα αξία κεφαλαίου κίνησης: **{format_number_gr(result['pv_working_cap'])} €**")
        st.write(f"• Αποσβέσεις: **{format_number_gr(result['depreciation'])} €**")
        st.write(f"• Συνολικοί τόκοι: **{format_number_gr(result['interest_total'])} €**")
        st.write(f"• Φορολογικό όφελος: **{format_number_gr(result['tax_savings'])} €**")
        st.success(f"✅ Τελική επιβάρυνση: **{format_number_gr(result['total_cost'])} €**")

    col1, col2 = st.columns(2)
    with col1:
        show_results("🏦 Τραπεζικός Δανεισμός", res_loan)
    with col2:
        show_results("📌 Leasing", res_leasing)

    st.markdown("---")
    diff = res_loan["total_cost"] - res_leasing["total_cost"]
    better_option = "📌 Leasing" if diff > 0 else "🏦 Τραπεζικός Δανεισμός"
    st.info(f"Διαφορά υπέρ **{better_option}**: **{format_number_gr(abs(diff))} €**")
