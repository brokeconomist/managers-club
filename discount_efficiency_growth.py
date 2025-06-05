import streamlit as st
import numpy as np

from utils import format_number_gr, format_percentage_gr, parse_gr_number


def calculate_cash_discount_efficiency(current_sales, extra_sales, discount_rate, discount_acceptance,
                                       discount_days, non_acceptance, non_discount_days,
                                       cash_days, cost_percent, wacc,
                                       suppliers_days, current_collection_days):
    extra_revenue = extra_sales * (1 - cost_percent / 100)
    total_discount = current_sales * (discount_rate / 100) * (discount_acceptance / 100)
    capital_unlocked = (
        (current_sales * (discount_acceptance / 100) * (current_collection_days - discount_days)) +
        (current_sales * (non_acceptance / 100) * (current_collection_days - non_discount_days)) +
        (extra_sales * (current_collection_days - cash_days))
    ) / 365
    cost_of_capital = capital_unlocked * (wacc / 100)
    net_benefit = extra_revenue - total_discount - cost_of_capital
    total_collection_days = (
        (discount_days * discount_acceptance + non_discount_days * non_acceptance) / 100
    )
    new_total_collection_days = (
        (total_collection_days * current_sales + cash_days * extra_sales) / (current_sales + extra_sales)
    )
    cash_cycle_reduction = current_collection_days - new_total_collection_days
    new_cash_cycle = new_total_collection_days - suppliers_days

    return {
        "Κέρδος από επιπλέον πωλήσεις": format_number_gr(extra_revenue),
        "Συνολικό Κόστος Έκπτωσης": format_number_gr(total_discount),
        "Απελευθέρωση Κεφαλαίου": format_number_gr(capital_unlocked),
        "Κόστος Κεφαλαίου": format_number_gr(cost_of_capital),
        "Καθαρό Όφελος": format_number_gr(net_benefit),
        "Μείωση Ημερών Είσπραξης": format_number_gr(cash_cycle_reduction),
        "Νέος Συνολικός Χρ. Κύκλος": format_number_gr(new_cash_cycle)
    }


def discount_efficiency_ui():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς με Ανάπτυξη Πωλήσεων")

    default_values = {
        "current_sales": "1000",
        "extra_sales": "250",
        "discount_rate": "2",
        "discount_acceptance": "60",
        "discount_days": "60",
        "non_discount_days": "120",
        "cash_days": "10",
        "cost_percent": "80",
        "wacc": "20",
        "suppliers_days": "30",
        "current_collection_days": "84"
    }

    with st.form("discount_efficiency_form"):
        st.markdown("### Εισαγωγή Δεδομένων")
        col1, col2 = st.columns(2)

        with col1:
            current_sales = parse_gr_number(st.text_input("Τρέχουσες Πωλήσεις (€)", default_values["current_sales"]))
            extra_sales = parse_gr_number(st.text_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", default_values["extra_sales"]))
            discount_rate = parse_gr_number(st.text_input("Ποσοστό Έκπτωσης (%)", default_values["discount_rate"]))
            discount_acceptance = parse_gr_number(st.text_input("Ποσοστό Πελατών που Δέχεται την Έκπτωση (%)", default_values["discount_acceptance"]))
            discount_days = parse_gr_number(st.text_input("Ημέρες Είσπραξης με Έκπτωση", default_values["discount_days"]))
            non_discount_days = parse_gr_number(st.text_input("Ημέρες Είσπραξης χωρίς Έκπτωση", default_values["non_discount_days"]))

        with col2:
            cash_days = parse_gr_number(st.text_input("Ημέρες Πληρωμής Τοις Μετρητοίς", default_values["cash_days"]))
            cost_percent = parse_gr_number(st.text_input("Μέσο Κόστος επί των Πωλήσεων (%)", default_values["cost_percent"]))
            wacc = parse_gr_number(st.text_input("Κόστος Κεφαλαίου (WACC %) ετησίως", default_values["wacc"]))
            suppliers_days = parse_gr_number(st.text_input("Μέση Περίοδος Πληρωμής Προμηθευτών", default_values["suppliers_days"]))
            current_collection_days = parse_gr_number(st.text_input("Τρέχουσα Μέση Περίοδος Είσπραξης", default_values["current_collection_days"]))

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted or "discount_submitted" not in st.session_state:
        st.session_state.discount_submitted = True

        non_acceptance = 100 - discount_acceptance

        results = calculate_cash_discount_efficiency(
            current_sales,
            extra_sales,
            discount_rate,
            discount_acceptance,
            discount_days,
            non_acceptance,
            non_discount_days,
            cash_days,
            cost_percent,
            wacc,
            suppliers_days,
            current_collection_days
        )

        st.subheader("Αποτελέσματα")

        for label, value in results.items():
            st.write(f"**{label}:** {value} €")
