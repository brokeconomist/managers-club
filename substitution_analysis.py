import streamlit as st
from utils.number_formatting import format_number_gr, parse_gr_number, format_percentage_gr

def calculate_max_product_A_sales_drop(
    price_old,
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

    denominator = ((profit_A - benefit_substitutes) / price_old) + price_increase_absolute
    numerator = -price_increase_absolute

    try:
        max_sales_drop_decimal = numerator / denominator
        max_sales_drop_percent = max_sales_drop_decimal * 100
        return max_sales_drop_percent
    except ZeroDivisionError:
        return None

def show_substitution_max_drop():
    st.header("📉 Μέγιστη Αποδεκτή Μείωση Πωλήσεων Προϊόντος Α λόγω Αύξησης Τιμής")
    st.title("Τι θα γίνει αν οι πελάτες προτιμήσουν άλλο προϊόν μου; 🔄")
    st.markdown("""
    Αν αυξήσετε την τιμή ενός προϊόντος και κάποιοι πελάτες στραφούν σε άλλα δικά σας υποκατάστατα,
    αυτό το εργαλείο υπολογίζει πόσο μπορούν να μειωθούν οι πωλήσεις του ακριβότερου προϊόντος χωρίς να χαθεί συνολικό κέρδος.
    """)

    with st.form("substitution_max_drop_form"):
        col1, col2 = st.columns(2)

        with col1:
            price_old_input = st.text_input("Αρχική Τιμή Προϊόντος Α (€)", value=format_number_gr(1.50))
            price_increase_pct_input = st.text_input("Αύξηση Τιμής Προϊόντος Α (%)", value=format_number_gr(5.0))
            profit_A_input = st.text_input("Κέρδος Προϊόντος Α ανά μονάδα (€)", value=format_number_gr(0.30))

        with col2:
            profit_B_input = st.text_input("Κέρδος Προϊόντος Β ανά μονάδα (€)", value=format_number_gr(0.20))
            profit_C_input = st.text_input("Κέρδος Προϊόντος Γ ανά μονάδα (€)", value=format_number_gr(0.20))
            profit_D_input = st.text_input("Κέρδος Προϊόντος Δ ανά μονάδα (€)", value=format_number_gr(0.05))

        percent_B = st.slider("Ποσοστό πελατών προς Προϊόν Β (%)", 0.0, 100.0, 45.0) / 100
        percent_C = st.slider("Ποσοστό πελατών προς Προϊόν Γ (%)", 0.0, 100.0, 20.0) / 100
        percent_D = st.slider("Ποσοστό πελατών προς Προϊόν Δ (%)", 0.0, 100.0, 5.0) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        price_old = parse_gr_number(price_old_input)
        price_increase_pct = parse_gr_number(price_increase_pct_input) / 100
        profit_A = parse_gr_number(profit_A_input)
        profit_B = parse_gr_number(profit_B_input)
        profit_C = parse_gr_number(profit_C_input)
        profit_D = parse_gr_number(profit_D_input)

        if None in (price_old, price_increase_pct, profit_A, profit_B, profit_C, profit_D):
            st.error("❌ Έλεγξε ότι όλα τα αριθμητικά πεδία είναι σωστά συμπληρωμένα.")
            return

        total_substitute = percent_B + percent_C + percent_D
        if total_substitute > 1:
            st.error("❌ Το συνολικό ποσοστό πελατών που επιλέγουν άλλα προϊόντα δεν μπορεί να ξεπερνά το 100%.")
            return

        no_purchase = 1 - total_substitute

        result = calculate_max_product_A_sales_drop(
            price_old,
            price_increase_pct,
            profit_A,
            profit_B,
            profit_C,
            profit_D,
            percent_B,
            percent_C,
            percent_D
        )

        if result is None:
            st.error("❌ Αδυναμία υπολογισμού. Δοκίμασε άλλες τιμές.")
        else:
            st.success(f"✅ Μέγιστη αποδεκτή μείωση πωλήσεων Προϊόντος Α: {format_percentage_gr(result)}")
            st.info(f"ℹ️ Ποσοστό πελατών που δεν θα αγοράσουν τίποτα: {format_percentage_gr(no_purchase * 100)}")
