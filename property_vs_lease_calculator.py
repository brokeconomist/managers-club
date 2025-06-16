import streamlit as st
from property_vs_lease_logic import calculate_property_vs_lease
from utils import format_number_gr, parse_gr_number, format_percentage_gr

def show_property_vs_lease_calculator():
    st.header("Ανάλυση Απόκτησης Ακινήτου έναντι Μίσθωσης")

    st.markdown("### 📥 Είσοδοι")

    col1, col2 = st.columns(2)

    with col1:
        rent_per_month = parse_gr_number(st.text_input("Μηνιαίο μίσθωμα (€)", "1000"))
        duration_years = st.number_input("Διάρκεια (έτη)", value=15, min_value=1)
        interest_rate_annual = st.number_input("Ετήσιο επιτόκιο δανείου (%)", value=6.0, min_value=0.0)
        tax_rate = st.number_input("Φορολογικός συντελεστής (%)", value=22.0, min_value=0.0)

    with col2:
        property_price = parse_gr_number(st.text_input("Τιμή αγοράς ακινήτου (€)", "150000"))
        acquisition_costs = parse_gr_number(st.text_input("Λοιπά έξοδα απόκτησης (€)", "10000"))
        annual_maintenance = parse_gr_number(st.text_input("Ετήσιο κόστος συντήρησης (€)", "1000"))

    results = calculate_property_vs_lease(
        rent_per_month, duration_years, interest_rate_annual,
        property_price, acquisition_costs, annual_maintenance, tax_rate
    )

    st.markdown("### 📊 Αποτελέσματα")

    st.subheader("💼 Εναλλακτική 1: Μίσθωση")
    st.write(f"Συνολικό καταβληθέν ποσό: **{format_number_gr(results['total_rent'])} €**")
    st.write(f"Παρούσα αξία μισθώσεων: **{format_number_gr(results['rent_npv'])} €**")

    st.subheader("🏠 Εναλλακτική 2: Απόκτηση")
    st.write(f"Μηνιαία δόση δανείου: **{format_number_gr(results['monthly_payment'])} €**")
    st.write(f"Συνολικές πληρωμές δανείου: **{format_number_gr(results['total_loan_payments'])} €**")
    st.write(f"Συνολικοί τόκοι: **{format_number_gr(results['total_interest'])} €**")
    st.write(f"Φορολογικό όφελος: **{format_number_gr(results['tax_savings'])} €**")
    st.write(f"Καθαρό κόστος απόκτησης (με φόρους): **{format_number_gr(results['net_acquisition_cost'])} €**")

    st.subheader("⚖️ Σύγκριση")
    st.write(f"Διαφορά κόστους (Απόκτηση - Μίσθωση): **{format_number_gr(results['cost_difference'])} €**")

    if results['cost_difference'] < 0:
        st.success("Η αγορά είναι φθηνότερη σε παρούσα αξία.")
    elif results['cost_difference'] > 0:
        st.error("Η μίσθωση είναι οικονομικότερη σε παρούσα αξία.")
    else:
        st.info("Οι δύο επιλογές είναι ισοδύναμες οικονομικά.")
