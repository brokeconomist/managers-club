import streamlit as st
import numpy as np

def show_discount_cash_analysis():
    st.header("Ανάλυση Έκπτωσης για Πληρωμή τοις Μετρητοίς")

    st.subheader("1. Εισαγωγή Παραμέτρων")
    current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=1000.0)
    extra_sales = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", value=250.0)
    discount_pct = st.number_input("Προσφερόμενη Έκπτωση (%)", value=2.0) / 100
    acceptance_rate = st.number_input("% Πελατών που Αποδέχονται την Έκπτωση", value=60.0) / 100
    payment_days_discount = st.number_input("Μέρες Πληρωμής με Έκπτωση", value=10.0)
    cogs_pct = st.number_input("Κόστος Πωληθέντων (% επί των πωλήσεων)", value=80.0) / 100
    wacc = st.number_input("Κόστος Κεφαλαίου (% Ετησίως)", value=20.0) / 100
    old_dso = st.number_input("Παλιά Μέση Περίοδος Είσπραξης (μέρες)", value=84.0)

    new_clients_pct = acceptance_rate
    old_clients_pct = 1 - acceptance_rate
    new_dso = payment_days_discount * new_clients_pct + old_dso * old_clients_pct
    total_sales = current_sales + extra_sales

    gross_profit_extra = extra_sales * (1 - cogs_pct)
    discount_cost = total_sales * discount_pct * acceptance_rate

    npv = (
        total_sales * acceptance_rate / ((1 + wacc / 365) ** payment_days_discount)
        + total_sales * (1 - acceptance_rate) / ((1 + wacc / 365) ** old_dso)
        - discount_cost / ((1 + wacc / 365) ** payment_days_discount)
        - current_sales / ((1 + wacc / 365) ** old_dso)
    )

    try:
        ratio = extra_sales / current_sales
        term1 = 1 - (1 / acceptance_rate)
        term2 = ((1 + wacc / 365) ** (old_dso - payment_days_discount))
        max_discount = 1 - ((1 + wacc / 365) ** (payment_days_discount - old_dso)) * (
            (term1 + ((term2 + cogs_pct * ratio * ((1 + wacc / 365) ** (old_dso - 30))) / (acceptance_rate * (1 + ratio))))
        )
        optimal_discount = (1 - ((1 + wacc / 365) ** (payment_days_discount - old_dso))) / 2
    except Exception:
        max_discount = 0
        optimal_discount = 0

    st.subheader("2. Αποτελέσματα")
    st.metric("Νέα Σταθμισμένη Μέση Περίοδος Είσπραξης (μέρες)", round(new_dso, 2))
    st.metric("NPV (€)", round(npv, 2))
    st.metric("Μέγιστη Δυνητική Έκπτωση (%)", round(max_discount * 100, 2))
    st.metric("Βέλτιστη Έκπτωση (%)", round(optimal_discount * 100, 2))
