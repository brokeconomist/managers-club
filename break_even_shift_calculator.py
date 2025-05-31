import streamlit as st
from utils import format_number_gr, parse_gr_number, format_percentage_gr
from break_even_shift_chart import calculate_break_even_shift_v2, plot_break_even_shift

def show_break_even_shift_calculator():
    st.header("🟠 Ανάλυση Αλλαγής στο Νεκρό Σημείο με Νέα Τιμή / Κόστος / Επένδυση")
    st.title("Τι αλλάζει στο 'μηδέν' μου αν ανεβάσω τιμές ή επενδύσω;")

    st.markdown("""
    Σκεφτήκατε να ανεβάσετε τιμή; Ή να επενδύσετε σε κάτι νέο;

    👉 Αυτό το εργαλείο δείχνει μια εκτίμηση του πώς **αλλάζει** το νεκρό σας σημείο (σε τεμάχια και ευρώ) όταν:
    - Ανεβάζετε τιμή
    - Αλλάζει το κόστος
    - Ή κάνετε μια νέα επένδυση

    Ιδανικό για να πάρετε απόφαση αν «σας συμφέρει».
    """)

    with st.form("break_even_shift_form"):
        old_price_input = st.text_input("Παλιότερη Τιμή Πώλησης (€):", value="10,00")
        new_price_input = st.text_input("Νέα Τιμή Πώλησης (€):", value="11,00")
        old_cost_input = st.text_input("Παλιό Κόστος Μονάδας (€):", value="6,00")
        new_cost_input = st.text_input("Νέο Κόστος Μονάδας (€):", value="6,50")
        investment_cost_input = st.text_input("Κόστος Επένδυσης (€):", value=format_number_gr(2000.00))
        units_sold_input = st.text_input("Πωλήσεις Μονάδων (τελευταία περίοδος):", value=format_number_gr(500, decimals=0))
        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        old_price = parse_gr_number(old_price_input)
        new_price = parse_gr_number(new_price_input)
        old_cost = parse_gr_number(old_cost_input)
        new_cost = parse_gr_number(new_cost_input)
        investment_cost = parse_gr_number(investment_cost_input)
        units_sold = parse_gr_number(units_sold_input)

        if None in (old_price, new_price, old_cost, new_cost, investment_cost, units_sold):
            st.warning("⚠️ Παρακαλώ εισάγετε έγκυρους αριθμούς σε όλα τα πεδία.")
            return

        percent_change, units_change = calculate_break_even_shift_v2(
            old_price, new_price, old_cost, new_cost, investment_cost, units_sold
        )

        if percent_change is None:
            st.error("🚫 Υπολογισμός αδύνατος με τα δοσμένα στοιχεία (διαίρεση με μηδέν).")
            return

        st.success(f"📉 Αλλαγή Νεκρού Σημείου (%): {format_percentage_gr(percent_change)}")
        st.success(f"📦 Αλλαγή Νεκρού Σημείου (μονάδες): {format_number_gr(units_change, 0)} μονάδες")

        plot_break_even_shift(
            old_price, new_price,
            old_cost, new_cost,
            investment_cost,
            units_sold
        )

        st.markdown("---")

import matplotlib.pyplot as plt
import streamlit as st

def calculate_break_even_shift_v2(
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

def plot_break_even_shift(
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
