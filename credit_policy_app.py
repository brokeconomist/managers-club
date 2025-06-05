import streamlit as st

def calculate_credit_policy_analysis(
    CurrentCash, CurrentCreditPercentage, CurrentCreditDays,
    NewCash, NewCreditPercentage, NewCreditDays,
    SalesIncrease, CurrentSales, UnitPrice,
    TotalUnitCost, VariableUnitCost,
    ExpectedBadDebts, InterstRateOnDebt
):
    current_units = CurrentSales / UnitPrice
    new_sales = CurrentSales * (1 + SalesIncrease)
    new_units = new_sales / UnitPrice

    # Καθαρό Κέρδος από Αύξηση Πωλήσεων
    net_profit = current_units * SalesIncrease * (UnitPrice - VariableUnitCost)

    # Κόστος Παρούσας Δέσμευσης Κεφαλαίου
    current_credit_sales = CurrentSales * CurrentCreditPercentage
    current_capital_cost = (current_credit_sales * TotalUnitCost / UnitPrice) * (CurrentCreditDays / 360)

    # Κόστος Προτεινόμενης Δέσμευσης Κεφαλαίου
    new_credit_sales = new_sales * NewCreditPercentage
    weighted_unit_cost = (
        (current_units * TotalUnitCost + (new_units - current_units) * VariableUnitCost)
        / new_units
    )
    new_capital_cost = (new_credit_sales * weighted_unit_cost) * (NewCreditDays / 360)

    # Επισφάλειες
    bad_debts = (new_sales * ExpectedBadDebts)

    # Τελικό Κόστος
    capital_cost_diff = (new_capital_cost - current_capital_cost) * InterstRateOnDebt
    total_cost = capital_cost_diff + bad_debts

    # Καθαρό Όφελος
    anticipated_gain = net_profit - total_cost

    return net_profit, total_cost, anticipated_gain

def show_credit_policy_analysis():
    st.header("🏦 Ανάλυση Πολιτικής Πίστωσης")

    with st.form("credit_policy_form"):
        st.subheader("Παρούσα Κατάσταση")
        col1, col2, col3 = st.columns(3)
        CurrentCash = col1.number_input("Ποσοστό Πωλήσεων Μετρητοίς (%)", value=50.0) / 100
        CurrentCreditPercentage = col2.number_input("Ποσοστό Πωλήσεων με Πίστωση (%)", value=50.0) / 100
        CurrentCreditDays = col3.number_input("Ημέρες Πίστωσης", value=60)

        st.subheader("Προτεινόμενη Κατάσταση")
        col4, col5, col6 = st.columns(3)
        NewCash = col4.number_input("Νέο Ποσοστό Μετρητοίς (%)", value=20.0) / 100
        NewCreditPercentage = col5.number_input("Νέο Ποσοστό Πίστωσης (%)", value=80.0) / 100
        NewCreditDays = col6.number_input("Νέες Ημέρες Πίστωσης", value=90)

        st.subheader("Δεδομένα Πωλήσεων & Κόστους")
        SalesIncrease = st.number_input("Αναμενόμενη Αύξηση Πωλήσεων (%)", value=20.0) / 100
        CurrentSales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=20_000_000)
        UnitPrice = st.number_input("Τιμή Μονάδας (€)", value=20.0)
        TotalUnitCost = st.number_input("Συνολικό Κόστος Μονάδας (€)", value=18.0)
        VariableUnitCost = st.number_input("Μεταβλητό Κόστος Μονάδας (€)", value=14.0)
        ExpectedBadDebts = st.number_input("Επισφάλειες (%)", value=2.0) / 100
        InterstRateOnDebt = st.number_input("Κόστος Κεφαλαίου (%)", value=10.0) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        net_profit, total_cost, gain = calculate_credit_policy_analysis(
            CurrentCash, CurrentCreditPercentage, CurrentCreditDays,
            NewCash, NewCreditPercentage, NewCreditDays,
            SalesIncrease, CurrentSales, UnitPrice,
            TotalUnitCost, VariableUnitCost,
            ExpectedBadDebts, InterstRateOnDebt
        )

        st.success("✅ Αποτελέσματα:")
        st.metric("Καθαρό Κέρδος από Αύξηση Πωλήσεων (€)", f"{net_profit:,.0f}")
        st.metric("Συνολικό Κόστος (€)", f"{total_cost:,.0f}")
        st.metric("Καθαρό Όφελος (€)", f"{gain:,.0f}")

        if gain > 0:
            st.info("💡 Πρόταση: **Αξίζει** να εφαρμοστεί η νέα πολιτική πίστωσης.")
        else:
            st.warning("⚠️ Πρόταση: **Δεν αξίζει** να εφαρμοστεί η νέα πολιτική πίστωσης.")
