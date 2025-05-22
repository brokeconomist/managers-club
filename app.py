import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Managers' Club", page_icon="📊", layout="centered")

### ΥΠΟΛΟΓΙΣΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ###

def calculate_break_even(price_per_unit, variable_cost, fixed_costs):
    if price_per_unit <= variable_cost:
        return None, None
    contribution_margin = price_per_unit - variable_cost
    break_even_units = fixed_costs / contribution_margin
    break_even_revenue = break_even_units * price_per_unit
    return break_even_units, break_even_revenue

def credit_control(CurrentCreditDays, NewCreditDays, SalesIncrease, CurrentSales,
                   UnitPrice, TotalUnitCost, VariableUnitCost, ExpectedBadDebts, InterestRateOnDebt):
    current_units = CurrentSales / UnitPrice
    avg_cost_per_unit = ((TotalUnitCost * current_units) + (current_units * SalesIncrease * VariableUnitCost)) / (current_units + current_units * SalesIncrease)
    term1 = current_units * SalesIncrease * (UnitPrice - VariableUnitCost)
    term2_num = (CurrentSales * (1 + SalesIncrease)) / (360 / NewCreditDays)
    term2_inner = (avg_cost_per_unit / UnitPrice)
    term2_diff = (CurrentSales / (360 / CurrentCreditDays)) * (TotalUnitCost / UnitPrice)
    term2 = term2_num * (term2_inner - term2_diff) * InterestRateOnDebt
    term3 = CurrentSales * (1 + SalesIncrease) * ExpectedBadDebts
    result = term1 - (term2 + term3)
    return result

### ΣΥΝΑΡΤΗΣΕΙΣ ΓΙΑ ΑΠΕΙΚΟΝΙΣΗ ###

def plot_break_even(price_per_unit, variable_cost, fixed_costs, break_even_units):
    units = list(range(0, int(break_even_units * 2) + 1))
    revenue = [price_per_unit * u for u in units]
    total_cost = [fixed_costs + variable_cost * u for u in units]
    fig, ax = plt.subplots()
    ax.plot(units, revenue, label="Έσοδα")
    ax.plot(units, total_cost, label="Συνολικό Κόστος")
    ax.axvline(break_even_units, color="red", linestyle="--", label="Νεκρό Σημείο")
    ax.set_xlabel("Μονάδες Πώλησης")
    ax.set_ylabel("€")
    ax.set_title("Break-Even Analysis")
    ax.legend()
    st.pyplot(fig)

### UI ΣΥΝΑΡΤΗΣΕΙΣ ###

def show_home():
    st.title("📊 Managers’ Club")
    st.subheader("Ο οικονομικός βοηθός κάθε μικρομεσαίας επιχείρησης.")
    st.markdown("""
    Καλώς ήρθες!

    Το **Managers’ Club** είναι μια online εφαρμογή που σε βοηθά να παίρνεις οικονομικές αποφάσεις **χωρίς πολύπλοκα οικονομικά**.

    ### Τι μπορείς να κάνεις:
    - ✅ Υπολογίσεις break-even και ανάλυση κόστους
    - ✅ Πλάνο πληρωμών & εισπράξεων
    - ✅ Υποστήριξη τιμολόγησης και πιστωτικής πολιτικής

    ---
    🧮 Εδώ, τα οικονομικά μιλάνε απλά.  
    Δεν αντικαθιστούμε τους συμβούλους σου – **τους διευκολύνουμε**.
    """)

def show_break_even():
    st.title("📊 Υπολογιστής Νεκρού Σημείου (Break-Even)")
    price_per_unit = st.number_input("Τιμή πώλησης ανά μονάδα (€)", value=1000.0, min_value=0.0)
    variable_cost = st.number_input("Μεταβλητό κόστος ανά μονάδα (€)", value=720.0, min_value=0.0)
    fixed_costs = st.number_input("Σταθερά κόστη (€)", value=261000.0, min_value=0.0)

    break_even_units, break_even_revenue = calculate_break_even(price_per_unit, variable_cost, fixed_costs)
    if break_even_units is None:
        st.warning("Η τιμή πώλησης πρέπει να είναι μεγαλύτερη από το μεταβλητό κόστος.")
        return

    st.success(f"🔹 Νεκρό Σημείο σε Μονάδες: **{break_even_units:.2f}**")
    st.success(f"🔹 Νεκρό Σημείο σε Πωλήσεις (€): **{break_even_revenue:,.2f}**")

    plot_break_even(price_per_unit, variable_cost, fixed_costs, break_even_units)

def show_credit():
    st.title("📉 Υπολογιστής Πίστωσης")
    CurrentCreditDays = st.number_input("Τρέχουσες μέρες πίστωσης", min_value=1, value=90)
    NewCreditDays = st.number_input("Νέες μέρες πίστωσης", min_value=1, value=60)
    SalesIncrease = st.number_input("Αύξηση πωλήσεων (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1) / 100
    CurrentSales = st.number_input("Τρέχουσες πωλήσεις (€)", min_value=0.0, value=1000.0)
    UnitPrice = st.number_input("Τιμή ανά μονάδα (€)", min_value=0.0, value=1000.0)
    TotalUnitCost = st.number_input("Συνολικό κόστος ανά μονάδα (€)", min_value=0.0, value=800.0)
    VariableUnitCost = st.number_input("Μεταβλητό κόστος ανά μονάδα (€)", min_value=0.0, value=720.0)
    ExpectedBadDebts = st.number_input("Αναμενόμενες ζημίες (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1) / 100
    InterestRateOnDebt = st.number_input("Επιτόκιο δανεισμού (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1) / 100

    impact = credit_control(CurrentCreditDays, NewCreditDays, SalesIncrease, CurrentSales,
                            UnitPrice, TotalUnitCost, VariableUnitCost, ExpectedBadDebts, InterestRateOnDebt)

    st.write(f"🧾 Οικονομικό αποτέλεσμα αλλαγής πίστωσης: **{impact:,.2f} €**")

### MAIN ###

def main():
    page = st.sidebar.selectbox("Μετάβαση σε:", [
        "🏠 Αρχική",
        "📊 Break-Even",
        "📉 Πίστωση",
        "📈 Αξία Πελάτη"
    ])

    if page == "🏠 Αρχική":
        show_home()
    elif page == "📊 Break-Even":
        show_break_even()
    elif page == "📉 Πίστωση":
        show_credit()
    elif page == "📈 Αξία Πελάτη":
        show_clv()

if __name__ == "__main__":
    main()
