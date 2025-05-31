import streamlit as st
from utils import format_percentage_gr

def calculate_required_sales_increase(
    price_A,
    profit_A,
    profit_B,
    profit_C,
    profit_D,
    percent_B,
    percent_C,
    percent_D,
    price_reduction_pct  # π.χ. -10 για μείωση 10%
):
    # Μετατροπή ποσοστών σε δεκαδικά
    percent_B /= 100
    percent_C /= 100
    percent_D /= 100

    price_reduction = price_reduction_pct / 100  # πχ -10% -> -0.10

    total_supplement_profit = (
        profit_B * percent_B +
        profit_C * percent_C +
        profit_D * percent_D
    )

    denominator = ((profit_A + total_supplement_profit) / price_A) + price_reduction

    if denominator == 0:
        return None

    required_increase = -price_reduction / denominator

    return required_increase * 100  # Επιστρέφει ποσοστό %

def show_complementary_analysis():
    st.title("➕ Ανάλυση Συμπληρωματικών Προϊόντων")

    price_A = st.number_input("Τιμή προϊόντος Α (€)", min_value=0.01, format="%.2f")
    profit_A = st.number_input("Κέρδος ανά μονάδα προϊόντος Α (€)", min_value=0.0, format="%.2f")

    profit_B = st.number_input("Κέρδος ανά μονάδα προϊόντος Β (€)", min_value=0.0, format="%.2f")
    profit_C = st.number_input("Κέρδος ανά μονάδα προϊόντος Γ (€)", min_value=0.0, format="%.2f")
    profit_D = st.number_input("Κέρδος ανά μονάδα προϊόντος Δ (€)", min_value=0.0, format="%.2f")

    percent_B = st.number_input("Ποσοστό πελατών που αγοράζουν προϊόν Β (%)", min_value=0.0, max_value=100.0, format="%.2f")
    percent_C = st.number_input("Ποσοστό πελατών που αγοράζουν προϊόν Γ (%)", min_value=0.0, max_value=100.0, format="%.2f")
    percent_D = st.number_input("Ποσοστό πελατών που αγοράζουν προϊόν Δ (%)", min_value=0.0, max_value=100.0, format="%.2f")

    # Εδώ δίνουμε μόνο αρνητικές τιμές για μείωση τιμής από 0% έως -100%
    price_reduction_pct = st.number_input("Μείωση Τιμής Προϊόντος Α (%)", min_value=-100.0, max_value=0.0, format="%.2f")

    if st.button("Υπολόγισε Ελάχιστη Αύξηση Πωλήσεων"):
        st.write(f"DEBUG: price_reduction_pct = {price_reduction_pct}")  # debug
        result = calculate_required_sales_increase(
            price_A,
            profit_A,
            profit_B,
            profit_C,
            profit_D,
            percent_B,
            percent_C,
            percent_D,
            price_reduction_pct
        )
        if result is None:
            st.error("⚠️ Δεν μπορεί να υπολογιστεί. Έλεγξε τις τιμές.")
        else:
            st.success(f"✅ Ελάχιστη Απαιτούμενη Αύξηση Πωλήσεων στο Προϊόν Α: {format_percentage_gr(result)}")

    st.markdown("---")
