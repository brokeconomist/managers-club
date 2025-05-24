import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Managers' Club", page_icon="📊", layout="centered")

### Βοηθητικές συναρτήσεις μορφοποίησης και parsing ###

def parse_gr_number(s):
    """Μετατρέπει αριθμό μορφής '1.234,56' σε float 1234.56"""
    if s is None or s.strip() == "":
        return None
    try:
        return float(s.replace('.', '').replace(',', '.'))
    except:
        return None

def format_number_gr(num, decimals=2):
    """Μορφοποιεί αριθμό σε ελληνικό format '1.234,56'"""
    if num is None:
        return ""
    s = f"{num:,.{decimals}f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s

### ΥΠΟΛΟΓΙΣΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ###

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
        return None, None
    percent_change = -((new_price - old_price) - (new_unit_cost - old_unit_cost)) / denominator \
                     + (investment_cost / (denominator * units_sold))
    units_change = ( -((new_price - old_price) - (new_unit_cost - old_unit_cost)) / denominator * units_sold ) \
                   + (investment_cost / denominator)
    return percent_change * 100, units_change

def calculate_custom_clv(
    years_retained,
    purchases_per_period,
    price_per_unit,
    cost_per_unit,
    annual_marketing_cost,
    discount_rate
):
    gross_profit = purchases_per_period * (price_per_unit - cost_per_unit)
    net_cash_flow = gross_profit - annual_marketing_cost
    clv = net_cash_flow / ((1 + discount_rate) ** years_retained)
    return clv

def plot_clv_tornado_chart(
    years_retained,
    purchases_per_period,
    price_per_unit,
    cost_per_unit,
    annual_marketing_cost,
    discount_rate
):
    base_clv = calculate_custom_clv(
        years_retained,
        purchases_per_period,
        price_per_unit,
        cost_per_unit,
        annual_marketing_cost,
        discount_rate
    )

    variations = {
        "Χρόνια Πελάτη +10%": (years_retained * 1.1, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Χρόνια Πελάτη -10%": (years_retained * 0.9, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Αγορές/Περίοδο +10%": (years_retained, purchases_per_period * 1.1, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Αγορές/Περίοδο -10%": (years_retained, purchases_per_period * 0.9, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Τιμή Πώλησης +10%": (years_retained, purchases_per_period, price_per_unit * 1.1, cost_per_unit, annual_marketing_cost, discount_rate),
        "Τιμή Πώλησης -10%": (years_retained, purchases_per_period, price_per_unit * 0.9, cost_per_unit, annual_marketing_cost, discount_rate),
        "Κόστος Μονάδας +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit * 1.1, annual_marketing_cost, discount_rate),
        "Κόστος Μονάδας -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit * 0.9, annual_marketing_cost, discount_rate),
        "Κόστος Μάρκετινγκ +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost * 1.1, discount_rate),
        "Κόστος Μάρκετινγκ -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost * 0.9, discount_rate),
        "Επιτόκιο +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate * 1.1),
        "Επιτόκιο -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate * 0.9),
    }

    impacts = []
    labels = []

    for label, args in variations.items():
        new_clv = calculate_custom_clv(*args)
        delta = new_clv - base_clv
        impacts.append(delta)
        labels.append(label)

    colors = ['green' if x > 0 else 'red' for x in impacts]
    sorted_indices = np.argsort(np.abs(impacts))[::-1]
    sorted_impacts = np.array(impacts)[sorted_indices]
    sorted_labels = np.array(labels)[sorted_indices]
    sorted_colors = np.array(colors)[sorted_indices]

    fig, ax = plt.subplots()
    ax.barh(sorted_labels, sorted_impacts, color=sorted_colors)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlabel("Μεταβολή στην CLV (€)")
    ax.set_title("Tornado Chart Ευαισθησίας CLV")
    st.pyplot(fig)

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

### UI ΣΥΝΑΡΤΗΣΕΙΣ ###

def show_home():
    st.title("📊 Managers’ Club")
    st.markdown("""
    ### 💼 Ο οικονομικός βοηθός κάθε μικρομεσαίας επιχείρησης

    **Καλώς ήρθες!**

    Το **Managers’ Club** είναι μια online εφαρμογή που σε βοηθά να παίρνεις οικονομικές αποφάσεις χωρίς πολύπλοκα οικονομικά.

    > 🧮 Εδώ, τα οικονομικά είναι στα χέρια σου. Απλά, καθαρά, χρήσιμα.
    """)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Οικονομικά Εργαλεία",
        "📈 Σενάρια & Στρατηγικές",
        "💼 Πελάτες & Χρηματοδότηση",
        "📉 Αποδεκτή Μείωση Πωλήσεων"
    ])

    with tab1:
        show_break_even_calculator()

    with tab2:
        show_break_even_shift_calculator()

    with tab3:
        show_clv_calculator()

    with tab4:
        show_price_increase_scenario()

def show_break_even_calculator():
    st.header("Υπολογιστής Νεκρού Σημείου (Break-Even)")
    old_price = st.number_input("Τιμή Πώλησης ανά Μονάδα (€)", min_value=0.01, value=1.5, step=0.01)
    variable_cost = st.number_input("Μεταβλητό Κόστος ανά Μονάδα (€)", min_value=0.0, value=0.7, step=0.01)
    fixed_costs = st.number_input("Συνολικά Σταθερά Κόστη (€)", min_value=0.0, value=1000.0, step=1.0)

    if st.button("Υπολόγισε Νεκρό Σημείο"):
        units, revenue = calculate_break_even(old_price, variable_cost, fixed_costs)
        if units is None:
            st.error("Η τιμή πρέπει να είναι μεγαλύτερη από το μεταβλητό κόστος.")
        else:
            st.success(f"Νεκρό Σημείο: {units:.0f} μονάδες, ή έσοδα {revenue:.2f} €")
            plot_break_even(old_price, variable_cost, fixed_costs, units)

def show_break_even_shift_calculator():
    st.header("Επίδραση Επένδυσης & Αλλαγής Τιμής στο Νεκρό Σημείο")
    old_price = st.number_input("Παλαιά Τιμή Πώλησης (€)", min_value=0.01, value=1.50, step=0.01, key="old_price_shift")
    new_price = st.number_input("Νέα Τιμή Πώλησης (€)", min_value=0.01, value=1.65, step=0.01, key="new_price_shift")
    old_cost = st.number_input("Παλαιό Μεταβλητό Κόστος (€)", min_value=0.0, value=0.70, step=0.01, key="old_cost_shift")
    new_cost = st.number_input("Νέο Μεταβλητό Κόστος (€)", min_value=0.0, value=0.75, step=0.01, key="new_cost_shift")
    investment = st.number_input("Κόστος Επένδυσης (€)", min_value=0.0, value=1000.0, step=1.0, key="investment_shift")
    units_sold = st.number_input("Μονάδες Πώλησης (προ επένδυσης)", min_value=1, value=1000, step=1, key="units_sold_shift")

    if st.button("Υπολόγισε Μεταβολή Νεκρού Σημείου"):
        pct_change, units_change = calculate_break_even_shift_v2(
            old_price, new_price, old_cost, new_cost, investment, units_sold
        )
        if pct_change is None:
            st.error("Μη έγκυρα δεδομένα για τον υπολογισμό.")
        else:
            st.success(f"Αλλαγή Νεκρού Σημείου: {pct_change:.2f} %")
            st.info(f"Μεταβολή σε Μονάδες: {units_change:.0f} μονάδες")

def show_clv_calculator():
    st.header("Υπολογιστής Customer Lifetime Value (CLV)")
    years_retained = st.number_input("Χρόνια Διατήρησης Πελάτη", min_value=1, max_value=50, value=5, step=1)
    purchases_per_period = st.number_input("Αγορές ανά Έτος", min_value=1, value=12, step=1)
    price_per_unit = st.number_input("Τιμή Πώλησης ανά Μονάδα (€)", min_value=0.01, value=50.0, step=0.01)
    cost_per_unit = st.number_input("Κόστος ανά Μονάδα (€)", min_value=0.0, value=30.0, step=0.01)
    annual_marketing_cost = st.number_input("Ετήσιο Κόστος Marketing (€)", min_value=0.0, value=100.0, step=1.0)
    discount_rate = st.number_input("Ετήσιο Επιτόκιο Προεξόφλησης (π.χ. 0.05)", min_value=0.0, max_value=1.0, value=0.05, step=0.01)

    if st.button("Υπολόγισε CLV"):
        clv = calculate_custom_clv(
            years_retained,
            purchases_per_period,
            price_per_unit,
            cost_per_unit,
            annual_marketing_cost,
            discount_rate
        )
        st.success(f"Customer Lifetime Value (CLV): {clv:.2f} €")
        plot_clv_tornado_chart(
            years_retained,
            purchases_per_period,
            price_per_unit,
            cost_per_unit,
            annual_marketing_cost,
            discount_rate
        )

def show_price_increase_scenario():
    st.header("📈 Εκτίμηση Αποδεκτής Μείωσης Πωλήσεων Προϊόντος Α μετά από Αύξηση Τιμής")

    with st.form("price_increase_form"):
        col1, col2 = st.columns(2)

        with col1:
            old_price = st.number_input("Τιμή ανά μονάδα Προϊόντος Α (€)", min_value=0.01, value=1.50, step=0.01)
            price_increase_pct = st.number_input("Αύξηση τιμής (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
            profit_A = st.number_input("Κέρδος ανά μονάδα Προϊόντος Α (€)", min_value=0.0, value=0.5, step=0.01)

        with col2:
            profit_B = st.number_input("Κέρδος ανά μονάδα Προϊόντος Β (€)", min_value=0.0, value=0.4, step=0.01)
            profit_C = st.number_input("Κέρδος ανά μονάδα Προϊόντος Γ (€)", min_value=0.0, value=0.3, step=0.01)
            profit_D = st.number_input("Κέρδος ανά μονάδα Προϊόντος Δ (€)", min_value=0.0, value=0.2, step=0.01)

        percent_B = st.number_input("Ποσοστό Υποκατάστατων Προϊόντος Β (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
        percent_C = st.number_input("Ποσοστό Υποκατάστατων Προϊόντος Γ (%)", min_value=0.0, max_value=100.0, value=15.0, step=0.1)
        percent_D = st.number_input("Ποσοστό Υποκατάστατων Προϊόντος Δ (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)

        submitted = st.form_submit_button("Υπολόγισε")

    if submitted:
        price_increase = price_increase_pct / 100
        max_sales_drop = calculate_max_product_A_sales_drop(
            old_price, price_increase, profit_A, profit_B, profit_C, profit_D, 
            percent_B / 100, percent_C / 100, percent_D / 100
        )
        if max_sales_drop is None:
            st.error("Αδύνατος ο υπολογισμός με τα δοθέντα στοιχεία.")
        else:
            st.success(f"Αποδεκτή Μείωση Πωλήσεων Προϊόντος Α: {max_sales_drop*100:.2f} %")

if __name__ == "__main__":
    show_home()
