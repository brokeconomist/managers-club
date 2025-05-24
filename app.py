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

def calculate_custom_clv(
    years_retained,
    purchases_per_period,
    price_per_unit,
    cost_per_unit,
    annual_marketing_cost,
    discount_rate
):
    gross_profit = purchases_per_period * (price_per_unit - cost_per_unit)
    net_cash_flow = gross_profit - annual_marketing_cost
    clv = net_cash_flow / ((1 + discount_rate) ** years_retained)
    return clv

def plot_clv_tornado_chart(
    years_retained,
    purchases_per_period,
    price_per_unit,
    cost_per_unit,
    annual_marketing_cost,
    discount_rate
):
    base_clv = calculate_custom_clv(
        years_retained,
        purchases_per_period,
        price_per_unit,
        cost_per_unit,
        annual_marketing_cost,
        discount_rate
    )

    variations = {
        "Χρόνια Πελάτη +10%": (years_retained * 1.1, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Χρόνια Πελάτη -10%": (years_retained * 0.9, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Αγορές/Περίοδο +10%": (years_retained, purchases_per_period * 1.1, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Αγορές/Περίοδο -10%": (years_retained, purchases_per_period * 0.9, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Τιμή Πώλησης +10%": (years_retained, purchases_per_period, price_per_unit * 1.1, cost_per_unit, annual_marketing_cost, discount_rate),
        "Τιμή Πώλησης -10%": (years_retained, purchases_per_period, price_per_unit * 0.9, cost_per_unit, annual_marketing_cost, discount_rate),
        "Κόστος Μονάδας +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit * 1.1, annual_marketing_cost, discount_rate),
        "Κόστος Μονάδας -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit * 0.9, annual_marketing_cost, discount_rate),
        "Κόστος Μάρκετινγκ +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost * 1.1, discount_rate),
        "Κόστος Μάρκετινγκ -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost * 0.9, discount_rate),
        "Επιτόκιο +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate * 1.1),
        "Επιτόκιο -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate * 0.9),
    }

    impacts = []
    labels = []

    for label, args in variations.items():
        new_clv = calculate_custom_clv(*args)
        delta = new_clv - base_clv
        impacts.append(delta)
        labels.append(label)

    colors = ['green' if x > 0 else 'red' for x in impacts]
    sorted_indices = np.argsort(np.abs(impacts))[::-1]
    sorted_impacts = np.array(impacts)[sorted_indices]
    sorted_labels = np.array(labels)[sorted_indices]
    sorted_colors = np.array(colors)[sorted_indices]

    fig, ax = plt.subplots()
    ax.barh(sorted_labels, sorted_impacts, color=sorted_colors)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlabel("Μεταβολή στην CLV (€)")
    ax.set_title("Tornado Chart Ευαισθησίας CLV")
    st.pyplot(fig)

def show_investment_impact():
    st.title("📉 Μεταβολή Νεκρού Σημείου λόγω Νέας Επένδυσης")

    old_price = st.number_input("Παλαιά Τιμή Πώλησης (€)", value=10.0)
    new_price = st.number_input("Νέα Τιμή Πώλησης (€)", value=9.5)
    old_unit_cost = st.number_input("Παλαιό Κόστος ανά Μονάδα (€)", value=5.3)
    new_unit_cost = st.number_input("Νέο Κόστος ανά Μονάδα (€)", value=5.1)
    investment_cost = st.number_input("Κόστος Νέας Επένδυσης (€)", value=800.0)
    units_sold = st.number_input("Εκτιμώμενες Πωλούμενες Μονάδες", value=4000.0, min_value=10.0)

    change_percent, change_units = calculate_break_even_shift(
        old_price, new_price,
        old_unit_cost, new_unit_cost,
        investment_cost, units_sold
    )

    if change_percent is None or change_units is None:
        st.warning("Δεν ήταν δυνατός ο υπολογισμός λόγω μηδενικού παρονομαστή ή πωλήσεων.")
        return

    st.success(f"🔁 Ποσοστιαία Μεταβολή στο Νεκρό Σημείο: **{change_percent:.2f}%**")
    st.success(f"🔁 Μεταβολή στο Νεκρό Σημείο σε Μονάδες: **{change_units:.2f}**")

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
    st.markdown("""
    ### 💼 Ο οικονομικός βοηθός κάθε μικρομεσαίας επιχείρησης
    **Καλώς ήρθες!**
    Το **Managers’ Club** είναι μια online εφαρμογή που σε βοηθά να παίρνεις οικονομικές αποφάσεις χωρίς πολύπλοκα οικονομικά.
    > 🧮 Εδώ, τα οικονομικά είναι στα χέρια σου. Απλά, καθαρά, χρήσιμα.
    """)

def show_break_even():
    st.title("📊 Υπολογιστής Νεκρού Σημείου (Break-Even)")
    price_per_unit = st.number_input("Τιμή πώλησης ανά μονάδα (€)", value=100.0, min_value=0.0)
    variable_cost = st.number_input("Μεταβλητό κόστος ανά μονάδα (€)", value=75.0, min_value=0.0)
    fixed_costs = st.number_input("Σταθερά κόστη (€)", value=25000.0, min_value=0.0)

    break_even_units, break_even_revenue = calculate_break_even(price_per_unit, variable_cost, fixed_costs)
    if break_even_units is None:
        st.warning("Η τιμή πώλησης πρέπει να είναι μεγαλύτερη από το μεταβλητό κόστος.")
        return

    st.success(f"🔹 Νεκρό Σημείο σε Μονάδες: **{break_even_units:.2f}**")
    st.success(f"🔹 Νεκρό Σημείο σε Πωλήσεις (€): **{break_even_revenue:,.2f}**")
    plot_break_even(price_per_unit, variable_cost, fixed_costs, break_even_units)

def show_clv():
    st.title("📈 Αξία Πελάτη (Customer Lifetime Value)")
    years_retained = st.number_input("Χρόνια διατήρησης πελάτη", value=3.0)
    purchases_per_period = st.number_input("Αγορές ανά περίοδο", value=10.0)
    price_per_unit = st.number_input("Τιμή πώλησης (€)", value=100.0)
    cost_per_unit = st.number_input("Κόστος ανά μονάδα (€)", value=60.0)
    marketing_cost = st.number_input("Ετήσιο κόστος marketing (€)", value=200.0)
    discount_rate = st.number_input("Προεξοφλητικό επιτόκιο (%)", value=5.0) / 100

    clv = calculate_custom_clv(
        years_retained, purchases_per_period,
        price_per_unit, cost_per_unit,
        marketing_cost, discount_rate
    )
    st.success(f"Αξία Πελάτη (CLV): {clv:,.2f} €")
    plot_clv_tornado_chart(
        years_retained, purchases_per_period,
        price_per_unit, cost_per_unit,
        marketing_cost, discount_rate
    )

def show_investment_impact():
    st.title("📉 Μεταβολή Νεκρού Σημείου λόγω Νέας Επένδυσης")

    old_price = st.number_input("Παλαιά Τιμή Πώλησης (€)", value=10.0)
    new_price = st.number_input("Νέα Τιμή Πώλησης (€)", value=9.5)
    old_unit_cost = st.number_input("Παλαιό Κόστος ανά Μονάδα (€)", value=5.3)
    new_unit_cost = st.number_input("Νέο Κόστος ανά Μονάδα (€)", value=5.1)
    investment_cost = st.number_input("Κόστος Νέας Επένδυσης (€)", value=800.0)
    units_sold = st.number_input("Εκτιμώμενες Πωλούμενες Μονάδες", value=4000.0, min_value=10.0)

    break_even_change_percent, break_even_change_units = calculate_break_even_shift(
        old_price, new_price,
        old_unit_cost, new_unit_cost,
        investment_cost, units_sold
    )
    if break_even_change_percent is None:
        st.warning("Μη έγκυρα δεδομένα για υπολογισμό (διαίρεση με μηδέν).")
        return

    st.success(f"🔁 Ποσοστιαία Μεταβολή στο Νεκρό Σημείο: **{break_even_change_percent:.2f}%**")
    st.success(f"🔁 Μεταβολή στο Νεκρό Σημείο σε Μονάδες: **{break_even_change_units:.2f} μονάδες**")

### ΚΥΡΙΩΣ ΡΟΗ ###

def main():
    page = st.sidebar.selectbox("Μετάβαση σε:", [
        "🏠 Αρχική",
        "📊 Break-Even",
        "📈 Αξία Πελάτη",
        "📉 Μεταβολή Νεκρού Σημείου"
    ])

    if page == "🏠 Αρχική":
        show_home()
    elif page == "📊 Break-Even":
        show_break_even()
    elif page == "📈 Αξία Πελάτη":
        show_clv()
    elif page == "📉 Μεταβολή Νεκρού Σημείου":
        show_investment_impact()

if __name__ == "__main__":
    main()
