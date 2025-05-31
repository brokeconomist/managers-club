import streamlit as st
from utils import format_number_gr, parse_gr_number

def calculate_max_product_A_sales_drop(
    old_price,
    price_increase_absolute,
    profit_A,
    profit_B,
    profit_C,
    profit_D,
    percent_B,
    percent_C,
    percent_D
):
    """
    Επιστρέφει το εκτιμώμενο μέγιστο % μείωσης των πωλήσεων του Προϊόντος Α
    ώστε το συνολικό κέρδος να μην μειωθεί, με ακρίβεια ποσοστού (π.χ. -31.00).
    """
    benefit_substitutes = (
        percent_B * profit_B +
        percent_C * profit_C +
        percent_D * profit_D
    )

    denominator = ((profit_A - benefit_substitutes) / old_price) + price_increase_absolute
    numerator = -price_increase_absolute

    try:
        max_sales_drop_decimal = numerator / denominator
        max_sales_drop_percent = max_sales_drop_decimal * 100
        return max_sales_drop_percent
    except ZeroDivisionError:
        return None

import streamlit as st
from utils import format_number_gr, parse_gr_number

def show_complementary_analysis():
    st.header("➕ Ανάλυση Συμπληρωματικών Προϊόντων")
    st.markdown("""
    Υπολογίστε τη μέγιστη επιτρεπτή μείωση των πωλήσεων ενός προϊόντος μετά από αύξηση τιμής, 
    με βάση τα κέρδη από συμπληρωματικά προϊόντα.
    """)

    with st.form("complementary_form"):
        st.subheader("🔢 Εισαγωγή Δεδομένων")

        col1, col2 = st.columns(2)

        with col1:
            old_price = st.text_input("Αρχική Τιμή Προϊόντος A (€)", value=format_number_gr(10.0))
            price_increase = st.text_input("Αύξηση Τιμής Προϊόντος A (€)", value=format_number_gr(0.10))
            profit_A = st.text_input("Κέρδος ανά τεμάχιο Προϊόντος A (€)", value=format_number_gr(3.0))
            profit_B = st.text_input("Κέρδος ανά τεμάχιο Προϊόντος B (€)", value=format_number_gr(2.5))
            percent_B = st.text_input("Ποσοστό πελατών που αγοράζουν και το B", value="0.40")

        with col2:
            profit_C = st.text_input("Κέρδος ανά τεμάχιο Προϊόντος C (€)", value=format_number_gr(1.5))
            profit_D = st.text_input("Κέρδος ανά τεμάχιο Προϊόντος D (€)", value=format_number_gr(1.0))
            percent_C = st.text_input("Ποσοστό πελατών που αγοράζουν και το C", value="0.30")
            percent_D = st.text_input("Ποσοστό πελατών που αγοράζουν και το D", value="0.20")

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        inputs = [old_price, price_increase, profit_A, profit_B, profit_C, profit_D, percent_B, percent_C, percent_D]
        parsed_inputs = [parse_gr_number(x) for x in inputs]

        if None in parsed_inputs:
            st.error("⚠️ Έλεγξε ότι όλα τα πεδία είναι σωστά συμπληρωμένα.")
            return

        (
            old_price_val,
            price_increase_val,
            profit_A_val,
            profit_B_val,
            profit_C_val,
            profit_D_val,
            percent_B_val,
            percent_C_val,
            percent_D_val
        ) = parsed_inputs

        result = calculate_max_product_A_sales_drop(
            old_price_val,
            price_increase_val,
            profit_A_val,
            profit_B_val,
            profit_C_val,
            profit_D_val,
            percent_B_val,
            percent_C_val,
            percent_D_val
        )

        if result is None:
            st.error("⚠️ Προέκυψε διαίρεση με το μηδέν. Έλεγξε τα κέρδη και την τιμή.")
        else:
            st.success(f"✅ Μέγιστη επιτρεπτή μείωση πωλήσεων Προϊόντος A: {result:.2f}%")

    st.markdown("---")
