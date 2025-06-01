import streamlit as st
import pandas as pd
import numpy as np
from utils import format_number_gr, parse_gr_number, format_percentage_gr

def calculate_cash_discount(
    current_sales, extra_sales, gross_margin,
    discount_rate, accept_rate,
    days_accept, days_non_accept,
    current_collection_days, wacc
):
    profit_extra = extra_sales * gross_margin
    new_sales = current_sales + extra_sales

    pct_new_policy = (current_sales * accept_rate + extra_sales) / new_sales
    pct_old_policy = 1 - pct_new_policy

    new_avg_days = pct_new_policy * days_accept + pct_old_policy * days_non_accept

    old_receivables = (current_sales * current_collection_days) / 365
    new_receivables = (new_sales * new_avg_days) / 365

    capital_released = old_receivables - new_receivables
    profit_release = capital_released * wacc

    discount_cost = new_sales * pct_new_policy * discount_rate

    total_profit = profit_extra + profit_release - discount_cost
    npv = total_profit / (1 + wacc)

    return {
        "profit_extra": profit_extra,
        "profit_release": profit_release,
        "discount_cost": discount_cost,
        "total_profit": total_profit,
        "npv": npv,
        "pct_new_policy": pct_new_policy,
        "new_sales": new_sales,
        "new_avg_days": new_avg_days,
        "capital_released": capital_released
    }

def find_break_even_and_optimal(
    current_sales, extra_sales, gross_margin,
    accept_rate, days_accept, days_non_accept,
    current_collection_days, wacc
):
    discounts = np.linspace(0.0, 0.30, 301)
    npv_list = []

    for d in discounts:
        res = calculate_cash_discount(
            current_sales, extra_sales, gross_margin,
            d, accept_rate, days_accept, days_non_accept,
            current_collection_days, wacc
        )
        npv_list.append(res["npv"])

    npv_arr = np.array(npv_list)
    idx_opt = npv_arr.argmax()
    idx_be = np.abs(npv_arr).argmin()

    return discounts[idx_opt], discounts[idx_be], discounts, npv_list

def show_cash_discount_ui():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    col1, col2 = st.columns(2)
    with col1:
        current_sales = parse_gr_number(st.text_input("Τρέχουσες Πωλήσεις (€)", "100.000"))
        extra_sales = parse_gr_number(st.text_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", "20.000"))
        gross_margin = st.slider("Μικτό Περιθώριο Κέρδους (%)", 0.0, 1.0, 0.30, 0.01)
        accept_rate = st.slider("Ποσοστό Πελατών που Δέχεται την Έκπτωση (%)", 0.0, 1.0, 0.6, 0.01)

    with col2:
        days_accept = st.number_input("Ημέρες Είσπραξης με Έκπτωση", 0, 365, 10)
        days_non_accept = st.number_input("Ημέρες Είσπραξης χωρίς Έκπτωση", 0, 365, 45)
        current_collection_days = st.number_input("Τρέχουσες Ημέρες Είσπραξης", 0, 365, 40)
        wacc = st.slider("Κόστος Κεφαλαίου (WACC)", 0.0, 0.5, 0.12, 0.01)

    st.subheader("Αποτελέσματα για ποσοστά έκπτωσης 0%–30%")

    opt_disc, be_disc, discounts, npvs = find_break_even_and_optimal(
        current_sales, extra_sales, gross_margin,
        accept_rate, days_accept, days_non_accept,
        current_collection_days, wacc
    )

    df = pd.DataFrame({
        "Έκπτωση": discounts * 100,
        "Καθαρή Παρούσα Αξία": npvs
    })

    st.line_chart(df.rename(columns={"Έκπτωση": "Ποσοστό Έκπτωσης (%)"}).set_index("Ποσοστό Έκπτωσης (%)"))

    st.markdown(f"**Βέλτιστη Έκπτωση:** {format_percentage_gr(opt_disc)}")
    st.markdown(f"**Οριακή (Break-even) Έκπτωση:** {format_percentage_gr(be_disc)}")

    with st.expander("Ανάλυση για τη Βέλτιστη Έκπτωση"):
        result = calculate_cash_discount(
            current_sales, extra_sales, gross_margin,
            opt_disc, accept_rate, days_accept, days_non_accept,
            current_collection_days, wacc
        )

        st.write(f"Κέρδος από νέες πωλήσεις: {format_number_gr(result['profit_extra'])} €")
        st.write(f"Απόδοση αποδέσμευσης κεφαλαίου: {format_number_gr(result['profit_release'])} €")
        st.write(f"Κόστος από τις εκπτώσεις: {format_number_gr(result['discount_cost'])} €")
        st.write(f"Καθαρό όφελος: {format_number_gr(result['total_profit'])} €")
        st.write(f"Καθαρή Παρούσα Αξία: {format_number_gr(result['npv'])} €")
