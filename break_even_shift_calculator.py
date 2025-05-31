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
        # Ανάλυση και μετατροπή τιμών
        old_price = parse_gr_number(old_price_input)
        new_price = parse_gr_number(new_price_input)
        old_cost = parse_gr_number(old_cost_input)
        new_cost = parse_gr_number(new_cost_input)
        investment_cost = parse_gr_number(investment_cost_input)
        units_sold = parse_gr_number(units_sold_input)

        if None in (old_price, new_price, old_cost, new_cost, investment_cost, units_sold):
            st.warning("⚠️ Παρακαλώ εισάγετε έγκυρους αριθμούς σε όλα τα πεδία.")
            return

        # Υπολογισμός αλλαγής στο νεκρό σημείο
        percent_change, units_change = calculate_break_even_shift_v2(
            old_price, new_price, old_cost, new_cost, investment_cost, units_sold
        )

        if percent_change is None:
            st.error("🚫 Υπολογισμός αδύνατος με τα δοσμένα στοιχεία (π.χ. διαίρεση με μηδέν).")
            return

        st.success(f"📉 Αλλαγή Νεκρού Σημείου (%): {format_percentage_gr(percent_change)}")
        st.success(f"📦 Αλλαγή Νεκρού Σημείου (μονάδες): {format_number_gr(units_change, 0)} μονάδες")

        # Διάγραμμα
        plot_break_even_shift(
            old_price, new_price,
            old_cost, new_cost,
            investment_cost,
            units_sold
        )

        st.markdown("---")
