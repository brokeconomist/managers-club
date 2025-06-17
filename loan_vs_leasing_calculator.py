import streamlit as st
from utils import format_number_gr
from loan_vs_leasing_logic import calculate_loan_vs_leasing

def loan_vs_leasing_ui():
    st.header("🔄 Σύγκριση Τραπεζικού Δανεισμού vs Leasing")

    with st.form("loan_leasing_form"):
        st.subheader("📌 Βασικές Παράμετροι")
        col1, col2, col3 = st.columns(3)
        years = col1.number_input("Διάρκεια (χρόνια)", min_value=1, value=15)
        months = col2.number_input("Μήνες ανά έτος", min_value=1, value=12)
        dep_years = col3.number_input("Συνολικός χρόνος απόσβεσης", min_value=1, value=30)
        when = st.radio("Πληρωμή στην αρχή;", ["Ναι", "Όχι"], index=0)
        when = 1 if when == "Ναι" else 0
        tax_rate = st.number_input("Φορολογικός συντελεστής (%)", min_value=0.0, value=35.0)

        st.divider()
        st.subheader("🏦 Τραπεζικός Δανεισμός")
        loan_asset_value = st.text_input("Εμπορική αξία ακινήτου (Δάνειο)", "250.000")
        loan_funding = st.number_input("Ποσοστό Χρηματοδότησης (%)", min_value=0.0, value=70.0)
        loan_monthly_payment = st.text_input("Μηνιαία δόση", "1.469")
        loan_extra_costs = st.text_input("Επιπλέον έξοδα", "35.000")
        loan_working_cap_loan = st.text_input("Δάνειο για κεφάλαιο κίνησης", "110.000")
        loan_working_cap_monthly = st.text_input("Μηνιαία δόση για κεφάλαιο κίνησης", "1.044")
        loan_rate = st.number_input("Επιτόκιο Δανείου (%)", min_value=0.0, value=6.0)

        st.divider()
        st.subheader("📄 Leasing")
        leasing_asset_value = st.text_input("Εμπορική αξία ακινήτου (Leasing)", "250.000")
        leasing_funding = st.number_input("Ποσοστό Χρηματοδότησης Leasing (%)", min_value=0.0, value=100.0)
        leasing_monthly_payment = st.text_input("Μηνιαία δόση Leasing", "2.099")
        leasing_extra_costs = st.text_input("Επιπλέον έξοδα Leasing", "30.000")
        leasing_residual_value = st.text_input("Υπολειμματική αξία Leasing", "3.530")
        leasing_working_cap_loan = st.text_input("Δάνειο για κεφάλαιο κίνησης", "30.000")
        leasing_working_cap_monthly = st.text_input("Μηνιαία δόση για κεφάλαιο κίνησης", "285")
        leasing_rate = st.number_input("Επιτόκιο Leasing (%)", min_value=0.0, value=6.0)

        working_cap_rate = st.number_input("Επιτόκιο κεφαλαίου κίνησης (%)", min_value=0.0, value=8.0)

        submitted = st.form_submit_button("🔍 Υπολογισμός")

    if submitted:
        inputs = {
            'years': years,
            'months': months,
            'dep_years': dep_years,
            'when': when,
            'tax_rate': tax_rate,
            'loan_asset_value': loan_asset_value,
            'loan_funding': loan_funding,
            'loan_monthly_payment': loan_monthly_payment,
            'loan_extra_costs': loan_extra_costs,
            'loan_working_cap_loan': loan_working_cap_loan,
            'loan_working_cap_monthly': loan_working_cap_monthly,
            'loan_rate': loan_rate,
            'leasing_asset_value': leasing_asset_value,
            'leasing_funding': leasing_funding,
            'leasing_monthly_payment': leasing_monthly_payment,
            'leasing_extra_costs': leasing_extra_costs,
            'leasing_residual_value': leasing_residual_value,
            'leasing_working_cap_loan': leasing_working_cap_loan,
            'leasing_working_cap_monthly': leasing_working_cap_monthly,
            'leasing_rate': leasing_rate,
            'working_cap_rate': working_cap_rate
        }

        result = calculate_loan_vs_leasing(inputs)

        st.subheader("📊 Αποτελέσματα Σύγκρισης")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Τραπεζικός Δανεισμός")
            st.metric("Παρούσα αξία δόσεων", format_number_gr(result['loan']['pv_installments']))
            st.metric("Παρούσα αξία κεφαλαίου κίνησης", format_number_gr(result['loan']['pv_working_cap']))
            st.metric("Επιπλέον έξοδα", format_number_gr(result['loan']['extra_costs']))
            st.metric("Φορολογικό όφελος", format_number_gr(result['loan']['tax_benefit']))
            st.metric("💰 Τελική επιβάρυνση", format_number_gr(result['loan']['final_cost']))
        with col2:
            st.markdown("### Leasing")
            st.metric("Παρούσα αξία δόσεων", format_number_gr(result['leasing']['pv_installments']))
            st.metric("Παρούσα αξία κεφαλαίου κίνησης", format_number_gr(result['leasing']['pv_working_cap']))
            st.metric("Επιπλέον έξοδα", format_number_gr(result['leasing']['extra_costs']))
            st.metric("Φορολογικό όφελος", for
