import streamlit as st
from utils import format_number_gr, parse_gr_number, format_percentage_gr

def calculate_required_sales_increase(
    old_price,
    price_decrease_pct,
    profit_suit,
    profit_shirt,
    profit_tie,
    profit_belt,
    profit_shoes,
    percent_shirt,
    percent_tie,
    percent_belt,
    percent_shoes
):
    """
    Υπολογίζει την ελάχιστη % αύξηση πωλήσεων στα Κοστούμια ώστε να διατηρηθεί το συνολικό κέρδος
    μετά από μείωση τιμής, λαμβάνοντας υπόψη τα συμπληρωματικά προϊόντα.
    """
    combined_profit = (
        profit_suit +
        percent_shirt * profit_shirt +
        percent_tie * profit_tie +
        percent_belt * profit_belt +
        percent_shoes * profit_shoes
    )

    new_price = old_price * (1 - price_decrease_pct)
    new_profit = combined_profit - (old_price - new_price)

    try:
        required_increase = (old_price - new_price) / new_profit
        return required_increase * 100
    except ZeroDivisionError:
        return None

def show_complementary_analysis():
    st.write("Ανάλυση Συμπληρωματικών Προϊόντων")
    st.header("🧥 Εκτίμηση Αύξησης Πωλήσεων Κοστουμιών μετά από Έκπτωση")
    st.title("Τι θα γίνει αν οι πελάτες αγοράζουν και τα αξεσουάρ; 👔👞")
    st.markdown("""
    Ο υπεύθυνος σκέφτεται να μειώσει την τιμή στα κοστούμια. Όμως, γνωρίζει ότι οι πελάτες αγοράζουν και
    άλλα προϊόντα (π.χ. πουκάμισο, γραβάτα, παπούτσια).

    👉 Πόση αύξηση στις πωλήσεις κοστουμιών χρειάζεται για να μη μειωθεί το συνολικό κέρδος;
    """)

    with st.form("discount_impact_form"):
        col1, col2 = st.columns(2)

        with col1:
            old_price_input = st.text_input("Τιμή Κοστουμιού (€)", value=format_number_gr(200))
            cost_suit_input = st.text_input("Κόστος Κοστουμιού (€)", value=format_number_gr(140))
            price_decrease_input = st.text_input("Μείωση Τιμής Κοστουμιού (%)", value=format_number_gr(10.0))

            shirt_profit_input = st.text_input("Κέρδος Πουκαμίσου (€)", value=format_number_gr(13))
            tie_profit_input = st.text_input("Κέρδος Γραβάτας (€)", value=format_number_gr(11))

        with col2:
            belt_profit_input = st.text_input("Κέρδος Ζώνης (€)", value=format_number_gr(11))
            shoes_profit_input = st.text_input("Κέρδος Παπουτσιών (€)", value=format_number_gr(45))

            percent_shirt = st.slider("% πελατών που αγοράζουν πουκάμισο", 0.0, 100.0, 90.0) / 100
            percent_tie = st.slider("% πελατών που αγοράζουν γραβάτα", 0.0, 100.0, 70.0) / 100
            percent_belt = st.slider("% πελατών που αγοράζουν ζώνη", 0.0, 100.0, 10.0) / 100
            percent_shoes = st.slider("% πελατών που αγοράζουν παπούτσια", 0.0, 100.0, 5.0) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        old_price = parse_gr_number(old_price_input)
        cost_suit = parse_gr_number(cost_suit_input)
        price_decrease_pct = parse_gr_number(price_decrease_input) / 100
        profit_suit = old_price - cost_suit

        profit_shirt = parse_gr_number(shirt_profit_input)
        profit_tie = parse_gr_number(tie_profit_input)
        profit_belt = parse_gr_number(belt_profit_input)
        profit_shoes = parse_gr_number(shoes_profit_input)

        if None in (
            old_price, cost_suit, price_decrease_pct, profit_suit,
            profit_shirt, profit_tie, profit_belt, profit_shoes
        ):
            st.error("❌ Έλεγξε ότι όλα τα αριθμητικά πεδία είναι σωστά συμπληρωμένα.")
            return

        result = calculate_required_sales_increase(
            old_price,
            price_decrease_pct,
            profit_suit,
            profit_shirt,
            profit_tie,
            profit_belt,
            profit_shoes,
            percent_shirt,
            percent_tie,
            percent_belt,
            percent_shoes
        )

        if result is None:
            st.error("❌ Δεν μπορεί να υπολογιστεί. Δοκίμασε διαφορετικές τιμές.")
        else:
            st.success(f"✅ Απαιτούμενη αύξηση πωλήσεων κοστουμιών: {format_percentage_gr(result)}")
