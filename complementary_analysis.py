import streamlit as st
from utils.number_formatting import format_percentage_gr


def calculate_required_sales_increase(
    price_per_unit_A,
    profit_per_unit_A,
    profit_per_unit_B,
    profit_per_unit_C,
    percent_B,
    percent_C,
    price_reduction_pct
):
    """
    Υπολογίζει την ελάχιστη αύξηση πωλήσεων που απαιτείται μετά από μείωση τιμής,
    ώστε να διατηρηθεί το ίδιο συνολικό κέρδος, λαμβάνοντας υπόψη τα συμπληρωματικά προϊόντα.
    """
    price_reduction = price_reduction_pct / 100  # π.χ. -10 -> -0.10

    total_supplement_profit = (
        profit_per_unit_B * percent_B / 100 +
        profit_per_unit_C * percent_C / 100
    )

    denominator = ((profit_per_unit_A + total_supplement_profit) / price_per_unit_A) + price_reduction

    if denominator == 0:
        return None

    required_sales_increase = -price_reduction / denominator
    return required_sales_increase * 100


def show_complementary_analysis():
    st.header("📈 Ανάλυση Συμπληρωματικών Προϊόντων")
    st.markdown("### 🎯 Στόχος: Υπολόγισε πόσο πρέπει να αυξηθούν οι πωλήσεις του κύριου προϊόντος σου, μετά από μείωση τιμής, ώστε να διατηρηθεί το συνολικό κέρδος.")

    with st.form("complementary_form"):
        col1, col2 = st.columns(2)

        with col1:
            price_A = st.number_input("Τιμή Προϊόντος Α (€)", min_value=0.01, format="%.2f")
            profit_A = st.number_input("Κέρδος ανά μονάδα Προϊόντος Α (€)", format="%.2f")
            price_reduction_pct = st.number_input("Ποσοστό Μείωσης Τιμής (%)", format="%.2f")

        with col2:
            profit_B = st.number_input("Κέρδος ανά μονάδα Συμπληρωματικού Β (€)", format="%.2f")
            percent_B = st.number_input("Ποσοστό πελατών που αγοράζουν και το Β (%)", min_value=0.0, max_value=100.0, format="%.1f")
            profit_C = st.number_input("Κέρδος ανά μονάδα Συμπληρωματικού Γ (€)", format="%.2f")
            percent_C = st.number_input("Ποσοστό πελατών που αγοράζουν και το Γ (%)", min_value=0.0, max_value=100.0, format="%.1f")

        submitted = st.form_submit_button("📊 Υπολογισμός")

    if submitted:
        result = calculate_required_sales_increase(
            price_A,
            profit_A,
            profit_B,
            profit_C,
            percent_B,
            percent_C,
            price_reduction_pct
        )

        if result is None:
            st.error("⚠️ Δεν μπορεί να υπολογιστεί. Έλεγξε τις τιμές (π.χ. μηδενικό κόστος ή τιμή).")
        else:
            st.success(f"✅ Ελάχιστη Απαιτούμενη Αύξηση Πωλήσεων στο Προϊόν Α: {format_percentage_gr(result)}")

    st.markdown("---")
