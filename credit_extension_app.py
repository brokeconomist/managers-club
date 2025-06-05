import streamlit as st
from credit_extension_analysis import calculate_credit_extension_impact

def show_credit_extension_analysis():
    st.title("📅 Ανάλυση Αύξησης Πίστωσης")

    with st.form("credit_extension_form"):
        col1, col2 = st.columns(2)
        with col1:
            old_credit_days = st.number_input("Τρέχουσες Μέρες Πίστωσης", value=60)
            new_credit_days = st.number_input("Νέες Μέρες Πίστωσης", value=90)
            sales_increase_pct = st.number_input("Αύξηση Πωλήσεων (%)", value=20.0)
            current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=200000.0)
            unit_price = st.number_input("Τιμή Προϊόντος (€)", value=20.0)
        with col2:
            total_cost_per_unit = st.number_input("Συνολικό Κόστος ανά Μονάδα (€)", value=18.0)
            variable_cost_per_unit = st.number_input("Μεταβλητό Κόστος ανά Μονάδα (€)", value=14.0)
            bad_debt_rate = st.number_input("Επισφαλείς Απαιτήσεις (% επί των επιπλέον πωλήσεων)", value=2.0)
            cost_of_capital = st.number_input("Κόστος Κεφαλαίου (%)", value=10.0)

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_credit_extension_impact(
            old_credit_days,
            new_credit_days,
            sales_increase_pct,
            current_sales,
            unit_price,
            total_cost_per_unit,
            variable_cost_per_unit,
            bad_debt_rate,
            cost_of_capital
        )

        st.subheader("📊 Αποτελέσματα Ανάλυσης")
        for label, value in results.items():
            st.write(f"**{label}**: € {value:,.2f}")
