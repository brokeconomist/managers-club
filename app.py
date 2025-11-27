import streamlit as st

# ----------------------------
# IMPORT ΕΡΓΑΛΕΙΩΝ
# ----------------------------
from break_even_calculator import run as run_break_even
from break_even_shift_calculator import run as run_break_even_shift
from clv_calculator import run as run_clv
from substitution_analysis import run as run_substitution
from complementary_analysis import run as run_complementary
from credit_policy_app import run as run_credit_policy
from credit_extension_app import run as run_credit_extension
from supplier_credit_app import run as run_supplier_credit
from discount_npv_ui import run as run_discount_npv
from cash_cycle import run as run_cash_cycle
from gross_profit_analysis import run as run_gross_profit
from economic_order_quantity import run as run_eoq
from loan_vs_leasing_calculator import run as run_loan_leasing
from unit_cost_app import run as run_unit_cost
from credit_days_calculator import run as run_credit_days  # placeholder

# ----------------------------
# WELCOME SECTION
# ----------------------------
st.title("🎯 Καλωσόρισες στο Managers’ Club!")
st.write("Το έξυπνο εργαλείο για σύγχρονες και τεκμηριωμένες οικονομικές αποφάσεις")
st.write("""
Το Managers’ Club είναι μια διαδικτυακή πλατφόρμα που σου δίνει τη δυνατότητα να κάνεις πιο γρήγορα, 
ξεκάθαρα και τεκμηριωμένα οικονομικές επιλογές για την επιχείρησή σου.

Δεν χρειάζεσαι πολύπλοκα φύλλα Excel, όλα τα εργαλεία είναι στη διάθεσή σου με ελληνικό περιβάλλον και απλές ερωτήσεις.
""")

st.write("---")

# ----------------------------
# TOOLS HUB (SHORTCUTS)
# ----------------------------
st.header("📌 Τι μπορείς να κάνεις εδώ:")

tools = [
    {"title": "Υπολογισμός Νεκρού Σημείου (Break-Even)", "func": run_break_even, "icon": "📈"},
    {"title": "Μεταβολή Νεκρού Σημείου (Τιμή/Κόστος/Επένδυση)", "func": run_break_even_shift, "icon": "🔄"},
    {"title": "Ανάλυση Αξίας Πελάτη (CLV)", "func": run_clv, "icon": "💰"},
    {"title": "Ανάλυση Υποκατάστασης Προϊόντων", "func": run_substitution, "icon": "⚖️"},
    {"title": "Ανάλυση Συμπληρωματικών Προϊόντων", "func": run_complementary, "icon": "🧩"},
    {"title": "Μέγιστη Επιτρεπτή Μεταβολή Τιμών", "func": run_credit_policy, "icon": "📊"},
    {"title": "Αποδοτικότητα Αλλαγής Πιστωτικής Πολιτικής", "func": run_credit_extension, "icon": "💳"},
    {"title": "Διαχείριση πληρωμών σε προμηθευτές", "func": run_supplier_credit, "icon": "🏦"},
    {"title": "Απόδοση για έκπτωση και πληρωμές τοις μετρητοίς", "func": run_discount_npv, "icon": "💵"},
    {"title": "Υπολογισμός Ταμειακού Κύκλου", "func": run_cash_cycle, "icon": "🔁"},
    {"title": "Εκτίμηση μικτού κέρδους", "func": run_gross_profit, "icon": "📉"},
    {"title": "Οικονομικότερη Παραγγελία Εμπορευμάτων (EOQ)", "func": run_eoq, "icon": "📦"},
    {"title": "Κόστος Δανείου ή Leasing", "func": run_loan_leasing, "icon": "🏁"},
    {"title": "Μέσο Κόστος Παραγωγής ανά Μονάδα", "func": run_unit_cost, "icon": "🏭"},
    {"title": "Χρηματοδοτικές Ανάγκες & Ρευστότητα", "func": run_credit_days, "icon": "💡"},
]

# Δύο στήλες για compact view
cols = st.columns(2)

for i, tool in enumerate(tools):
    col = cols[i % 2]
    with col:
        st.markdown(f"{tool['icon']} **{tool['title']}**")
        if st.button("Άνοιγμα →", key=tool["title"]):
            st.session_state["active_tool"] = tool["title"]
            st.session_state["active_func"] = tool["func"]

# ----------------------------
# Εμφάνιση εργαλείου κάτω από τα κουμπιά
# ----------------------------
if "active_func" in st.session_state:
    st.write("---")
    st.subheader(f"Εργαλείο: {st.session_state['active_tool']}")
    st.session_state["active_func"]()  # τρέχει το εργαλείο

st.write("---")

# ----------------------------
# ΟΔΗΓΙΕΣ ΧΡΗΣΗΣ
# ----------------------------
st.subheader("🧭 Πώς να ξεκινήσεις:")
st.write("""
1. Διάλεξε εργαλείο από τα παραπάνω κουμπιά ή από το μενού στα αριστερά.
2. Συμπλήρωσε τα πεδία με τα δικά σου δεδομένα.
3. Δες άμεσα αριθμούς, γραφήματα και συμπεράσματα.
""")
st.write("📘 Θες βοήθεια ή παράδειγμα;")
st.write("📄 Δες ένα demo παράδειγμα χρήσης (Excel) (Έρχεται σύντομα)")
st.write("🧑‍🏫 Οδηγός: Πώς χρησιμοποιώ τα εργαλεία (PDF) (Έρχεται σύντομα)")

# ----------------------------
# ΕΠΙΚΟΙΝΩΝΙΑ
# ----------------------------
st.subheader("📬 Επικοινώνησε μαζί μας")
st.write("Αν έχεις ερωτήσεις, ιδέες ή θέλεις να συνεργαστούμε, στείλε email στο:")
st.write("✉️ managersclub2025@gmail.com")

st.write("---")
st.write("🚀 Έτοιμος να πάρεις τον έλεγχο στα χέρια σου;")
st.write("👉 Ξεκίνα από τα κουμπιά παραπάνω ή από το sidebar και δες τις δυνατότητες του Managers’ Club στην πράξη.")
