import streamlit as st
from utils import format_number_gr, parse_gr_number

def show_complementary_product_analysis():
    st.header("➕ Ανάλυση Συμπληρωματικών Προϊόντων")
    st.markdown("""
    Αναλύστε πώς η αύξηση ή μείωση πωλήσεων ενός προϊόντος επηρεάζει την πώληση συμπληρωματικών προϊόντων.
    """)

    with st.form("complementary_form"):
        col1, col2 = st.columns(2)

        with col1:
            sales_main_product = st.text_input("Πωλήσεις Κύριου Προϊόντος (τεμάχια)", value=format_number_gr(1000))
            sales_comp_product = st.text_input("Πωλήσεις Συμπληρωματικού Προϊόντος (τεμάχια)", value=format_number_gr(500))

        with col2:
            change_main_product = st.text_input("Αλλαγή πωλήσεων κύριου προϊόντος (%)", value="10")

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        s_main = parse_gr_number(sales_main_product)
        s_comp = parse_gr_number(sales_comp_product)
        ch_main = parse_gr_number(change_main_product)

        if None in (s_main, s_comp, ch_main):
            st.error("⚠️ Έλεγξε ότι όλα τα πεδία είναι σωστά συμπληρωμένα.")
            return

        # Παράδειγμα απλού υπολογισμού: προβλεπόμενη αλλαγή συμπληρωματικών πωλήσεων
        predicted_comp_change = s_comp * (ch_main / 100)

        st.success(f"✅ Προβλεπόμενη αλλαγή πωλήσεων συμπληρωματικού προϊόντος: {predicted_comp_change:.2f} τεμάχια")

    st.markdown("---")
