import streamlit as st
import locale

locale.setlocale(locale.LC_ALL, 'el_GR.UTF-8')

def calculate_credit_extension_simple(unit_price, variable_cost, sales_increase_pct,
                                      current_sales, new_credit_days, cost_of_capital_pct,
                                      bad_debt_pct):

    additional_sales = current_sales * sales_increase_pct
    contribution_margin = unit_price - variable_cost
    profit_from_new_sales = additional_sales * contribution_margin

    financing_cost = current_sales * (new_credit_days / 360) * cost_of_capital_pct
    bad_debt_cost = current_sales * bad_debt_pct

    total_cost = financing_cost + bad_debt_cost
    net_gain = profit_from_new_sales - total_cost

    return {
        "Κέρδος από Νέες Πωλήσεις (€)": profit_from_new_sales,
        "Κόστος Χρηματοδότησης (€)": financing_cost,
        "Κόστος Επισφαλειών (€)": bad_debt_cost,
        "Συνολικό Κόστος (€)": total_cost,
        "Καθαρό Όφελος (€)": net_gain
    }

def show_credit_extension_analysis():
    st.title("🕒 Ανάλυση Αύξησης Πίστωσης")

    with st.form("credit_extension_form"):
        st.subheader("📊 Εισαγωγή Δεδομένων")

        unit_price = st.number_input("Τιμή Μονάδας (€)", 0.01, 1e6, 20.0)
        variable_cost = st.number_input("Μεταβλητό Κόστος (€)", 0.01, 1e6, 12.0)
        sales_increase_pct = st.number_input("Αναμενόμενη Αύξηση Πωλήσεων (%)", 0.0, 100.0, 10.0) / 100
        current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", 0.0, 1e9, 1_000_000.0)
        new_credit_days = st.number_input("Αύξηση Ημερών Πίστωσης", 0, 365, 30)
        cost_of_capital_pct = st.number_input("Κόστος Κεφαλαίου (%)", 0.0, 100.0, 8.0) / 100
        bad_debt_pct = st.number_input("Ποσοστό Επισφαλειών (%)", 0.0, 100.0, 2.0) / 100

        submitted = st.form_submit_button("🔍 Υπολογισμός")

    if submitted:
        results = calculate_credit_extension_simple(
            unit_price, variable_cost, sales_increase_pct,
            current_sales, new_credit_days, cost_of_capital_pct,
            bad_debt_pct
        )

        st.subheader("📈 Αποτελέσματα")
        for label, value in results.items():
            st.metric(label, locale.format_string('%.0f', value, grouping=True))
