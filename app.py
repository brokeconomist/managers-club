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

def calculate_clv_custom(retention_years, orders_per_period, price, cost, marketing, discount):
    total_cash_flow = (orders_per_period * (price - cost)) - marketing
    present_value = total_cash_flow / ((1 + discount) ** retention_years)
    return total_cash_flow, present_value

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

    st.markdown("""
    Εισήγαγε τις παραμέτρους για τον υπολογισμό της εκτιμώμενης συνολικής και καθαρής αξίας των μελλοντικών εισπράξεων από τον πελάτη:
    """)

    retention_years = st.number_input("📅 Εκτιμώμενος Χρόνος που ο Πελάτης Παραμένει (σε έτη)", value=5.0, min_value=0.0)
    orders_per_period = st.number_input("🛒 Εκτιμώμενη Πρόβλεψη Αγορών ανά Περίοδο", value=10.0, min_value=0.0)
    price = st.number_input("💶 Τιμή Πώλησης για τον Πελάτη (€)", value=100.0, min_value=0.0)
    cost = st.number_input("⚙️ Κόστος ανά Μονάδα (€)", value=60.0, min_value=0.0)
    marketing = st.number_input("📢 Ετήσιες Δαπάνες Μάρκετινγκ ειδικά για τον Πελάτη (€)", value=100.0, min_value=0.0)
    discount = st.number_input("📉 Προεξοφλητικό Επιτόκιο (%)", value=10.0, min_value=0.0) / 100

    total_cf, present_val = calculate_clv_custom(retention_years, orders_per_period, price, cost, marketing, discount)

    st.success(f"📦 Εκτιμώμενη Συνολική Αξία Μελλοντικών Εισπράξεων: **{total_cf:,.2f} €**")
    st.success(f"💰 Εκτιμώμενη Καθαρή Παρούσα Αξία Εισπράξεων: **{present_val:,.2f} €**")

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
