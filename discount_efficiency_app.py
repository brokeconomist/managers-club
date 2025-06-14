from discount_efficiency_logic import calculate_discount_efficiency
import streamlit as st
from utils import format_number_gr, format_percentage_gr

def show_discount_efficiency_app():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    st.markdown("Αξιολόγηση αν συμφέρει η προσφορά έκπτωσης έναντι είσπραξης σε μεταγενέστερη ημερομηνία.")

    # Είσοδοι
    col1, col2 = st.columns(2)

    with col1:
        sales = st.number_input("Πωλήσεις (€)", value=100000.0, step=1000.0, format="%.2f")
        credit_days = st.number_input("Ημέρες Πίστωσης (π.χ. 60)", value=60, step=1)
        discount_days = st.number_input("Ημέρες είσπραξης με έκπτωση (π.χ. 10)", value=10, step=1)

    with col2:
        discount_pct = st.number_input("Ποσοστό Έκπτωσης (%)", value=3.0, step=0.1, format="%.2f")
        wacc_pct = st.number_input("Ετήσιο Κόστος Κεφαλαίου (WACC) (%)", value=12.0, step=0.1, format="%.2f")

    # Υπολογισμοί
    result = calculate_discount_efficiency(sales, credit_days, discount_days, discount_pct, wacc_pct)

    # Αποτελέσματα
    st.subheader("Αποτελέσματα:")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Ποσό που λαμβάνεται", format_number_gr(result['amount_received']) + " €")
        st.metric("Αποδέσμευση Κεφαλαίου", format_number_gr(result['capital_released']) + " €")

    with col2:
        st.metric("Ετήσια Απόδοση Έκπτωσης", format_percentage_gr(result['annualized_return']))
        st.metric("WACC", format_percentage_gr(result['wacc_pct']))

    st.markdown("---")
    st.subheader("Αξιολόγηση:")
    if result['annualized_return'] > result['wacc_pct']:
        st.success("✅ Συμφέρει να δώσεις την έκπτωση.")
    else:
        st.error("❌ Δεν συμφέρει.")
