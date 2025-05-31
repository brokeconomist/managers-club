import streamlit as st
import matplotlib.pyplot as plt

# --- Χρήσιμες βοηθητικές συναρτήσεις για ελληνική μορφή αριθμών ---
def parse_gr_number(number_str):
    return float(number_str.replace('.', '').replace(',', '.'))

def format_number_gr(number, decimals=2):
    return f"{number:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(number, decimals=1):
    return f"{number*100:.{decimals}f}%".replace(".", ",")

# --- Υπολογισμός νεκρού σημείου ---
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

    fixed_costs_old = old_cm * units_sold
    fixed_costs_new = fixed_costs_old + investment_cost

    old_break_even = fixed_costs_old / old_cm
    new_break_even = fixed_costs_new / new_cm

    percent_change = (new_break_even - old_break_even) / old_break_even
    units_change = new_break_even - old_break_even

    return percent_change, units_change

# --- Γραφική απεικόνιση ---
def plot_break_even_shift(old_price, new_price, old_cost, new_cost, investment_cost, units_sold):
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

# --- Streamlit UI ---
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
        try:
            old_price = parse_gr_number(old_price_input)
            new_price = parse_gr_number(new_price_input)
            old_cost = parse_gr_number(old_cost_input)
            new_cost = parse_gr_number(new_cost_input)
            investment_cost = parse_gr_number(investment_cost_input)
            units_sold = parse_gr_number(units_sold_input)

            percent_change, units_change = calculate_break_even_shift_v2(
                old_price, new_price, old_cost, new_cost, investment_cost, units_sold
            )

            if percent_change is None:
                st.error("Το περιθώριο συνεισφοράς είναι μηδέν ή αρνητικό. Δεν μπορεί να υπολογιστεί το νεκρό σημείο.")
            else:
                st.success("✅ Αποτελέσματα Υπολογισμού")
                st.markdown(f"- Μεταβολή Νεκρού Σημείου (σε τεμάχια): **{format_number_gr(units_change, 0)}**")
                st.markdown(f"- Ποσοστιαία Μεταβολή: **{format_percentage_gr(percent_change)}**")
                plot_break_even_shift(old_price, new_price, old_cost, new_cost, investment_cost, units_sold)

        except Exception as e:
            st.error(f"⚠️ Σφάλμα στην είσοδο: {e}")
