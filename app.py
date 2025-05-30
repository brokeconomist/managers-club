import streamlit as st
from home import show_home
from break_even import show_break_even_calculator
from break_even_shift import show_break_even_shift_calculator
from clv import show_clv_calculator
from substitution import show_price_increase_scenario
from complement import show_required_sales_increase_calculator
from price_loss_limit import show_loss_threshold_before_price_cut

st.set_page_config(page_title="Managers’ Club", layout="centered")

menu = st.sidebar.radio("📊 Επιλογή Εργαλείου", (
    "Αρχική Σελίδα",
    "Υπολογιστής Νεκρού Σημείου",
    "Ανάλυση Αλλαγής Νεκρού Σημείου",
    "Υπολογιστής Αξίας Πελάτη (CLV)",
    "Ανάλυση Υποκατάστασης Προϊόντων",
    "Ανάλυση Συμπληρωματικών Προϊόντων",
    "Όριο Απώλειας Πωλήσεων πριν Μείωση Τιμής"
))

if menu == "Αρχική Σελίδα":
    show_home()
elif menu == "Υπολογιστής Νεκρού Σημείου":
    show_break_even_calculator()
elif menu == "Ανάλυση Αλλαγής Νεκρού Σημείου":
    show_break_even_shift_calculator()
elif menu == "Υπολογιστής Αξίας Πελάτη (CLV)":
    show_clv_calculator()
elif menu == "Ανάλυση Υποκατάστασης Προϊόντων":
    show_price_increase_scenario()
elif menu == "Ανάλυση Συμπληρωματικών Προϊόντων":
    show_required_sales_increase_calculator()
elif menu == "Όριο Απώλειας Πωλήσεων πριν Μείωση Τιμής":
    show_loss_threshold_before_price_cut()
