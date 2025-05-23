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

### ΣΥΝΑΡΤΗΣΕΙΣ ΓΙΑ ΑΠΕΙΚΟΝΙΣΗ ###

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
    price_per_unit = st.number_input("Τιμή πώλησης ανά μονάδα (€)", value=1000.0, min_value=0.0)
    variable_cost = st.number_input("Μεταβλητό κόστος ανά μονάδα (€)", value=720.0, min_value=0.0)
    fixed_costs = st.number_input("Σταθερά κόστη (€)", value=261000.0, min_value=0.0)

    break_even_units, break_even_revenue = calculate_break_even(price_per_unit, variable_cost, fixed_costs)
    if break_even_units is None:
        st.warning("Η τιμή πώλησης πρέπει να είναι μεγαλύτερη από το μεταβλητό κόστος.")
        return

    st.success(f"🔹 Νεκρό Σημείο σε Μονάδες: **{break_even_units:.2f}**")
    st.success(f"🔹 Νεκρό Σημείο σε Πωλήσεις (€): **{break_even_revenue:,.2f}**")

    plot_break_even(price_per_unit, variable_cost, fixed_costs, break_even_units)

def show_clv():
    st.title("📈 Αξία Πελάτη (Customer Lifetime Value)")

    st.markdown("**Συμπλήρωσε τις παρακάτω παραμέτρους για να υπολογίσεις την CLV:**")

    years_retained = st.number_input("📆 Εκτιμώμενος Χρόνος Που Ο Πελάτης Παραμένει (σε έτη)", min_value=0.0, value=3.0)
    purchases_per_period = st.number_input("🛒 Εκτιμώμενη Πρόβλεψη Αγορών Ανά Περίοδο", min_value=0.0, value=5.0)
    price_per_unit = st.number_input("💶 Τιμή Πώλησης για τον Πελάτη (€)", min_value=0.0, value=100.0)
    cost_per_unit = st.number_input("🧾 Κόστος Ανά Μονάδα (€)", min_value=0.0, value=60.0)
    marketing_cost = st.number_input("📣 Ετήσιες Δαπάνες Μάρκετινγκ (€)", min_value=0.0, value=50.0)
    discount_rate_percent = st.number_input("🏦 Προεξοφλητικό Επιτόκιο (%)", min_value=0.0, value=10.0)

    discount_rate = discount_rate_percent / 100.0

    clv = calculate_custom_clv(
        years_retained,
        purchases_per_period,
        price_per_unit,
        cost_per_unit,
        marketing_cost,
        discount_rate
    )

    st.success(f"💰 Εκτιμώμενη Καθαρή Αξία Πελάτη (CLV): **{clv:,.2f} €**")
    st.markdown("---")
    st.subheader("📊 Ανάλυση Ευαισθησίας CLV")
    st.markdown("Πώς επηρεάζεται η CLV αν αλλάξουν οι βασικές υποθέσεις;")
    plot_clv_tornado_chart(
        years_retained,
        purchases_per_period,
        price_per_unit,
        cost_per_unit,
        marketing_cost,
        discount_rate
    )

### MAIN ###

def main():
    page = st.sidebar.selectbox("Μετάβαση σε:", [
        "🏠 Αρχική",
        "📊 Break-Even",
        "📈 Αξία Πελάτη"
    ])

    if page == "🏠 Αρχική":
        show_home()
    elif page == "📊 Break-Even":
        show_break_even()
    elif page == "📈 Αξία Πελάτη":
        show_clv()

if __name__ == "__main__":
    main()
