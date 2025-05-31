# break_even_chart.py

import matplotlib.pyplot as plt
import streamlit as st

# Συνάρτηση σχεδίασης γραφήματος ανάλυσης νεκρού σημείου
def plot_break_even(price_per_unit, variable_cost, fixed_costs, break_even_units):
    units = list(range(0, int(break_even_units * 2) + 1))  # Από 0 μέχρι το διπλάσιο του BEP
    revenue = [price_per_unit * u for u in units]  # Ολική είσπραξη
    total_cost = [fixed_costs + variable_cost * u for u in units]  # Ολικό κόστος

    fig, ax = plt.subplots()
    ax.plot(units, revenue, label="Έσοδα", color="green")
    ax.plot(units, total_cost, label="Συνολικό Κόστος", color="blue")
    ax.axvline(break_even_units, color="red", linestyle="--", label="Νεκρό Σημείο")
    ax.set_xlabel("Μονάδες Πώλησης")
    ax.set_ylabel("€")
    ax.set_title("Ανάλυση Νεκρού Σημείου")
    ax.legend()
    st.pyplot(fig)
    st.markdown("---")
