# break_even_shift_chart.py

import matplotlib.pyplot as plt
import streamlit as st
from utils import format_number_gr

def calculate_break_even_shift(
    old_price, new_price,
    old_unit_cost, new_unit_cost,
    investment_cost, units_sold
):
    denominator = new_price - new_unit_cost
    if denominator == 0 or units_sold == 0:
        return None, None

    percent_change = -((new_price - old_price) - (new_unit_cost - old_unit_cost)) / denominator \
                     + (investment_cost / (denominator * units_sold))

    units_change = ( -((new_price - old_price) - (new_unit_cost - old_unit_cost)) / denominator * units_sold ) \
                   + (investment_cost / denominator)

    return percent_change * 100, units_change


def plot_break_even_shift(units_sold, new_price, new_cost, investment_cost, units_change):
    max_units = int(units_sold + abs(units_change) + 100)
    units = list(range(0, max_units + 1))
    revenue = [u * new_price for u in units]
    cost = [investment_cost + u * new_cost for u in units]

    break_even_new = None
    for u, r, c in zip(units, revenue, cost):
        if r >= c:
            break_even_new = u
            break

    fig, ax = plt.subplots()
    ax.plot(units, revenue, label="Έσοδα (νέα τιμή)", color="green")
    ax.plot(units, cost, label="Συνολικό Κόστος (με επένδυση)", color="orange")
    if break_even_new:
        ax.axvline(break_even_new, color="red", linestyle="--", label="Νέο Νεκρό Σημείο")
    ax.set_xlabel("Μονάδες")
    ax.set_ylabel("€")
    ax.set_title("Μεταβολή Νεκρού Σημείου")
    ax.legend()
    st.pyplot(fig)
    st.markdown(f"**Νέο Νεκρό Σημείο:** {format_number_gr(break_even_new, 0)} μονάδες")
