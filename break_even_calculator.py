# break_even_calculator.py
import streamlit as st
from utils import format_number_gr, parse_gr_number

def calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit):
    try:
        if price_per_unit == variable_cost_per_unit:
            return None
        return fixed_costs / (price_per_unit - variable_cost_per_unit)
    except ZeroDivisionError:
        return None

def show_break_even_calculator():
    st.header("🟢 Υπολογιστής Νεκρού Σημείου (Break-Even Point)")
    st.markdown("Υπολογίστε πόσες μονάδες πρέπει να πουλήσετε για να καλύψετε τα σταθερά και μεταβλητά κόστη σας.")

    with st.form("break_even_form"):
        fixed_costs_input = st.text_input("Σταθερά Κόστη (€)", value=format_number_gr(10000))
        price_per_unit_input = st.text_input("Τιμή ανά Μονάδα (€)", value=format_number_gr(50))
        variable_cost_per_unit_input = st.text_input("Μεταβλητό Κόστος ανά Μονάδα (€)", value=format_number_gr(30))
        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        fixed_costs = parse_gr_number(fixed_costs_input)
        price_per_unit = parse_gr_number(price_per_unit_input)
        variable_cost_per_unit = parse_gr_number(variable_cost_per_unit_input)

        if None in (fixed_costs, price_per_unit, variable_cost_per_unit):
            st.error("⚠️ Εισάγετε σωστούς αριθμούς σε όλα τα πεδία.")
            return

        bep = calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit)
        if bep is None:
            st.error("⚠️ Η τιμή πρέπει να είναι μεγαλύτερη από το μεταβλητό κόστος.")
        else:
            st.success(f"✅ Νεκρό Σημείο: {format_number_gr(bep)} μονάδες")

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
    st.markdown("---")
