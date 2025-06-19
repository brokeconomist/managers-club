import streamlit as st
from utils import format_number_gr, parse_gr_number, format_percentage_gr

def calculate_sales_loss_threshold(
    competitor_old_price,
    competitor_new_price,
    our_price,
    unit_cost
):
    try:
        top = (competitor_new_price - competitor_old_price) / competitor_old_price
        bottom = (unit_cost - our_price) / our_price
        if bottom == 0:
            return None
        result = top / bottom
        return result * 100  # επιστρέφεται ως ποσοστό
    except ZeroDivisionError:
        return None

def show_loss_threshold_before_price_cut():
    st.header("📉 Όριο Απώλειας Πωλήσεων πριν τη Μείωση Τιμών")
    st.title("Πόσες πωλήσεις μπορώ να χάσω πριν σκεφτώ μείωση τιμής; ⚖️")

    st.markdown("""
    🧠 Οι ανταγωνιστές μείωσαν την τιμή και αναρωτιέστε αν πρέπει να κάνετε το ίδιο;

    👉 Αυτό το εργαλείο σάς δείχνει **πόσο ποσοστό πωλήσεων μπορείτε να χάσετε**
    πριν χρειαστεί να μειώσετε την τιμή σας για να παραμείνετε ανταγωνιστικοί.
    """)

    with st.form("loss_threshold_form"):
        col1, col2 = st.columns(2)

        with col1:
            competitor_old_price_input = st.text_input("Αρχική τιμή ανταγωνιστή πριν την μείωση (€)", value=format_number_gr(8.0))
            our_price_input = st.text_input("Τιμή πώλησης προϊόντος (€)", value=format_number_gr(8.0))

        with col2:
            competitor_new_price_input = st.text_input("Νέα τιμή ανταγωνιστή μετά την μείωση (€)", value=format_number_gr(7.2))
            unit_cost_input = st.text_input("Κόστος ανά μονάδα προϊόντος (€)", value=format_number_gr(4.5))

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        competitor_old_price = parse_gr_number(competitor_old_price_input)
        competitor_new_price = parse_gr_number(competitor_new_price_input)
        our_price = parse_gr_number(our_price_input)
        unit_cost = parse_gr_number(unit_cost_input)

        if None in (competitor_old_price, competitor_new_price, our_price, unit_cost):
            st.error("⚠️ Έλεγξε ότι όλα τα αριθμητικά πεδία είναι σωστά συμπληρωμένα.")
            return

        result = calculate_sales_loss_threshold(
            competitor_old_price,
            competitor_new_price,
            our_price,
            unit_cost
        )

        if result is None:
            st.error("⚠️ Δεν μπορεί να υπολογιστεί. Έλεγξε τις τιμές.")
        elif result <= 0:
            st.warning("❗ Δεν υπάρχει περιθώριο απώλειας πωλήσεων. Η τιμή σας είναι ήδη λιγότερο ανταγωνιστική.")
        else:
            st.success(f"✅ Μέγιστο % Πωλήσεων που μπορεί να χαθεί πριν μειωθεί η τιμή: {format_percentage_gr(result)}")

    st.markdown("---")
