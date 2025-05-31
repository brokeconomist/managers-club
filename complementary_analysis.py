import streamlit as st
from utils.number_formatting import format_percentage_gr

def calculate_required_sales_increase(
    price_A,
    profit_A,
    profit_B,
    profit_C,
    percent_B,
    percent_C,
    price_change_pct
):
    """
    Υπολογίζει την ελάχιστη αύξηση πωλήσεων που απαιτείται μετά από αλλαγή τιμής
    ώστε να διατηρηθεί το ίδιο συνολικό κέρδος, λαμβάνοντας υπόψη τα συμπληρωματικά προϊόντα.
    """
    # Μετατροπή ποσοστών σε δεκαδικά
    percent_B /= 100
    percent_C /= 100
    price_change = price_A * price_change_pct / 100  # π.χ. +10% = +τιμή σε €

    numerator = -price_change

    # Προσαρμοσμένο κέρδος λαμβάνοντας υπόψη ποσοστά πελατών και κέρδη από Β και Γ
    adjusted_profit = profit_A - (percent_B * profit_B + percent_C * profit_C)

    denominator = (adjusted_profit / price_A) + (price_change_pct / 100)

    try:
        result_pct = numerator / denominator * 100  # ποσοστό αύξησης πωλήσεων
        return result_pct
    except ZeroDivisionError:
        return None


def show_complementary_analysis():
    st.title("➕ Ανάλυση Συμπληρωματικών Προϊόντων")

    price_A = st.number_input("Τιμή προϊόντος Α (€)", min_value=0.01, format="%.2f")
    profit_A = st.number_input("Κέρδος ανά μονάδα προϊόντος Α (€)", min_value=0.0, format="%.2f")

    profit_B = st.number_input("Κέρδος ανά μονάδα προϊόντος Β (€)", min_value=0.0, format="%.2f")
    profit_C = st.number_input("Κέρδος ανά μονάδα προϊόντος Γ (€)", min_value=0.0, format="%.2f")

    percent_B = st.number_input("Ποσοστό πελατών που αγοράζουν προϊόν Β (%)", min_value=0.0, max_value=100.0, format="%.2f")
    percent_C = st.number_input("Ποσοστό πελατών που αγοράζουν προϊόν Γ (%)", min_value=0.0, max_value=100.0, format="%.2f")

    price_change_pct = st.number_input("Αύξηση Τιμής Προϊόντος Α (%)", format="%.2f")

    if st.button("Υπολόγισε Ελάχιστη Αύξηση Πωλήσεων"):
        result = calculate_required_sales_increase(
            price_A,
            profit_A,
            profit_B,
            profit_C,
            percent_B,
            percent_C,
            price_change_pct
        )
        if result is None:
            st.error("⚠️ Δεν μπορεί να υπολογιστεί. Έλεγξε τις τιμές.")
        else:
            st.success(f"✅ Ελάχιστη Απαιτούμενη Αύξηση Πωλήσεων στο Προϊόν Α: {format_percentage_gr(result)}")

    st.markdown("---")
