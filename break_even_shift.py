import streamlit as st
from utils import format_number_gr, parse_gr_number

def calculate_break_even_shift(
    fixed_costs, price_per_unit, variable_cost_per_unit,
    new_fixed_costs=None, new_price_per_unit=None, new_variable_cost_per_unit=None
):
    # Χρησιμοποιεί τα νέα αν δοθούν, αλλιώς τα παλιά
    try:
        f_costs = new_fixed_costs if new_fixed_costs is not None else fixed_costs
        p_unit = new_price_per_unit if new_price_per_unit is not None else price_per_unit
        v_cost = new_variable_cost_per_unit if new_variable_cost_per_unit is not None else variable_cost_per_unit
        
        if p_unit == v_cost:
            return None
        return f_costs / (p_unit - v_cost)
    except ZeroDivisionError:
        return None

def show_break_even_shift_calculator():
    st.header("⚙️ Αλλαγή Νεκρού Σημείου με Νέα Τιμή / Κόστος / Επένδυση")
    st.markdown("""
    Υπολογίστε τη νέα τιμή νεκρού σημείου όταν αλλάζει η τιμή πώλησης, το μεταβλητό κόστος ή τα σταθερά κόστη (επένδυση).
    """)

    with st.form("break_even_shift_form"):
        col1, col2 = st.columns(2)

        with col1:
            fixed_costs_input = st.text_input("Τρέχοντα Σταθερά Κόστη (€)", value=format_number_gr(10000))
            price_per_unit_input = st.text_input("Τρέχουσα Τιμή ανά Μονάδα (€)", value=format_number_gr(50))
            variable_cost_per_unit_input = st.text_input("Τρέχον Μεταβλητό Κόστος ανά Μονάδα (€)", value=format_number_gr(30))

        with col2:
            new_fixed_costs_input = st.text_input("Νέα Σταθερά Κόστη (€)", value="")
            new_price_per_unit_input = st.text_input("Νέα Τιμή ανά Μονάδα (€)", value="")
            new_variable_cost_per_unit_input = st.text_input("Νέο Μεταβλητό Κόστος ανά Μονάδα (€)", value="")

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        fixed_costs = parse_gr_number(fixed_costs_input)
        price_per_unit = parse_gr_number(price_per_unit_input)
        variable_cost_per_unit = parse_gr_number(variable_cost_per_unit_input)

        new_fixed_costs = parse_gr_number(new_fixed_costs_input) if new_fixed_costs_input.strip() else None
        new_price_per_unit = parse_gr_number(new_price_per_unit_input) if new_price_per_unit_input.strip() else None
        new_variable_cost_per_unit = parse_gr_number(new_variable_cost_per_unit_input) if new_variable_cost_per_unit_input.strip() else None

        if None in (fixed_costs, price_per_unit, variable_cost_per_unit):
            st.error("⚠️ Εισάγετε σωστούς αριθμούς στα τρέχοντα κόστη και τιμές.")
            return

        new_bep = calculate_break_even_shift(
            fixed_costs, price_per_unit, variable_cost_per_unit,
            new_fixed_costs, new_price_per_unit, new_variable_cost_per_unit
        )

        if new_bep is None:
            st.error("⚠️ Η νέα τιμή πρέπει να είναι μεγαλύτερη από το νέο μεταβλητό κόστος.")
        else:
            st.success(f"✅ Νέα τιμή Νεκρού Σημείου: {format_number_gr(new_bep)} μονάδες")

    st.markdown("---")
