import streamlit as st
from utils import format_number_gr, parse_gr_number, format_percentage_gr

# Τίτλος
st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

st.markdown("Αξιολόγηση αν συμφέρει η προσφορά έκπτωσης έναντι είσπραξης σε μεταγενέστερη ημερομηνία.")

# Είσοδοι
col1, col2 = st.columns(2)

with col1:
    sales = st.number_input("Πωλήσεις (€)", value=100000, step=1000, format="%.2f")
    credit_days = st.number_input("Ημέρες Πίστωσης (π.χ. 60)", value=60, step=1)
    discount_days = st.number_input("Ημέρες είσπραξης με έκπτωση (π.χ. 10)", value=10, step=1)

with col2:
    discount_pct = st.number_input("Ποσοστό Έκπτωσης (%)", value=3.0, step=0.1, format="%.2f")
    wacc_pct = st.number_input("Ετήσιο Κόστος Κεφαλαίου (WACC) (%)", value=12.0, step=0.1, format="%.2f")

# Υπολογισμοί
amount_received = sales * (1 - discount_pct / 100)
capital_released = sales - amount_received
days_saved = credit_days - discount_days

# Ετήσια απόδοση έκπτωσης
if capital_released > 0 and days_saved > 0:
    annualized_return = (capital_released / amount_received) * (365 / days_saved) * 100
else:
    annualized_return = 0

# Απόφαση
decision = "✅ Συμφέρει να δώσεις την έκπτωση." if annualized_return > wacc_pct else "❌ Δεν συμφέρει."

# Αποτελέσματα
st.subheader("Αποτελέσματα:")

col1, col2 = st.columns(2)

with col1:
    st.metric("Ποσό που λαμβάνεται", format_number_gr(amount_received) + " €")
    st.metric("Αποδέσμευση Κεφαλαίου", format_number_gr(capital_released) + " €")

with col2:
    st.metric("Ετήσια Απόδοση Έκπτωσης", format_percentage_gr(annualized_return))
    st.metric("WACC", format_percentage_gr(wacc_pct))

st.markdown("---")
st.subheader("Αξιολόγηση:")
st.success(decision) if annualized_return > wacc_pct else st.error(decision)
