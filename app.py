import streamlit as st

from home import show_home
from break_even_calculator import show_break_even_calculator
from break_even_shift_calculator import show_break_even_shift_calculator
from clv_calculator import show_clv_calculator
from substitution_analysis import show_substitution_analysis
from complementary_analysis import show_complementary_analysis
from loss_threshold import show_loss_threshold_before_price_cut
from credit_extension_analysis import show_credit_extension_analysis
from credit_policy_app import show_credit_policy_analysis
from supplier_credit_app import show_supplier_credit_analysis  # ✅ Νέο
from cash_cycle import run_cash_cycle_app  # ✅ Νέο
from discount_efficiency_app import show_discount_efficiency_app

# Ρυθμίσεις σελίδας
st.set_page_config(page_title="Managers’ Club", page_icon="📊", layout="centered")

# Λεξικό εργαλείων
tools = {
    "🏠 Αρχική": show_home,
    "🟢 Νεκρό Σημείο (Break-Even)": show_break_even_calculator,
    "⚙️ Αλλαγή Νεκρού Σημείου (Τιμή / Κόστος / Επένδυση)": show_break_even_shift_calculator,
    "👥 CLV - Αξία Πελάτη": show_clv_calculator,
    "🔄 Ανάλυση Υποκατάστασης Προϊόντων": show_substitution_analysis,
    "➕ Ανάλυση Συμπληρωματικών Προϊόντων": show_complementary_analysis,
    "📉 Όριο Απώλειας Πωλήσεων πριν τη Μείωση Τιμών": show_loss_threshold_before_price_cut,
    "🕒 Ανάλυση Αύξησης Πίστωσης": show_credit_extension_analysis,
    "🏛️ Ανάλυση Πολιτικής Πίστωσης": show_credit_policy_analysis,
    "🏦 Ανάλυση Πίστωσης Προμηθευτών (Έκπτωση)": show_supplier_credit_analysis,  # ✅ Νέο
    "📊 Ταμειακός Κύκλος": run_cash_cycle_app  # ✅ Νέο
    "💸 Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς": show_discount_efficiency_app
}

# Πλευρικό μενού
st.sidebar.title("📊 Managers’ Club - Επιλογή Εργαλείου")
selected_tool = st.sidebar.radio("🧰 Επιλέξτε εργαλείο", list(tools.keys()))

# Εκτέλεση της επιλεγμένης λειτουργίας
tools[selected_tool]()
