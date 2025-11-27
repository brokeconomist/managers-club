import streamlit as st

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

# Λίστα εργαλείων με icon/emoji όπως στο sidebar
tools = [
    {"title": "Υπολογισμός Νεκρού Σημείου (Break-Even)", "page": "break_even_calculator", "icon": "📈"},
    {"title": "Μεταβολή Νεκρού Σημείου (Τιμή/Κόστος/Επένδυση)", "page": "break_even_shift_calculator", "icon": "🔄"},
    {"title": "Ανάλυση Αξίας Πελάτη (CLV)", "page": "clv_calculator", "icon": "💰"},
    {"title": "Ανάλυση Υποκατάστασης Προϊόντων", "page": "substitution_analysis", "icon": "⚖️"},
    {"title": "Ανάλυση Συμπληρωματικών Προϊόντων", "page": "complementary_analysis", "icon": "🧩"},
    {"title": "Μέγιστη Επιτρεπτή Μεταβολή Τιμών", "page": "credit_policy_app", "icon": "📊"},
    {"title": "Αποδοτικότητα Αλλαγής Πιστωτικής Πολιτικής", "page": "credit_extension_app", "icon": "💳"},
    {"title": "Διαχείριση πληρωμών σε προμηθευτές", "page": "supplier_credit_app", "icon": "🏦"},
    {"title": "Απόδοση για έκπτωση και πληρωμές τοις μετρητοίς", "page": "discount_npv_ui", "icon": "💵"},
    {"title": "Υπολογισμός Ταμειακού Κύκλου", "page": "cash_cycle", "icon": "🔁"},
    {"title": "Εκτίμηση μικτού κέρδους", "page": "gross_profit_analysis", "icon": "📉"},
    {"title": "Οικονομικότερη Παραγγελία Εμπορευμάτων (EOQ)", "page": "economic_order_quantity", "icon": "📦"},
    {"title": "Κόστος Δανείου ή Leasing", "page": "loan_vs_leasing_calculator", "icon": "🏁"},
    {"title": "Μέσο Κόστος Παραγωγής ανά Μονάδα", "page": "unit_cost_app", "icon": "🏭"},
    {"title": "Χρηματοδοτικές Ανάγκες & Ρευστότητα", "page": "credit_days_calculator", "icon": "💡"},  # placeholder
]

# Δύο στήλες για compact view
cols = st.columns(2)

for i, tool in enumerate(tools):
    col = cols[i % 2]
    with col:
        st.markdown(f"{tool['icon']} **{tool['title']}**")
        if st.button("Άνοιγμα →", key=tool["title"]):
            st.session_state["selected_tool"] = tool["page"]

# Redirect σε εργαλείο όταν πατηθεί
if "selected_tool" in st.session_state:
    st.switch_page(st.session_state["selected_tool"])

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
