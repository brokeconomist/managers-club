import streamlit as st

def calculate_credit_extension_simple(
    current_credit_days: int,
    new_credit_days: int,
    sales_increase_pct: float,
    current_sales: float,
    unit_price: float,
    total_unit_cost: float,
    variable_unit_cost: float,
    bad_debt_pct: float,
    capital_cost_pct: float,
):
    units = current_sales / unit_price
    increased_sales = current_sales * (1 + sales_increase_pct)
    increased_units = units * (1 + sales_increase_pct)

    # Net profit from additional sales
    net_profit = units * sales_increase_pct * (unit_price - variable_unit_cost)

    # Weighted average unit cost after increase
    total_cost_old = units * total_unit_cost
    total_cost_new = (increased_units - units) * variable_unit_cost
    total_combined_cost = total_cost_old + total_cost_new
    weighted_unit_cost = total_combined_cost / increased_units

    # Capital tied up before and after credit extension
    capital_old = current_sales / 360 * current_credit_days * (total_unit_cost / unit_price)
    capital_new = increased_sales / 360 * new_credit_days * (weighted_unit_cost / unit_price)
    additional_capital = capital_new - capital_old

    # Total cost: cost of capital + bad debts
    capital_cost = additional_capital * capital_cost_pct
    bad_debt_cost = increased_sales * bad_debt_pct
    total_cost = capital_cost + bad_debt_cost

    # Final anticipated gain
    anticipated_gain = net_profit - total_cost

    return {
        "Net Profit": round(net_profit, 2),
        "Total Cost from Increase": round(total_cost, 2),
        "Anticipated Gain": round(anticipated_gain, 2),
        "Suggestion": "Increase Credit" if anticipated_gain > 0 else "Do Not Increase Credit"
    }

def show_credit_extension_analysis():
    st.title("📊 Ανάλυση Επέκτασης Χρόνου Πίστωσης")

    st.header("📌 Τρέχουσα Κατάσταση")
    current_credit_days = st.number_input("Μέρες Πίστωσης", value=60, min_value=1)

    st.header("📈 Νέα Πρόταση")
    new_credit_days = st.number_input("Νέες Μέρες Πίστωσης", value=90, min_value=1)
    sales_increase_pct = st.number_input("Ποσοστό Αύξησης Πωλήσεων (%)", value=20.0, step=1.0) / 100

    st.header("💼 Οικονομικά Δεδομένα")
    current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=20_000_000, step=100_000)
    unit_price = st.number_input("Τιμή Μονάδας (€)", value=20.0)
    total_unit_cost = st.number_input("Συνολικό Κόστος ανά Μονάδα (€)", value=18.0)
    variable_unit_cost = st.number_input("Μεταβλητό Κόστος ανά Μονάδα (€)", value=14.0)
    bad_debt_pct = st.number_input("Ποσοστό Επισφαλειών (%)", value=2.0) / 100
    capital_cost_pct = st.number_input("Κόστος Κεφαλαίου (%)", value=10.0) / 100

    if st.button("Υπολογισμός"):
        results = calculate_credit_extension_simple(
            current_credit_days,
            new_credit_days,
            sales_increase_pct,
            current_sales,
            unit_price,
            total_unit_cost,
            variable_unit_cost,
            bad_debt_pct,
            capital_cost_pct,
        )

        st.header("📊 Αποτελέσματα")
        st.metric("Καθαρό Κέρδος (€)", f"{results['Net Profit']:,.2f}")
        st.metric("Συνολικό Κόστος (€)", f"{results['Total Cost from Increase']:,.2f}")
        st.metric("Εκτιμώμενο Κέρδος (€)", f"{results['Anticipated Gain']:,.2f}")
        st.success(f"Πρόταση: {results['Suggestion']}")
