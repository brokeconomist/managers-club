import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Managers' Club", page_icon="📊", layout="centered")

### ΥΠΟΛΟΓΙΣΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ###

def calculate_break_even(price_per_unit, variable_cost, fixed_costs):
    if price_per_unit <= variable_cost:
        return None, None
    contribution_margin = price_per_unit - variable_cost
    break_even_units = fixed_costs / contribution_margin
    break_even_revenue = break_even_units * price_per_unit
    return break_even_units, break_even_revenue

def calculate_break_even_shift(
    old_price, new_price,
    old_unit_cost, new_unit_cost,
    investment_cost, units_sold
):
    # Υπολογισμός νέων και παλαιών σταθερών κόστους προσθέτοντας την επένδυση
    old_contribution_margin = old_price - old_unit_cost
    new_contribution_margin = new_price - new_unit_cost

    if old_contribution_margin <= 0 or new_contribution_margin <= 0 or units_sold == 0:
        return None, None  # Αδύνατος υπολογισμός

    old_fixed_costs = investment_cost  # Υποθέτουμε η επένδυση αυξάνει τα σταθερά κόστη
    old_break_even_units = old_fixed_costs / old_contribution_margin
    new_fixed_costs = old_fixed_costs + investment_cost  # Εδώ αν θέλεις μπορείς να το αλλάξεις
    new_break_even_units = (old_fixed_costs + investment_cost) / new_contribution_margin

    # Υπολογισμός μεταβολών
    change_units = new_break_even_units - old_break_even_units
    change_percent = (change_units / old_break_even_units) * 100 if old_break_even_units != 0 else None

    return change_percent, change_units

# Νέα συνάρτηση με τον ακριβή τύπο που ζήτησες
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
        - 📈 Ανάλυση του Νεκρού Σημείου με Σενάρια Τιμής, Κόστους & Πάγιων Επενδύσεων (υπό υλοποίηση)
        - 🔄 Αλληλεπίδραση Υποκατάστατων και Συμπληρωματικών Προϊόντων (υπό υλοποίηση)
        """)

    with tab3:
        st.markdown("""
        - 💰 Υπολογισμός Αξίας Πελάτη (Customer Lifetime Value)
        - 🏦 Απόφαση Χρηματοδότησης: Δάνειο ή Leasing; (υπό υλοποίηση)
        - 💼 Χρηματοοικονομική Αξιολόγηση Νέων Επενδύσεων (υπό υλοποίηση)
        """)

def show_break_even():
    st.title("📊 Υπολογιστής Νεκρού Σημείου (Break-Even)")
    price_per_unit = st.number_input("Τιμή πώλησης ανά μονάδα (€)", value=100.0, min_value=0.0)
    variable_cost = st.number_input("Μεταβλητό κόστος ανά μονάδα (€)", value=75.0, min_value=0.0)
    fixed_costs = st.number_input("Σταθερά κόστη (€)", value=25000.0, min_value=0.0)

    break_even_units, break_even_revenue = calculate_break_even(price_per_unit, variable_cost, fixed_costs)
    if break_even_units is None:
        st.warning("Η τιμή πώλησης πρέπει να είναι μεγαλύτερη από το μεταβλητό κόστος.")
        return

    st.success(f"🔹 Νεκρό Σημείο σε Μονάδες: **{break_even_units:.2f}**")
    st.success(f"🔹 Νεκρό Σημείο σε Πωλήσεις (€): **{break_even_revenue:,.2f}**")
    plot_break_even(price_per_unit, variable_cost, fixed_costs, break_even_units)

def show_clv():
    st.title("📈 Αξία Πελάτη (Customer Lifetime Value)")
    years_retained = st.number_input("Χρόνια διατήρησης πελάτη", value=3.0)
    purchases_per_period = st.number_input("Αγορές ανά περίοδο", value=10.0)
    price_per_unit = st.number_input("Τιμή ανά μονάδα (€)", value=100.0)
    cost_per_unit = st.number_input("Κόστος ανά μονάδα (€)", value=60.0)
    annual_marketing_cost = st.number_input("Ετήσιο κόστος μάρκετινγκ ανά πελάτη (€)", value=50.0)
    discount_rate = st.number_input("Προεξοφλητικό επιτόκιο (%)", value=0.10)

    clv = calculate_custom_clv(
        years_retained,
        purchases_per_period,
        price_per_unit,
        cost_per_unit,
        annual_marketing_cost,
        discount_rate
    )
    st.success(f"🧾 Αξία Πελάτη (CLV): **{clv:,.2f} €**")

    st.subheader("Ανάλυση Ευαισθησίας CLV (Tornado Chart)")
    plot_clv_tornado_chart(
        years_retained,
        purchases_per_period,
        price_per_unit,
        cost_per_unit,
        annual_marketing_cost,
        discount_rate
    )

def show_investment_impact():
    st.title("📉 Μεταβολή Νεκρού Σημείου λόγω Νέας Επένδυσης")

    old_price = st.number_input("Παλαιά Τιμή Πώλησης (€)", value=10.0)
    new_price = st.number_input("Νέα Τιμή Πώλησης (€)", value=9.5)
    old_unit_cost = st.number_input("Παλαιό Κόστος ανά Μονάδα (€)", value=5.3)
    new_unit_cost = st.number_input("Νέο Κόστος ανά Μονάδα (€)", value=5.1)
    investment_cost = st.number_input("Κόστος Νέας Επένδυσης (€)", value=800.0)
    units_sold = st.number_input("Εκτιμώμενες Πωλούμενες Μονάδες", value=4000.0, min_value=10.0)

    change_percent, change_units = calculate_break_even_shift_v2(
        old_price, new_price,
        old_unit_cost, new_unit_cost,
        investment_cost, units_sold
    )
    if change_percent is None:
        st.warning("Μη έγκυρα δεδομένα για υπολογισμό (διαίρεση με μηδέν).")
        return

    st.success(f"🔁 Ποσοστιαία Μεταβολή στο Νεκρό Σημείο: **{change_percent:.2f}%**")
    st.success(f"🔁 Μεταβολή στο Νεκρό Σημείο σε Μονάδες: **{change_units:.2f} μονάδες**")

### MAIN APP ###

def main():
    menu = {
        "Αρχική": show_home,
        "Υπολογιστής Νεκρού Σημείου": show_break_even,
        "Αξία Πελάτη (CLV)": show_clv,
        "Επίδραση Επένδυσης στο Νεκρό Σημείο": show_investment_impact,
    }

    choice = st.sidebar.selectbox("Μενού", list(menu.keys()))
    menu[choice]()

if __name__ == "__main__":
    main()
