import streamlit as st
from utils import format_percentage_gr

def calculate_required_sales_increase(
    price_per_unit_A,
    profit_per_unit_A,
    profit_per_unit_B,
    profit_per_unit_C,
    percent_B,
    percent_C,
    price_reduction_pct
):
    price_reduction = price_reduction_pct / 100
    total_supplement_profit = (profit_per_unit_B * percent_B / 100) + (profit_per_unit_C * percent_C / 100)
    denominator = ((profit_per_unit_A + total_supplement_profit) / price_per_unit_A) + price_reduction

    if denominator == 0:
        return None

    required_sales_increase = -price_reduction / denominator
    return required_sales_increase * 100

def show_complementary_analysis():
    st.header("➕ Ανάλυση Συμπληρωματικών Προϊόντων")
    st.markdown("**Πόση αύξηση πωλήσεων χρειάζεσαι για να αντισταθμίσεις μια μείωση τιμής;**")

    with st.form("complementary_form"):
        col1, col2 = st.columns(2)
        with col1:
            price_per_unit_A = st.number_input("Τιμή ανά μονάδα προϊόντος Α (€)", value=100.0, min_value=0.0)
            profit_per_unit_A = st.number_input("Κέρδος ανά μονάδα προϊόντος Α (€)", value=30.0, min_value=0.0)
            price_reduction_pct = st.number_input("Μείωση τιμής προϊόντος Α (%)", value=-10.0)

        with col2:
            profit_per_unit_B = st.number_input("Κέρδος ανά μονάδα συμπληρωματικού προϊόντος B (€)", value=5.0, min_value=0.0)
            percent_B = st.number_input("Ποσοστό αγοραστών που αγοράζουν και B (%)", value=30.0, min_value=0.0, max_value=100.0)
            profit_per_unit_C = st.number_input("Κέρδος ανά μονάδα συμπληρωματικού προϊόντος C (€)", value=3.0, min_value=0.0)
            percent_C = st.number_input("Ποσοστό αγοραστών που αγοράζουν και C (%)", value=15.0, min_value=0.0, max_value=100.0)

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        result = calculate_required_sales_increase(
            price_per_unit_A,
            profit_per_unit_A,
            profit_per_unit_B,
            profit_per_unit_C,
            percent_B,
            percent_C,
            price_reduction_pct
        )

        if result is None:
            st.error("⚠️ Δεν μπορεί να υπολογιστεί. Έλεγξε τις τιμές.")
        else:
            st.success(f"✅ Ελάχιστη Απαιτούμενη Αύξηση Πωλήσεων στο Προϊόν Α: {format_percentage_gr(result)}")

    st.markdown("---")
