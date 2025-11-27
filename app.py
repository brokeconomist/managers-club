import streamlit as st

# Εδώ κάνουμε import όλα τα εργαλεία όπως στο app.py
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

# Λεξικό εργαλείων για εύκολη αναφορά
tools = {
    "🟢 Νεκρό Σημείο (Break-Even)": show_break_even_calculator,
    "⚙️ Αλλαγή Νεκρού Σημείου (Τιμή / Κόστος / Επένδυση)": show_break_even_shift_calculator,
    "👥 CLV - Αξία Πελάτη": show_clv_calculator,
    "🔄 Ανάλυση Υποκατάστασης Προϊόντων": show_substitution_analysis,
    "➕ Ανάλυση Συμπληρωματικών Προϊόντων": show_complementary_analysis,
    "📉 Όριο Απώλειας Πωλήσεων πριν τη Μείωση Τιμών": show_loss_threshold_before_price_cut,
    "🕒 Ανάλυση Αύξησης Πίστωσης": show_credit_extension_analysis,
    "🏛️ Ανάλυση Πολιτικής Πίστωσης": show_credit_policy_analysis,
    "🏦 Ανάλυση Έκπτωσης Πληρωμής Προμηθευτών Τοις Μετρητοίς": show_supplier_credit_analysis,
    "📊 Μέσος Ταμειακός Κύκλος": run_cash_cycle_app,
    "🏡 Ανάλυση Δανείου vs Leasing": loan_vs_leasing_ui,
    "📈 Υπολογισμός Μικτού Κέρδους": show_gross_profit_template,
    "📦 Οικονομικότερη Παραγγελία Εμπορευμάτων": show_economic_order_quantity,
    "⚖️ Μέσο Κόστος Παραγωγής Ανά Μονάδα": show_unit_cost_app,
    "💰 Ανάλυση NPV Για Έκπτωση Πληρωμής Τοις Μετρητοίς": show_discount_npv_ui,
    "🏛️ Μεσοσταθμικός Υπολογισμός Ημερών Πίστωσης": show_credit_days_calculator,
    "🔁 Ταχύτητα Κυκλοφορίας Αποθεμάτων (ποσότητα/αξία)": show_inventory_turnover_calculator,
}

# Περιγραφές εργαλείων για την αρχική σελίδα
tool_descriptions = {
    "🟢 Νεκρό Σημείο (Break-Even)": "Υπολογισμός σημείου ισορροπίας πωλήσεων / κόστους.",
    "⚙️ Αλλαγή Νεκρού Σημείου (Τιμή / Κόστος / Επένδυση)": "Δείτε πώς μεταβάλλεται το Νεκρό Σημείο με αλλαγές τιμής, κόστους ή επένδυσης.",
    "👥 CLV - Αξία Πελάτη": "Υπολογισμός μακροχρόνιας αξίας πελάτη.",
    "🔄 Ανάλυση Υποκατάστασης Προϊόντων": "Προσομοιώστε τον αντίκτυπο υποκατάστασης προϊόντων στις πωλήσεις.",
    "➕ Ανάλυση Συμπληρωματικών Προϊόντων": "Δείτε πώς τα συμπληρωματικά προϊόντα επηρεάζουν τα κέρδη σας.",
    "📉 Όριο Απώλειας Πωλήσεων πριν τη Μείωση Τιμών": "Υπολογίστε πόση απώλεια πωλήσεων μπορείτε να αντέξετε πριν μειώσετε τιμές.",
    "🕒 Ανάλυση Αύξησης Πίστωσης": "Αξιολογήστε την επίδραση της αύξησης πιστωτικών ορίων στους πελάτες σας.",
