import streamlit as st

# Import όλων των modules
from home import show_home
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

# Ρυθμίσεις σελίδας
st.set_page_config(page_title="Managers’ Club", page_icon="📊", layout="wide")

# Λεξικό εργαλείων
tools = {
    "🟢 Νεκρό Σημείο (Break-Even)": show_break_even_calculator,
    "⚙️ Αλλαγή Νεκρού Σημείου": show_break_even_shift_calculator,
    "👥 CLV - Αξία Πελάτη": show_clv_calculator,
    "🔄 Ανάλυση Υποκατάστασης Προϊόντων": show_substitution_analysis,
    "➕ Ανάλυση Συμπληρωματικών Προϊόντων": show_complementary_analysis,
    "📉 Όριο Απώλειας Πωλήσεων": show_loss_threshold_before_price_cut,
    "🕒 Ανάλυση Αύξησης Πίστωσης": show_credit_extension_analysis,
    "🏛️ Ανάλυση Πολιτικής Πίστωσης": show_credit_policy_analysis,
    "🏦 Ανάλυση Έκπτωσης Πληρωμής Προμηθευτών": show_supplier_credit_analysis,
    "📊 Μέσος Ταμειακός Κύκλος": run_cash_cycle_app,
    "🏡 Δάνειο vs Leasing": loan_vs_leasing_ui,
    "📈 Μικτό Κέρδος": show_gross_profit_template,
    "📦 Παραγγελία Εμπορευμάτων": show_economic_order_quantity,
    "⚖️ Κόστος Ανά Μονάδα": show_unit_cost_app,
    "💰 NPV για Έκπτωση Πληρωμής": show_discount_npv_ui,
    "⚖️ Ημέρες Πίστωσης": show_credit_days_calculator,
    "🔁 Ταχύτητα Κυκλοφορίας Αποθεμάτων": show_inventory_turnover_calculator,
}

# Sidebar με επιλογή εργαλείου
st.sidebar.title("📊 Managers’ Club - Επιλογή Εργαλείου")
selected_tool = st.sidebar.radio("🧰 Επιλέξτε εργαλείο", ["🏠 Αρχική"] + list(tools.keys()))

# Αν είμαστε στην Αρχική
if selected_tool == "🏠 Αρχική":
    st.title("Καλώς ήρθατε στο Managers’ Club 📊")
    st.write("""
        Το Managers’ Club συγκεντρώνει όλα τα χρηματοοικονομικά εργαλεία σας σε ένα μέρος.
        Επιλέξτε ένα εργαλείο από τα παρακάτω ή δείτε οδηγούς, συμβουλές και tutorials.
    """)

    st.subheader("Εργαλεία")
    cols = st.columns(3)
    i = 0
    for name, func in tools.items():
        with cols[i % 3]:
            if st.button(name, key=name):
                func()
        i += 1

    st.subheader("Επικοινωνία / Υποστήριξη")
    st.write("📧 Email: info@managersclub.gr")
    st.write("🌐 Blog / Οδηγοί: [Medium](https://medium.com/@brokeconomist)")
    st.write("💬 Social Media: [Facebook](https://www.facebook.com/brokeconomist) | [LinkedIn](https://www.linkedin.com/in/brokeconomist)")

else:
    # Εμφάνιση επιλεγμένου εργαλείου
    tools[selected_tool]()
