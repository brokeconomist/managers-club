import streamlit as st
from utils import format_number_gr, parse_gr_number, format_percentage_gr
import math

def cash_discount_efficiency():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    st.markdown("""
    #### Εισροές
    Συμπλήρωσε τα βασικά στοιχεία για να αξιολογήσεις την απόδοση μιας προτεινόμενης έκπτωσης για πληρωμή τοις μετρητοίς.
    """)

    col1, col2 = st.columns(2)

    with col1:
        sales = parse_gr_number(st.text_input("Ετήσιες Πωλήσεις (€)", "500.000"))
        current_collection_days = parse_gr_number(st.text_input("Τρέχουσες Ημέρες Είσπραξης", "60"))
        new_collection_days = parse_gr_number(st.text_input("Νέες Ημέρες Είσπραξης (με Έκπτωση)", "15"))
        discount_rate = parse_gr_number(st.text_input("Ποσοστό Έκπτωσης (%)", "2")) / 100

    with col2:
        gross_margin = parse_gr_number(st.text_input("Μικτό Περιθώριο (%)", "30")) / 100
        expected_sales_increase = parse_gr_number(st.text_input("Προσδοκώμενη Αύξηση Πωλήσεων (%)", "5")) / 100
        wacc = parse_gr_number(st.text_input("WACC / Επιτόκιο Αναφοράς (%)", "12")) / 100
        years = parse_gr_number(st.text_input("Ορίζοντας Χρόνου Ανάλυσης (έτη)", "1"))

    # Υπολογισμοί
    avg_daily_sales = sales / 365
    current_receivables = avg_daily_sales * current_collection_days
    new_sales = sales * (1 + expected_sales_increase)
    new_avg_daily_sales = new_sales / 365
    new_receivables = new_avg_daily_sales * new_collection_days
    capital_released = current_receivables - new_receivables

    sales_diff = new_sales - sales
    gross_profit_from_extra_sales = sales_diff * gross_margin
    discount_cost = new_sales * discount_rate
    net_annual_benefit = gross_profit_from_extra_sales - discount_cost

    if wacc > 0:
        npv = net_annual_benefit * (1 - (1 + wacc) ** (-years)) / wacc
    else:
        npv = net_annual_benefit * years

    breakeven_increase = discount_cost / gross_margin / sales
    optimal_discount = gross_margin * expected_sales_increase

    # Αποτελέσματα
    st.markdown("""
    #### Αποτελέσματα
    """)

    st.success(f"**Αποδέσμευση Κεφαλαίου:** {format_number_gr(capital_released)} €")
    st.success(f"**Καθαρό Ετήσιο Όφελος:** {format_number_gr(net_annual_benefit)} €")
    st.success(f"**Καθαρή Παρούσα Αξία (NPV):** {format_number_gr(npv)} €")

    st.info(f"**Ελάχιστη Απαραίτητη Αύξηση Πωλήσεων για Break-even:** {format_percentage_gr(breakeven_increase)}")
    st.info(f"**Βέλτιστο Ποσοστό Έκπτωσης:** {format_percentage_gr(optimal_discount)}")

    st.markdown("---")
    st.caption("Υπολογισμοί βασισμένοι σε cash flow εξοικονόμησης, όφελος μικτού κέρδους από αύξηση πωλήσεων και κόστος της έκπτωσης.")
