def show_property_vs_lease_calculator():
    st.header("Ανάλυση Απόκτησης Ακινήτου έναντι Μίσθωσης")

    st.markdown("### 📥 Είσοδοι")

    col1, col2 = st.columns(2)

    with col1:
        rent_per_month = st.number_input("Μηνιαίο μίσθωμα (€)", min_value=0.0, value=1000.0, step=10.0, format="%.2f")
        duration_years = st.number_input("Διάρκεια (έτη)", min_value=1, value=15, step=1)
        interest_rate_annual = st.number_input("Ετήσιο επιτόκιο δανείου (%)", min_value=0.0, value=6.0, step=0.1, format="%.2f")
        tax_rate = st.number_input("Φορολογικός συντελεστής (%)", min_value=0.0, value=22.0, step=0.1, format="%.2f")

    with col2:
        property_price = st.number_input("Τιμή αγοράς ακινήτου (€)", min_value=0.0, value=150000.0, step=1000.0, format="%.2f")
        acquisition_costs = st.number_input("Λοιπά έξοδα απόκτησης (€)", min_value=0.0, value=10000.0, step=100.0, format="%.2f")
        annual_maintenance = st.number_input("Ετήσιο κόστος συντήρησης (€)", min_value=0.0, value=1000.0, step=50.0, format="%.2f")

    results = calculate_property_vs_lease(
        rent_per_month, duration_years, interest_rate_annual,
        property_price, acquisition_costs, annual_maintenance, tax_rate
    )

    st.markdown("### 📊 Αποτελέσματα")

    st.subheader("💼 Εναλλακτική 1: Μίσθωση")
    st.write(f"Συνολικό καταβληθέν ποσό: **{format_number_gr(results['total_rent'], 2)} €**")
    st.write(f"Παρούσα αξία μισθώσεων: **{format_number_gr(results['rent_npv'], 2)} €**")

    st.subheader("🏠 Εναλλακτική 2: Απόκτηση")
    st.write(f"Μηνιαία δόση δανείου: **{format_number_gr(results['monthly_payment'], 2)} €**")
    st.write(f"Συνολικές πληρωμές δανείου: **{format_number_gr(results['total_loan_payments'], 2)} €**")
    st.write(f"Συνολικοί τόκοι: **{format_number_gr(results['total_interest'], 2)} €**")
    st.write(f"Φορολογικό όφελος: **{format_number_gr(results['tax_savings'], 2)} €**")
    st.write(f"Καθαρό κόστος απόκτησης (με φόρους): **{format_number_gr(results['net_acquisition_cost'], 2)} €**")

    st.subheader("⚖️ Σύγκριση")
    st.write(f"Διαφορά κόστους (Απόκτηση - Μίσθωση): **{format_number_gr(results['cost_difference'], 2)} €**")

    if results['cost_difference'] < 0:
        st.success("Η αγορά είναι φθηνότερη σε παρούσα αξία.")
    elif results['cost_difference'] > 0:
        st.error("Η μίσθωση είναι οικονομικότερη σε παρούσα αξία.")
    else:
        st.info("Οι δύο επιλογές είναι ισοδύναμες οικονομικά.")
