import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Managers' Club", page_icon="📊", layout="centered")

### Βοηθητικές συναρτήσεις μορφοποίησης και parsing ###

def format_number_gr(num, decimals=2):
    """Μορφοποιεί αριθμό σε ελληνικό format '1.234,56'"""
    if num is None:
        return ""
    s = f"{num:,.{decimals}f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s

### ΥΠΟΛΟΓΙΣΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ###

# (παραμένουν ίδιες, δεν τις αλλάζουμε)

def calculate_break_even(price_per_unit, variable_cost, fixed_costs):
    if price_per_unit <= variable_cost:
        return None, None
    contribution_margin = price_per_unit - variable_cost
    break_even_units = fixed_costs / contribution_margin
    break_even_revenue = break_even_units * price_per_unit
    return break_even_units, break_even_revenue

def calculate_break_even_shift_v2(
    old_price, new_price,
    old_unit_cost, new_unit_cost,
    investment_cost, units_sold
):
    denominator = new_price - new_unit_cost
    if denominator == 0 or units_sold == 0:
        return None, None  # Αποφυγή διαίρεσης με 0

    percent_change = -((new_price - old_price) - (new_unit_cost - old_unit_cost)) / denominator \
                     + (investment_cost / (denominator * units_sold))

    units_change = ( -((new_price - old_price) - (new_unit_cost - old_unit_cost)) / denominator * units_sold ) \
                   + (investment_cost / denominator)

    return percent_change * 100, units_change  # Ποσοστό %



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

def calculate_max_product_A_sales_drop(old_price, price_increase, profit_A, profit_B, profit_C, profit_D, percent_B, percent_C, percent_D):
    benefit_substitutes = (percent_B * profit_B + percent_C * profit_C + percent_D * profit_D)
    denominator = ((profit_A - benefit_substitutes) / old_price) + price_increase
    numerator = - price_increase
    try:
        max_sales_drop = numerator / denominator
        return max_sales_drop
    except ZeroDivisionError:
        return None

def format_percentage_gr(number):
    return f"{number:,.1f}%".replace(".", ",")

### UI ΣΥΝΑΡΤΗΣΕΙΣ ###

def show_home():
    st.title("📊 Managers’ Club")
    st.markdown("""
    ### 💼 Ο οικονομικός βοηθός κάθε μικρομεσαίας επιχείρησης

    **Καλώς ήρθες!**

    Το **Managers’ Club** είναι μια online εφαρμογή που σε βοηθά να παίρνεις οικονομικές αποφάσεις χωρίς πολύπλοκα οικονομικά.

    > 🧮 Εδώ, τα οικονομικά είναι στα χέρια σου. Απλά, καθαρά, χρήσιμα.
    """)

    tab1, tab2, tab3 = st.tabs(["📊 Οικονομικά Εργαλεία", "📈 Σενάρια & Στρατηγικές", "💼 Πελάτες & Χρηματοδότηση"])

    with tab1:
        st.markdown("""
        - 📊 Υπολογισμός Νεκρού Σημείου (Break-Even)
        - 📦 Διαχείριση Αποθεμάτων (υπό υλοποίηση)
        - 📥 Διαχείριση Εισπρακτέων Λογαριασμών (υπό υλοποίηση)
        - 📤 Διαχείριση Πληρωτέων Λογαριασμών (υπό υλοποίηση)
        - ⚙️ Μέσο Κόστος Παραγωγής ανά Μονάδα σε Οχτάωρο και Υπερωρίες (υπό υλοποίηση)
        """)

    with tab2:
        st.markdown("""
        - 📈 Ανάλυση του Νεκρού Σημείου με Σενάρια Τιμής, Κόστους & Πάγιων
        - 📉 Αξιολόγηση Επιπτώσεων Επένδυσης σε Νέες Υπηρεσίες ή Προϊόντα
        """)

    with tab3:
        st.markdown("""
        - 💵 Ανάλυση Πελάτη & Διάρκειας Ζωής Πελάτη (CLV)
        - 📅 Εκτίμηση Χρηματοδοτικών Αναγκών
        """)

### ΒΑΣΙΚΕΣ ΕΙΣΟΔΟΙ ΚΑΙ ΥΠΟΛΟΓΙΣΜΟΙ ###

def show_break_even_calculator():
    st.header("Υπολογιστής Νεκρού Σημείου (Break-Even Point)")

    # Είσοδοι ως ελληνικά μορφοποιημένα κείμενα
    price_input = st.text_input("Τιμή Πώλησης ανά Μονάδα (€):", value="10,00")
    variable_cost_input = st.text_input("Μεταβλητό Κόστος ανά Μονάδα (€):", value="6,00")
    fixed_costs_input = st.text_input("Πάγια Έξοδα (€):", value="1000,00")

    price = parse_gr_number(price_input)
    variable_cost = parse_gr_number(variable_cost_input)
    fixed_costs = parse_gr_number(fixed_costs_input)

    if None in (price, variable_cost, fixed_costs):
        st.warning("Παρακαλώ εισάγετε έγκυρους αριθμούς σε όλα τα πεδία.")
        return

    be_units, be_revenue = calculate_break_even(price, variable_cost, fixed_costs)

    if be_units is None:
        st.error("Η Τιμή Πώλησης πρέπει να είναι μεγαλύτερη από το Μεταβλητό Κόστος.")
        return

    st.success(f"Νεκρό Σημείο σε Μονάδες: {format_number_gr(be_units, 0)} μονάδες")
    st.success(f"Νεκρό Σημείο σε Έσοδα: {format_number_gr(be_revenue)} €")

    plot_break_even(price, variable_cost, fixed_costs, be_units)

def show_break_even_shift_calculator():
    st.header("Ανάλυση Αλλαγής στο Νεκρό Σημείο με Νέα Τιμή / Κόστος / Επένδυση")

    old_price_input = st.text_input("Παλιότερη Τιμή Πώλησης (€):", value="10,00", key="old_price")
    new_price_input = st.text_input("Νέα Τιμή Πώλησης (€):", value="11,00", key="new_price")
    old_cost_input = st.text_input("Παλιό Κόστος Μονάδας (€):", value="6,00", key="old_cost")
    new_cost_input = st.text_input("Νέο Κόστος Μονάδας (€):", value="6,50", key="new_cost")
    investment_cost_input = st.text_input("Κόστος Επένδυσης (€):", value="2000,00", key="investment_cost")
    units_sold_input = st.text_input("Πωλήσεις Μονάδων (τελευταία περίοδος):", value="500", key="units_sold")

    old_price = parse_gr_number(old_price_input)
    new_price = parse_gr_number(new_price_input)
    old_cost = parse_gr_number(old_cost_input)
    new_cost = parse_gr_number(new_cost_input)
    investment_cost = parse_gr_number(investment_cost_input)
    units_sold = parse_gr_number(units_sold_input)

    if None in (old_price, new_price, old_cost, new_cost, investment_cost, units_sold):
        st.warning("Παρακαλώ εισάγετε έγκυρους αριθμούς σε όλα τα πεδία.")
        return

    percent_change, units_change = calculate_break_even_shift_v2(
        old_price, new_price, old_cost, new_cost, investment_cost, units_sold
    )

    if percent_change is None:
        st.error("Υπολογισμός αδύνατος με τα δοσμένα στοιχεία (διαίρεση με μηδέν).")
        return

    st.success(f"Αλλαγή Νεκρού Σημείου (%): {percent_change:.2f} %")
    st.success(f"Αλλαγή Νεκρού Σημείου (μονάδες): {format_number_gr(units_change, 0)} μονάδες")

def parse_gr_number(s):
    """Μετατρέπει αριθμό μορφής '1.234,56' σε float 1234.56"""
    if s is None or s.strip() == "":
        return None
    try:
        return float(s.replace('.', '').replace(',', '.'))
    except:
        return None

def show_price_increase_scenario():
    st.header("📈 Εκτίμηση Αποδεκτής Μείωσης Πωλήσεων Προϊόντος Α μετά από Αύξηση Τιμής")

    with st.form("price_increase_form"):
        col1, col2 = st.columns(2)

        with col1:
            old_price = st.number_input("Τιμή ανά κιλό Προϊόντος Α (€)", min_value=0.01, value=1.50, step=0.01)
            price_increase_pct = st.number_input("Αύξηση τιμής (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1) / 100
            profit_A = st.number_input("Κέρδος ανά μονάδα Προϊόντος Α (€)", min_value=0.0, value=0.30, step=0.01)

        with col2:
            profit_B = st.number_input("Κέρδος ανά μονάδα Προϊόντος Β (€)", min_value=0.0, value=0.20, step=0.01)
            profit_C = st.number_input("Κέρδος ανά μονάδα Προϊόντος Γ (€)", min_value=0.0, value=0.20, step=0.01)
            profit_D = st.number_input("Κέρδος ανά μονάδα Προϊόντος Δ (€)", min_value=0.0, value=0.05, step=0.01)

        percent_B = st.slider("Ποσοστό πελατών που θα αγοράσουν Προϊόν Β (%)", 0.0, 100.0, 45.0) / 100
        percent_C = st.slider("Ποσοστό πελατών που θα αγοράσουν Προϊόν Γ (%)", 0.0, 100.0, 20.0) / 100
        percent_D = st.slider("Ποσοστό πελατών που θα αγοράσουν Προϊόν Δ (%)", 0.0, 100.0, 5.0) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        total_substitute = percent_B + percent_C + percent_D
        if total_substitute > 1:
            st.error("❌ Το συνολικό ποσοστό πελατών που επιλέγουν άλλα προϊόντα δεν μπορεί να ξεπερνά το 100%.")
            return

        no_purchase = 1 - total_substitute

        result = calculate_max_product_A_sales_drop(
            old_price,
            price_increase_pct,
            profit_A,
            profit_B,
            profit_C,
            profit_D,
            percent_B,
            percent_C,
            percent_D
        )

        if result is None:
            st.error("❌ Αδυναμία υπολογισμού. Δοκίμασε άλλες τιμές.")
        else:
            st.success(f"✅ Μέγιστη αποδεκτή μείωση πωλήσεων Προϊόντος Α: {format_number_gr(result)}%")
            st.info(f"ℹ️ Ποσοστό πελατών που δεν θα αγοράσουν τίποτα: {format_percentage_gr(no_purchase * 100)}")

### MAIN MENU ###

menu = st.sidebar.radio("📊 Επιλογή Εργαλείου", (
    "Αρχική Σελίδα",
    "Υπολογιστής Νεκρού Σημείου",
    "Ανάλυση Αλλαγής Νεκρού Σημείου",
    "Ανάλυση Υποκατάστασης Προϊόντων"
))

if menu == "Αρχική Σελίδα":
    show_home()
elif menu == "Υπολογιστής Νεκρού Σημείου":
    show_break_even_calculator()
elif menu == "Ανάλυση Αλλαγής Νεκρού Σημείου":
    show_break_even_shift_calculator()
elif menu == "Ανάλυση Υποκατάστασης Προϊόντων":
    show_price_increase_scenario()
