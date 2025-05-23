
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

def calculate_clv_custom(periods_customer_remains, purchases_per_period, price_per_unit,
                         cost_per_unit, annual_marketing_costs, discount_rate):
    gross_value = purchases_per_period * (price_per_unit - cost_per_unit)
    total_value = gross_value * periods_customer_remains - annual_marketing_costs
    net_clv = total_value / (1 + discount_rate) ** periods_customer_remains
    return net_clv, total_value

### ΓΡΑΦΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ###

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

def plot_clv_tornado_aggregate(data, base_params):
    param_names = list(base_params.keys())
    effects = []

    for param in param_names:
        deltas = []

        for change in [-0.1, 0.1]:
            temp_params = base_params.copy()
            temp_params[param] *= (1 + change)
            temp_data = data.copy()

            for col in temp_params:
                if col in temp_data.columns:
                    temp_data[col] = temp_params[col]

            temp_data["CLV"] = temp_data.apply(lambda row: calculate_clv_custom(
                row["Χρόνος Πιστότητας"],
                row["Αγορές ανά Περίοδο"],
                row["Τιμή Πώλησης"],
                row["Κόστος ανά Μονάδα"],
                row["Μάρκετινγκ"],
                row["Προεξόφληση"]
            )[0], axis=1)

            avg_clv = temp_data["CLV"].mean()
            deltas.append(avg_clv)

        effects.append(max(deltas) - min(deltas))

    y_pos = np.arange(len(param_names))
    fig, ax = plt.subplots()
    ax.barh(y_pos, effects, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(param_names)
    ax.invert_yaxis()
    ax.set_xlabel("Επίδραση στον Μέσο CLV (€)")
    ax.set_title("Ανάλυση Ευαισθησίας - Tornado Chart (Συνολικά)")
    st.pyplot(fig)

### UI ΕΝΟΤΗΤΕΣ ###

def show_home():
    st.title("📊 Managers’ Club")
    st.markdown("### 💼 Ο οικονομικός βοηθός κάθε μικρομεσαίας επιχείρησης")
    st.markdown("Το **Managers’ Club** είναι μια online εφαρμογή που σε βοηθά να παίρνεις οικονομικές αποφάσεις χωρίς πολύπλοκα οικονομικά.")

def show_break_even():
    st.title("📊 Υπολογιστής Νεκρού Σημείου (Break-Even)")
    price = st.number_input("Τιμή Πώλησης (€)", value=1000.0, min_value=0.0)
    variable = st.number_input("Μεταβλητό Κόστος (€)", value=720.0, min_value=0.0)
    fixed = st.number_input("Σταθερά Κόστη (€)", value=261000.0, min_value=0.0)
    units, revenue = calculate_break_even(price, variable, fixed)
    if units is None:
        st.warning("Η τιμή πώλησης πρέπει να είναι μεγαλύτερη από το κόστος.")
        return
    st.success(f"🔹 Νεκρό Σημείο: **{units:.2f} μονάδες**, **{revenue:,.2f} €**")
    plot_break_even(price, variable, fixed, units)

def show_clv_single():
    st.title("📈 Αξία Πελάτη (CLV - Μοναδικός Πελάτης)")
    periods = st.number_input("Χρόνος Πιστότητας (έτη)", value=3.0)
    purchases = st.number_input("Αγορές ανά Περίοδο", value=3.0)
    price = st.number_input("Τιμή Πώλησης (€)", value=500.0)
    cost = st.number_input("Κόστος ανά Μονάδα (€)", value=300.0)
    marketing = st.number_input("Μάρκετινγκ (€ ανά έτος)", value=100.0)
    discount = st.number_input("Προεξόφληση (%)", value=10.0) / 100

    net_clv, gross = calculate_clv_custom(periods, purchases, price, cost, marketing, discount)
    st.success(f"💰 Καθαρή Αξία Πελάτη: **{net_clv:,.2f} €**")
    st.caption(f"Μικτή Αξία Προ Φόρων: {gross:,.2f} €")

def show_clv_multiple():
    st.title("📊 CLV για Πολλούς Πελάτες")
    uploaded = st.file_uploader("🔽 Ανέβασε CSV με δεδομένα πελατών", type="csv")
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        required_cols = ["Χρόνος Πιστότητας", "Αγορές ανά Περίοδο", "Τιμή Πώλησης",
                         "Κόστος ανά Μονάδα", "Μάρκετινγκ", "Προεξόφληση"]
        if not all(col in df.columns for col in required_cols):
            st.error(f"Το αρχείο πρέπει να περιέχει τις στήλες: {', '.join(required_cols)}")
            return

        df["CLV"], df["Ακαθάριστη Αξία"] = zip(*df.apply(lambda row: calculate_clv_custom(
            row["Χρόνος Πιστότητας"],
            row["Αγορές ανά Περίοδο"],
            row["Τιμή Πώλησης"],
            row["Κόστος ανά Μονάδα"],
            row["Μάρκετινγκ"],
            row["Προεξόφληση"]
        ), axis=1))

        st.dataframe(df.style.format({"CLV": "{:,.2f}", "Ακαθάριστη Αξία": "{:,.2f}"}))
        st.success(f"📈 Μέση Καθαρή Αξία Πελάτη: **{df['CLV'].mean():,.2f} €**")

        base_params = {col: df[col].mean() for col in required_cols}
        plot_clv_tornado_aggregate(df, base_params)

### MAIN ###

def main():
    tab = st.sidebar.radio("Μετάβαση σε:", [
        "🏠 Αρχική",
        "📊 Break-Even",
        "📈 CLV Μοναδικού Πελάτη",
        "📊 CLV Πολλών Πελατών"
    ])

    if tab == "🏠 Αρχική":
        show_home()
    elif tab == "📊 Break-Even":
        show_break_even()
    elif tab == "📈 CLV Μοναδικού Πελάτη":
        show_clv_single()
    elif tab == "📊 CLV Πολλών Πελατών":
        show_clv_multiple()

if __name__ == "__main__":
    main()

