import streamlit as st
import pandas as pd
import plotly.express as px
from utils import format_number_gr, parse_gr_number

def calculate_clv_discounted(
    purchases_per_period,
    price_per_purchase,
    cost_per_purchase,
    marketing_cost_per_period,
    retention_years,
    discount_rate
):
    try:
        net_margin_per_period = (purchases_per_period * (price_per_purchase - cost_per_purchase)) - marketing_cost_per_period
        if discount_rate == 0:
            clv = net_margin_per_period * retention_years
        else:
            discount_factor = (1 - (1 + discount_rate) ** (-retention_years)) / discount_rate
            clv = net_margin_per_period * discount_factor
        return clv
    except Exception:
        return None

def tornado_data(clv_base, params, delta=0.1):
    results = []
    for key, value in params.items():
        if value is None or value == 0:
            continue
        params_plus = params.copy()
        params_plus[key] = value * (1 + delta)
        clv_plus = calculate_clv_discounted(**params_plus)

        params_minus = params.copy()
        params_minus[key] = value * (1 - delta)
        clv_minus = calculate_clv_discounted(**params_minus)

        pct_plus = ((clv_plus - clv_base) / clv_base) * 100 if clv_base != 0 else 0
        pct_minus = ((clv_minus - clv_base) / clv_base) * 100 if clv_base != 0 else 0

        results.append({
            "Παράμετρος": key,
            "Μεταβολή": f"+{int(delta*100)}%",
            "Επίδραση (%)": pct_plus
        })
        results.append({
            "Παράμετρος": key,
            "Μεταβολή": f"-{int(delta*100)}%",
            "Επίδραση (%)": pct_minus
        })

    mapping = {
    "purchases_per_period": "Αγορές ανά Περίοδο",
    "price_per_purchase": "Τιμή ανά Αγορά",
    "cost_per_purchase": "Κόστος ανά Αγορά",
    "marketing_cost_per_period": "Δαπάνες Μάρκετινγκ",
    "retention_years": "Χρόνια Παραμονής",
    "discount_rate": "Επιτόκιο Προεξόφλησης"
}

    df = pd.DataFrame(results)
    df["Παράμετρος"] = df["Παράμετρος"].map(mapping)
    return df

def show_clv_calculator():
    st.title("👥 Υπολογισμός Αξίας Πελάτη (CLV) με Προεξόφληση")

    purchases_str = st.text_input("Προβλεπόμενες αγορές ανά περίοδο (π.χ. έτος)", "10")
    price_str = st.text_input("Τιμή πώλησης ανά αγορά (€)", "100")
    cost_str = st.text_input("Κόστος ανά αγορά (€)", "60")
    marketing_str = st.text_input("Δαπάνες μάρκετινγκ ανά περίοδο (€)", "20")
    retention_str = st.text_input("Εκτιμώμενα χρόνια παραμονής πελάτη", "5")
    discount_str = st.text_input("Προεξοφλητικό επιτόκιο (π.χ. 0,05 για 5%)", "0,05")

    purchases = parse_gr_number(purchases_str)
    price = parse_gr_number(price_str)
    cost = parse_gr_number(cost_str)
    marketing = parse_gr_number(marketing_str)
    retention = parse_gr_number(retention_str)
    discount = parse_gr_number(discount_str)

    if None in [purchases, price, cost, marketing, retention, discount]:
        st.error("Παρακαλώ συμπληρώστε σωστά όλα τα πεδία με αριθμούς.")
        return

    clv = calculate_clv_discounted(
        purchases_per_period=purchases,
        price_per_purchase=price,
        cost_per_purchase=cost,
        marketing_cost_per_period=marketing,
        retention_years=retention,
        discount_rate=discount,
    )

    if clv is None:
        st.error("Σφάλμα στους υπολογισμούς. Ελέγξτε τις τιμές εισόδου.")
        return

    st.success(f"Η εκτιμώμενη καθαρή παρούσα αξία πελάτη είναι: {format_number_gr(clv)} €")

    # Tornado Chart
    st.subheader("📊 Ανάλυση Ευαισθησίας (Tornado Chart)")

    params = {
        "purchases_per_period": purchases,
        "price_per_purchase": price,
        "cost_per_purchase": cost,
        "marketing_cost_per_period": marketing,
        "retention_years": retention,
        "discount_rate": discount,
    }

    df_tornado = tornado_data(clv, params, delta=0.1)

    fig = px.bar(
        df_tornado,
        x="Επίδραση (%)",
        y="Παράμετρος",
        color="Μεταβολή",
        orientation="h",
        title="Ευαισθησία CLV σε Μεταβολές Παραμέτρων",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
