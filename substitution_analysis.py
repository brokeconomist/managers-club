import streamlit as st
from utils import format_number_gr, parse_gr_number

def show_substitution_analysis():
    st.header("🔄 Ανάλυση Υποκατάστασης Προϊόντων")
    st.markdown("""
    Αναλύστε την επίδραση μιας αλλαγής τιμής ή πωλήσεων σε ένα προϊόν που ανταγωνίζεται άλλο προϊόν.
    """)

    with st.form("substitution_form"):
        col1, col2 = st.columns(2)

        with col1:
            price_product_a = st.text_input("Τιμή Προϊόντος A (€)", value=format_number_gr(10.0))
            sales_product_a = st.text_input("Πωλήσεις Προϊόντος A (τεμάχια)", value=format_number_gr(1000))

        with col2:
            price_product_b = st.text_input("Τιμή Προϊόντος B (€)", value=format_number_gr(12.0))
            sales_product_b = st.text_input("Πωλήσεις Προϊόντος B (τεμάχια)", value=format_number_gr(800))

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        p_a = parse_gr_number(price_product_a)
        s_a = parse_gr_number(sales_product_a)
        p_b = parse_gr_number(price_product_b)
        s_b = parse_gr_number(sales_product_b)

        if None in (p_a, s_a, p_b, s_b):
            st.error("⚠️ Έλεγξε ότι όλα τα πεδία είναι σωστά συμπληρωμένα.")
            return

        # Παράδειγμα απλού υπολογισμού: ποσοστό μετατόπισης πωλήσεων
        substitution_ratio = (s_b / s_a) * 100 if s_a != 0 else 0

        st.success(f"✅ Ποσοστό Υποκατάστασης: {substitution_ratio:.2f}%")

    st.markdown("---")
