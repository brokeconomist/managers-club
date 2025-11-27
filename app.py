import streamlit as st

# Εδώ εισάγεις όλα τα module σου
from break_even_calculator import show_break_even_calculator
from break_even_shift_calculator import show_break_even_shift_calculator
from clv_calculator import show_clv_calculator
from substitution_analysis import show_substitution_analysis
from complementary_analysis import show_complementary_analysis
from loss_threshold import show_loss_threshold_before_price_cut
from credit_extension_analysis import show_credit_extension_analysis
from credit_policy_app import show_credit_policy_analysis
from supplier_credit_app import show_supplier_credit_analysis
from cash_cycle import run_cash_cycle_app
from loan_vs_leasing_calculator import loan_vs_leasing_ui
from gross_profit_analysis import show_gross_profit_template
from unit_cost_app import show_unit_cost_app
from discount_npv_ui import show_discount_npv_ui
from economic_order_quantity import show_economic_order_quantity
from credit_days_calculator import show_credit_days_calculator
from inventory_turnover_calculator import show_inventory_turnover_calculator

st.set_page_config(page_title="Managers’ Club", page_icon="📊", layout="wide")

st.title("📊 Managers’ Club - Επιλογή Εργαλείου")

# Δημιουργία tabs για τις κύριες κατηγορίες εργαλείων
tabs = st.tabs(["Ανάλυση Κερδοφορίας", "Διαχείριση Πίστωσης", "Διαχείριση Αποθεμάτων", "CLV / Πελάτες", "Άλλα Εργαλεία"])

with tabs[0]:  # Ανάλυση Κερδοφορίας
    st.subheader("Ανάλυση Κερδοφορίας")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Νεκρό Σημείο (Break-Even)"):
            show_break_even_calculator()
        if st.button("⚙️ Αλλαγή Νεκρού Σημείου"):
            show_break_even_shift_calculator()
        if st.button("📈 Υπολογισμός Μικτού Κέρδους"):
            show_gross_profit_template()
        if st.button("💰 NPV για Έκπτωση Πληρωμής"):
            show_discount_npv_ui()
    with col2:
        if st.button("🏡 Ανάλυση Δανείου vs Leasing"):
            loan_vs_leasing_ui()
        if st.button("⚖️ Μέσο Κόστος Παραγωγής Ανά Μονάδα"):
            show_unit_cost_app()
        if st.button("📦 Οικονομικότερη Παραγγελία Εμπορευμάτων"):
            show_economic_order_quantity()

with tabs[1]:  # Διαχείριση Πίστωσης
    st.subheader("Διαχείριση Πίστωσης")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🕒 Ανάλυση Αύξησης Πίστωσης"):
            show_credit_extension_analysis()
        if st.button("🏛️ Ανάλυση Πολιτικής Πίστωσης"):
            show_credit_policy_analysis()
        if st.button("🏦 Ανάλυση Έκπτωσης Πληρωμής Προμηθευτών"):
            show_supplier_credit_analysis()
    with col2:
        if st.button("⚖️ Μεσοσταθμικός Υπολογισμός Ημερών Πίστωσης"):
            show_credit_days_calculator()
        if st.button("📉 Όριο Απώλειας Πωλήσεων"):
            show_loss_threshold_before_price_cut()

with tabs[2]:  # Διαχείριση Αποθεμάτων
    st.subheader("Διαχείριση Αποθεμάτων")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Ταχύτητα Κυκλοφορίας Αποθεμάτων"):
            show_inventory_turnover_calculator()
    with col2:
        if st.button("📊 Μέσος Ταμειακός Κύκλος"):
            run_cash_cycle_app()

with tabs[3]:  # CLV / Πελάτες
    st.subheader("CLV / Ανάλυση Πελατών")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👥 CLV - Αξία Πελάτη"):
            show_clv_calculator()
    with col2:
        if st.button("🔄 Ανάλυση Υποκατάστασης Προϊόντων"):
            show_substitution_analysis()
        if st.button("➕ Ανάλυση Συμπληρωματικών Προϊόντων"):
            show_complementary_analysis()

with tabs[4]:  # Άλλα Εργαλεία
    st.subheader("Άλλα Εργαλεία")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏛️ Άλλα εργαλεία"):
            st.info("Προσθέστε εδώ τυχόν άλλα εργαλεία ή μελλοντικές εφαρμογές")

