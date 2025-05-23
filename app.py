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

def calculate_clv(remaining_years, purchases_per_period, price_per_unit, unit_cost, marketing_cost, discount_rate):
    future_cash_flows = purchases_per_period * (price_per_unit - unit_cost)
    total_cash_flows = future_cash_flows - marketing_cost
    clv = total_cash_flows / ((1 + discount_rate) ** remaining_years)
    return clv

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

def plot_clv_tornado(base_clv, params_dict):
    labels = list(params_dict.keys())
    values = []
    for key, val in params_dict.items():
        delta = 0.1 * val if val != 0 else 1
        new_params = params_dict.copy()
        new_params[key] = val + delta

        new_clv = calculate_clv(
            remaining_years=new_params["Χρόνος παραμονής πελάτη (έτη)"],
            purchases_per_period=new_params["Αγορές ανά περίοδο"],
            price_per_unit=new_params["Τιμή πώλησης (€)"],
            unit_cost=new_params["Κόστος ανά μονάδα (€)"],
            marketing_cost=new_params["Ετήσιο κόστος marketing (€)"],
            discount_rate=new_params["Προεξοφλητικό επιτόκιο (%)"] / 100
        )
        values.append(new_clv - base_clv)

    y_pos = np.arange(len(labels))
    fig, ax = plt.subplots()
    ax.barh(y_pos, values, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Επίδραση στην Αξία Πελάτη (€)")
    ax.set_title("Ανάλυση Ευαισθησίας - Tornado Chart")
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

    params = {
        "Χρόνος παραμονής πελάτη (έτη)": 3.0,
        "Αγορές ανά περίοδο": 5.0,
        "Τιμή πώλησης (€)": 5000.0,
        "Κόστος ανά μονάδα (€)": 3000.0,
        "Ετήσιο κόστος marketing (€)": 2000.0,
        "Προεξοφλητικό επιτόκιο (%)": 7.0,
    }

    st.markdown("**Ρύθμισε τις παραμέτρους:**")
    for key in params:
        params[key] = st.number_input(key, value=float(params[key]), min_value=0.0)

    clv = calculate_clv(
        remaining_years=params["Χρόνος παραμονής πελάτη (έτη)"],
        purchases_per_period=params["Αγορές ανά περίοδο"],
        price_per_unit=params["Τιμή πώλησης (€)"],
        unit_cost=params["Κόστος ανά μονάδα (€)"],
        marketing_cost=params["Ετήσιο κόστος marketing (€)"],
        discount_rate=params["Προεξοφλητικό επιτόκιο (%)"] / 100
    )

    st.success(f"💰 Εκτιμώμενη Καθαρή Αξία Πελάτη: **{clv:,.2f} €**")

    plot_clv_tornado(clv, params)

### MAIN ###

def main():
    page = st.sidebar.selectbox("Μετάβαση σε:", [
        "🏠 Αρχική",
        "📊 Break-Even",
        "📈 Αξία Πελάτη"
    ])

    if page == "🏠 Αρχική":
        show_home()
    elif page == "📊 Break-Even":
        show_break_even()
    elif page == "📈 Αξία Πελάτη":
        show_clv()

if __name__ == "__main__":
    main()

