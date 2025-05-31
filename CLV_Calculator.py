import streamlit as st
import pandas as pd
import altair as alt
from utils import format_number_gr, parse_gr_number

def calculate_clv_discounted(
    purchases_per_period,
    price_per_purchase,
    cost_per_purchase,
    marketing_cost,
    retention_years,
    discount_rate
):
    try:
        margin_per_purchase = price_per_purchase - cost_per_purchase
        net_margin_per_year = (purchases_per_period * margin_per_purchase) - marketing_cost
        if discount_rate == 0:
            return net_margin_per_year * retention_years
        else:
            pv_factor = (1 - (1 + discount_rate) ** (-retention_years)) / discount_rate
            return net_margin_per_year * pv_factor
    except Exception:
        return None

def tornado_data(clv_base, params, delta=0.1):
    """
    Δημιουργεί δεδομένα για tornado chart.
    params: dict με όνομα παραμέτρου και την τρέχουσα τιμή της.
    delta: ποσοστό μεταβολής (πχ 0.1 = 10%)
    Επιστρέφει DataFrame με % μεταβολής στο CLV για +/- delta κάθε παραμέτρου.
    """
    results = []
    for key, value in params.items():
        if value == 0:
            continue  # Αποφυγή διαίρεσης με μηδέν
        # +delta
        params_plus = params.copy()
        params_plus[key] = value * (1 + delta)
        clv_plus = calculate_clv_discounted(**params_plus)
        # -delta
        params_minus = params.copy()
        params_minus[key] = value * (1 - delta)
        clv_minus = calculate_clv_discounted(**params_minus)

        # % αλλαγή σε σχέση με βασικό
        pct_plus = ((clv_plus - clv_base) / clv_base) * 100 if clv_base != 0 else 0
        pct_minus = ((clv_minus - clv_base) / clv_base) * 100 if clv_base != 0 else 0

        results.append({"Parameter": key, "Change": f"+{int(delta*100)}%", "Impact (%)": pct_plus})
        results.append({"Parameter": key, "Change": f"-{int(delta*100)}%", "Impact (%)": pct_minus})

    df = pd.DataFrame(results)
    # Για να φαίνεται ωραία στο γράφημα
    df["Parameter"] = df["Parameter"].map({
        "purchases_per_period": "Αγορές ανά Περίοδο",
        "price_per_purchase": "Τιμή ανά Αγορά",
        "cost_per_purchase": "Κόστος ανά Αγορά",
        "marketing_cost": "Δαπάνες Μάρκετινγκ",
        "retention_years": "Χρόνια Παραμονής",
        "discount_rate": "Επιτόκιο Προεξόφλησης"
    })
    return df

def show_clv_calculator():
    st.header("👥 Υπολογιστής Αξίας Πελάτη (Customer Lifetime Value - CLV) με Tornado Chart")
    st.markdown("""
    Υπολογίστε την εκτιμώμενη αξία πελάτη και δείτε την ευαισθησία των παραμέτρων με το tornado chart.
    """)

    with st.form("clv_form"):
        purchases_per_period_input = st.text_input("Αγορές ανά Περίοδο (π.χ. έτος)", value="12")
        price_per_purchase_input = st.text_input("Τιμή ανά Αγορά (€)", value="20")
        cost_per_purchase_input = st.text_input("Κόστος ανά Αγορά (€)", value="10")
        marketing_cost_input = st.text_input("Δαπάνες Μάρκετινγκ ανά Έτος (€)", value="30")
        retention_years_input = st.text_input("Χρόνια Παραμονής Πελάτη", value="3")
        discount_rate_input = st.text_input("Ετήσιο Επιτόκιο Προεξόφλησης (π.χ. 0.05 για 5%)", value="0.05")

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        purchases_per_period = parse_gr_number(purchases_per_period_input)
        price_per_purchase = parse_gr_number(price_per_purchase_input)
        cost_per_purchase = parse_gr_number(cost_per_purchase_input)
        marketing_cost = parse_gr_number(marketing_cost_input)
        retention_years = parse_gr_number(retention_years_input)
        discount_rate = parse_gr_number(discount_rate_input)

        if None in (
            purchases_per_period, price_per_purchase, cost_per_purchase,
            marketing_cost, retention_years, discount_rate
        ):
            st.error("⚠️ Συμπληρώστε όλα τα πεδία σωστά.")
            return

        params = {
            "purchases_per_period": purchases_per_period,
            "price_per_purchase": price_per_purchase,
            "cost_per_purchase": cost_per_purchase,
            "marketing_cost": marketing_cost,
            "retention_years": retention_years,
            "discount_rate": discount_rate
        }

        clv_base = calculate_clv_discounted(**params)
        if clv_base is None:
            st.error("⚠️ Σφάλμα στον υπολογισμό του CLV με τις δοθείσες τιμές.")
            return

        st.success(f"✅ Εκτιμώμενη Προεξοφλημένη Αξία Πελάτη: {format_number_gr(clv_base)} €")

        # Δημιουργία tornado data
        df_tornado = tornado_data(clv_base, params, delta=0.1)

        # Altair tornado chart
        chart = alt.Chart(df_tornado).mark_bar().encode(
            x=alt.X("Impact (%):Q", title="Επίδραση % στο CLV"),
            y=alt.Y("Parameter:N", sort='-x', title="Παράμετρος"),
            color=alt.Color("Change:N", scale=alt.Scale(domain=["+10%", "-10%"], range=["#2ca02c", "#d62728"])),
            tooltip=["Parameter", "Change", alt.Tooltip("Impact (%)", format=".2f")]
        ).properties(
            width=700,
            height=300,
            title="Ανάλυση Ευαισθησίας CLV (Tornado Chart)"
        )

        st.altair_chart(chart, use_container_width=True)

    st.markdown("---")
