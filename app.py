import streamlit as st

# --- Εισαγωγή modules ---
from home_redesign import show_home_redesign
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

# --- Ρυθμίσεις σελίδας ---
st.set_page_config(page_title="Managers’ Club", page_icon="📊", layout="centered")

# --- State για navigation ---
if 'selected_tool' not in st.session_state:
    st.session_state.selected_tool = '🏠 Αρχική'

# --- Ορισμός εργαλείων ---
tools = {
    "🏠 Αρχική": lambda: show_home_redesign(st.session_state),
    "🟢 Νεκρό Σημείο (Break-Even)": show_break_even_calculator,
    "⚙️ Αλλαγή Νεκρού Σημείου (Τιμή / Κόστος / Επένδυση)": show_break_even_shift_calculator,
    "👥 CLV - Αξία Πελάτη": show_clv_calculator,
    "🔄 Ανάλυση Υποκατάστασης Προϊόντων": show_substitution_analysis,
    "➕ Ανάλυση Συμπληρωματικών Προϊόντων": show_complementary_analysis,
    "📉 Όριο Απώλειας Πωλήσεων πριν τη Μείωση Τιμών": show_loss_threshold_before_price_cut,
    "🕒 Ανάλυση Αύξησης Πί
