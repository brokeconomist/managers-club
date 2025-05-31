import streamlit as st
from utils import format_number_gr, parse_gr_number, format_percentage_gr

def calculate_required_sales_increase(
    old_price_A,
    price_decrease_pct,
    profit_A,
    profit_B,
    profit_C,
    profit_D,
    profit_E,
    percent_B,
    percent_C,
    percent_D,
    percent_E
):
    combined_profit = (
        profit_A +
        percent_B * profit_B +
        percent_C * profit_C +
        percent_D * profit_D +
        percent_E * profit_E
    )

    new_price = old_price_A * (1 - price_decrease_pct)
    new_profit = combined_profit - (old_price_A - new_price)

    try:
        required_increase = (old_price_A - new_price) / new_profit
        return required_increase * 100
    except ZeroDivisionError:
        return None

def show_complementary_analysis():
    st.header("📊 Ανάλυση Συμπληρωματικών Προϊόντων (Α–Ε)")
    st.markdown("""
    Το προϊόν Α (π.χ. Κοστούμι) συνοδεύεται συχνά από προϊόντα Β–Ε (π.χ. Πουκάμισο, Γραβάτα κλπ).
    Αν μειωθεί η τιμή του Α, πόσο πρέπει να αυξηθούν οι πωλήσεις του ώστε να διατηρηθεί το συνολικό κέρδος;
    """)

    with st.form("complementary_form"):
        col1, col2 = st.columns(2)

        with col1:
            price_A_input = st.text_input("Τιμή προϊόντος Α (€)", value=format_number_gr(200))
            cost_A_input = st.text_input("Κόστος προϊόντος Α (€)", value=format_number_gr(140))
            price_decrease_input = st.text_input("Μείωση τιμής Α (%)", value=format_number_gr(10))

            profit_B_input = st.text_input("Κέρδος προϊόντος Β (€)", value=format_number_gr(13))
            profit_C_input = st.text_input("Κέρδος προϊόντος Γ (€)", value=format_number_gr(11))

        with col2:
            profit_D_input = st.text_input("Κέρδος προϊόντος Δ (€)", value=format_number_gr(11))
            profit_E_input = st.text_input("Κέρδος προϊόντος Ε (€)", value=format_number_gr(45))

            percent_B = st.slider("% πελατών που αγοράζουν Β", 0.0, 100.0, 90.0) / 100
            percent_C = st.slider("% πελατών που αγοράζουν Γ", 0.0, 100.0, 70.0) / 100
            percent_D = st.slider("% πελατών που αγοράζουν Δ", 0.0, 100.0, 10.0) / 100
            percent_E = st.slider("% πελατών που αγοράζουν Ε", 0.0, 100.0, 5.0) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        price_A = parse_gr_number(price_A_input)
        cost_A = parse_gr_number(cost_A_input)
        price_decrease_pct = parse_gr_number(price_decrease_input) / 100
        profit_A = price_A - cost_A

        profit_B = parse_gr_number(profit_B_input)
        profit_C = parse_gr_number(profit_C_input)
        profit_D = parse_gr_number(profit_D_input)
        profit_E = parse_gr_number(profit_E_input)

        if None in (price_A, cost_A, price_decrease_pct, profit_A,
                    profit_B, profit_C, profit_D, profit_E):
            st.error("❌ Έλεγξε ότι όλα τα αριθμητικά πεδία είναι σωστά.")
            return

        result = calculate_required_sales_increase(
            price_A,
            price_decrease_pct,
            profit_A,
            profit_B,
            profit_C,
            profit_D,
            profit_E,
            percent_B,
            percent_C,
            percent_D,
            percent_E
        )

        if result is None:
            st.error("❌ Δεν μπορεί να υπολογιστεί. Δοκίμασε άλλες τιμές.")
        else:
            st.success(f"✅ Απαιτούμενη αύξηση πωλήσεων προϊόντος Α: {format_percentage_gr(result)}")
