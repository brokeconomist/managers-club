import streamlit as st
import locale

# Ρύθμιση ελληνικής μορφής για αριθμούς
locale.setlocale(locale.LC_ALL, 'el_GR.UTF-8')

def manosv_cash_credit_control(CurrentCash, CurrentCreditPercentage, CurrentCreditDays, NewCash, NewCreditPercentage,
                                NewCreditDays, SalesIncrease, CurrentSales, UnitPrice, TotalUnitCost, VariableUnitCost,
                                ExpectedBadDebts, InterstRateOnDebt):

    # Πωληθείσες Μονάδες
    current_units = CurrentSales / UnitPrice

    # Νέες μονάδες λόγω αύξησης πωλήσεων
    new_units = current_units * SalesIncrease

    # Καθαρό κέρδος από επιπλέον πωλήσεις
    net_profit = new_units * (UnitPrice - VariableUnitCost)

    # Υπολογισμός σημερινού κόστους δέσμευσης κεφαλαίου
    credit_sales_old = CurrentSales * CurrentCreditPercentage
    old_commitment_cost = credit_sales_old * (CurrentCreditDays / 360)

    # Νέες πωλήσεις
    total_new_sales = CurrentSales * (1 + SalesIncrease)
    credit_sales_new = total_new_sales * NewCreditPercentage
    new_commitment_cost = credit_sales_new * (NewCreditDays / 360)

    # Επιπλέον δέσμευση κεφαλαίων
    additional_commitment = new_commitment_cost - old_commitment_cost

    # Κόστος χρηματοδότησης
    cost_of_capital = additional_commitment * InterstRateOnDebt

    # Κόστος επισφαλών απαιτήσεων
    bad_debt_cost = CurrentSales * ExpectedBadDebts * (1 + SalesIncrease)

    # Συνολικό κόστος
    total_cost = cost_of_capital + bad_debt_cost

    # Καθαρό όφελος
    anticipated_gain = net_profit - total_cost

    # Απόφαση
    suggestion = "Αύξηση Πίστωσης" if anticipated_gain > 0 else "Όχι Αύξηση Πίστωσης"

    return {
        "Καθαρό Κέρδος (€)": net_profit,
        "Κόστος Χρηματοδότησης (€)": cost_of_capital,
        "Κόστος Επισφαλειών (€)": bad_debt_cost,
        "Συνολικό Κόστος (€)": total_cost,
        "Καθαρό Όφελος (€)": anticipated_gain,
        "Εισήγηση": suggestion
    }


def show_credit_policy_analysis():
    st.title("💶 Ανάλυση Πολιτικής Πίστωσης (Μετρητοίς & Πίστωση)")

    with st.form("credit_policy_form"):
        st.header("🔢 Παρούσα Κατάσταση")
        col1, col2, col3 = st.columns(3)
        with col1:
            CurrentCash = st.number_input("Ποσοστό Πωλήσεων Μετρητοίς (%)", 0.0, 100.0, 50.0) / 100
        with col2:
            CurrentCreditPercentage = st.number_input("Ποσοστό Πωλήσεων με Πίστωση (%)", 0.0, 100.0, 50.0) / 100
        with col3:
            CurrentCreditDays = st.number_input("Ημέρες Πίστωσης", 0, 365, 60)

        st.header("📈 Νέα Κατάσταση")
        col4, col5, col6 = st.columns(3)
        with col4:
            NewCash = st.number_input("Νέο Ποσοστό Μετρητοίς (%)", 0.0, 100.0, 20.0) / 100
        with col5:
            NewCreditPercentage = st.number_input("Νέο Ποσοστό Πίστωσης (%)", 0.0, 100.0, 80.0) / 100
        with col6:
            NewCreditDays = st.number_input("Νέες Ημέρες Πίστωσης", 0, 365, 90)

        SalesIncrease = st.number_input("Ποσοστό Αύξησης Πωλήσεων (%)", 0.0, 100.0, 20.0) / 100

        st.header("📊 Δεδομένα Επιχείρησης")
        CurrentSales = st.number_input("Τρέχουσες Πωλήσεις (€)", 0.0, 1e9, 20_000_000.0)
        UnitPrice = st.number_input("Τιμή Μονάδας (€)", 0.01, 1e5, 20.0)
        TotalUnitCost = st.number_input("Συνολικό Κόστος Μονάδας (€)", 0.01, 1e5, 18.0)
        VariableUnitCost = st.number_input("Μεταβλητό Κόστος Μονάδας (€)", 0.01, 1e5, 14.0)
        ExpectedBadDebts = st.number_input("Ποσοστό Επισφαλειών (%)", 0.0, 100.0, 2.0) / 100
        InterstRateOnDebt = st.number_input("Κόστος Κεφαλαίου (%)", 0.0, 100.0, 10.0) / 100

        submitted = st.form_submit_button("🔍 Υπολογισμός")

    if submitted:
        results = manosv_cash_credit_control(CurrentCash, CurrentCreditPercentage, CurrentCreditDays, NewCash,
                                             NewCreditPercentage, NewCreditDays, SalesIncrease, CurrentSales,
                                             UnitPrice, TotalUnitCost, VariableUnitCost, ExpectedBadDebts,
