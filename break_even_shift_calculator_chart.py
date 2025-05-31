import matplotlib.pyplot as plt
import streamlit as st

def calculate_break_even_shift_calculator(
    old_price, new_price,
    old_unit_cost, new_unit_cost,
    investment_cost, units_sold
):
    denominator = new_price - new_unit_cost
    if denominator == 0 or units_sold == 0:
        return None, None

    percent_change = -((new_price - old_price) - (new_unit_cost - old_unit_cost)) / denominator \
                     + (investment_cost / (denominator * units_sold))

    units_change = (-((new_price - old_price) - (new_unit_cost - old_unit_cost)) / denominator * units_sold) \
                   + (investment_cost / denominator)

    return percent_change * 100, units_change

def plot_break_even_shift_calculator(
    old_price, new_price,
    old_unit_cost, new_unit_cost,
    investment_cost, units_sold
):
    # Εσόδα & κόστη για παλιά και νέα κατάσταση
    old_revenue = [old_price * x for x in range(0, int(units_sold * 2) + 1)]
    old_total_cost = [old_unit_cost * x for x in range(0, int(units_sold * 2) + 1)]

    new_revenue = [new_price * x for x in range(0, int(units_sold * 2) + 1)]
    new_total_cost = [investment_cost + new_unit_cost * x for x in range(0, int(units_sold * 2) + 1)]

    units = list(range(0, int(units_sold * 2) + 1))

    fig, ax = plt.subplots()
    ax.plot(units, old_revenue, label="Παλιό Έσοδο", linestyle="--", color="green")
    ax.plot(units, old_total_cost, label="Παλιό Κόστος", linestyle="--", color="red")

    ax.plot(units, new_revenue, label="Νέο Έσοδο", color="blue")
    ax.plot(units, new_total_cost, label="Νέο Κόστος", color="orange")

    ax.set_xlabel("Μονάδες Πώλησης")
    ax.set_ylabel("€")
    ax.set_title("Σύγκριση Break-Even Πριν και Μετά την Αλλαγή")
    ax.legend()
    st.pyplot(fig)
