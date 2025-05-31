import streamlit as st
import matplotlib.pyplot as plt

def calculate_break_even_units(price, cost, fixed_costs):
    contribution_margin = price - cost
    if contribution_margin <= 0:
        return None
    return fixed_costs / contribution_margin

def calculate_break_even_shift_v2(old_price, new_price, old_cost, new_cost, investment_cost, units_sold):
    old_cm = old_price - old_cost
    new_cm = new_price - new_cost

    if old_cm <= 0 or new_cm <= 0:
        return (None, None)

    # Υπολογισμός αρχικών και νέων σταθερών εξόδων
    fixed_costs_old = old_cm * units_sold
    fixed_costs_new = fixed_costs_old + investment_cost

    old_break_even = fixed_costs_old / old_cm
    new_break_even = fixed_costs_new / new_cm

    percent_change = (new_break_even - old_break_even) / old_break_even
    units_change = new_break_even - old_break_even

    return percent_change, units_change

def plot_break_even_shift(old_price, new_price, old_cost, new_cost, investment_cost, units_sold):
    # Υπολογισμός σταθερών εξόδων
    old_cm = old_price - old_cost
    fixed_costs_old = old_cm * units_sold
    fixed_costs_new = fixed_costs_old + investment_cost

    x = list(range(0, int(units_sold * 2)))
    old_total_cost = [fixed_costs_old + old_cost * q for q in x]
    new_total_cost = [fixed_costs_new + new_cost * q for q in x]
    old_revenue = [old_price * q for q in x]
    new_revenue = [new_price * q for q in x]

    plt.figure(figsize=(8, 5))
    plt.plot(x, old_total_cost, 'r--', label="Παλαιό Κόστος")
    plt.plot(x, new_total_cost, 'r-', label="Νέο Κόστος")
    plt.plot(x, old_revenue, 'g--', label="Παλαιά Τιμή")
    plt.plot(x, new_revenue, 'g-', label="Νέα Τιμή")
    plt.xlabel("Πωληθείσες Μονάδες")
    plt.ylabel("€")
    plt.title("Σύγκριση Νεκρού Σημείου")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
