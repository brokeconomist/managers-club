import streamlit as st
from utils import format_number_gr, format_percentage_gr  # Υποθέτουμε ότι υπάρχουν αυτές οι συναρτήσεις

def show_discount_efficiency_ui():
    st.title("Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς")

    st.markdown("### Εισαγωγή Δεδομένων")
    col1, col2 = st.columns(2)

    with col1:
        current_sales = st.number_input("Τρέχουσες πωλήσεις", value=1000, step=1, format="%d")
        extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης", value=250, step=1, format="%d")
        cash_discount_pct = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0, min_value=0.0, max_value=100.0, step=0.1) / 100
        pct_accept_discount = st.number_input("% πελατών που αποδέχεται την έκπτωση", value=60.0, min_value=0.0, max_value=100.0, step=0.1) / 100
        days_accept_discount = st.number_input("Μέρες που πληρώνουν όσοι αποδέχονται την έκπτωση", value=60, step=1)

    with col2:
        pct_reject_discount = st.number_input("% πελατών που δεν αποδέχεται την έκπτωση", value=40.0, min_value=0.0, max_value=100.0, step=0.1) / 100
        days_reject_discount = st.number_input("Μέρες που πληρώνουν όσοι δεν αποδέχονται την έκπτωση", value=120, step=1)
        days_cash_payment = st.number_input("Μέρες για πληρωμή τοις μετρητοίς", value=10, step=1)
        cost_of_sales_pct = st.number_input("Κόστος πωλήσεων σε %", value=80.0, min_value=0.0, max_value=100.0, step=0.1) / 100
        wacc = st.number_input("Κόστος κεφαλαίου (WACC) σε %", value=20.0, min_value=0.0, max_value=100.0, step=0.1) / 100
        supplier_payment_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών (σε μέρες)", value=30, step=1)

    st.markdown("---")

    # Υπολογισμοί
    current_avg_collection = days_accept_discount * pct_accept_discount + days_reject_discount * pct_reject_discount
    current_receivables = current_sales * current_avg_collection / 365

    pct_follow_new_policy = ((current_sales * pct_accept_discount) + extra_sales) / (current_sales + extra_sales)
    pct_remain_old = 1 - pct_follow_new_policy

    new_avg_collection = pct_follow_new_policy * days_cash_payment + pct_remain_old * days_reject_discount
    new_receivables = (current_sales + extra_sales) * new_avg_collection / 365
    released_capital = current_receivables - new_receivables

    gross_profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)
    return_on_extra_sales = gross_profit_extra_sales / (new_receivables - current_receivables) if (new_receivables - current_receivables) != 0 else 0
    value_of_released_capital = released_capital * wacc
    discount_cost = (current_sales + extra_sales) * pct_follow_new_policy * cash_discount_pct
    total_economic_gain = gross_profit_extra_sales + value_of_released_capital - discount_cost

    discount_rate_daily = wacc / 365

    npv = (
        (current_sales + extra_sales) * pct_follow_new_policy * (1 - cash_discount_pct)
        * (1 / (1 + discount_rate_daily) ** days_cash_payment)
        + (current_sales + extra_sales) * (1 - pct_follow_new_policy)
        * (1 / (1 + discount_rate_daily) ** days_reject_discount)
        - cost_of_sales_pct * extra_sales * (1 / (1 + discount_rate_daily) ** supplier_payment_days)
        - current_sales * (1 / (1 + discount_rate_daily) ** current_avg_collection)
    )

        
    try:
    max_discount_break_even = 1 - (
        (1 + discount_rate_daily) ** (days_cash_payment - days_reject_discount)
        * (
            (1 - (1 / pct_follow_new_policy))
            + (1 + discount_rate_daily) ** (days_reject_discount - current_avg_collection)
            + (extra_sales / current_sales)
            * (1 + discount_rate_daily) ** (days_reject_discount - supplier_payment_days)
            - (cost_of_sales_pct * extra_sales / current_sales)
            * (1 + discount_rate_daily) ** (days_reject_discount - supplier_payment_days)
        )
        / (pct_follow_new_policy * (1 + (extra_sales / current_sales)))
    )
    except ZeroDivisionError:
        max_discount_break_even = None


    optimal_discount = (1 - ((1 + discount_rate_daily) ** (days_cash_payment - current_avg_collection))) / 2

    # Εμφάνιση Αποτελεσμάτων
    st.header("Αποτελέσματα")

    st.write(f"**Μέση περίοδος είσπραξης πριν:** {format_number_gr(current_avg_collection)} μέρες")
    st.write(f"**Τρέχουσες απαιτήσεις:** {format_number_gr(current_receivables)} €")
    st.write(f"**Νέα μέση περίοδος είσπραξης:** {format_number_gr(new_avg_collection)} μέρες")
    st.write(f"**Νέες απαιτήσεις:** {format_number_gr(new_receivables)} €")
    st.write(f"**Αποδέσμευση κεφαλαίου:** {format_number_gr(released_capital)} €")
    st.write("---")

    st.write(f"**Μικτό κέρδος από επιπλέον πωλήσεις:** {format_number_gr(gross_profit_extra_sales)} €")
    st.write(f"**Απόδοση επιπλέον πωλήσεων (σε € ανά € απαιτήσεων):** {format_number_gr(return_on_extra_sales)}")
    st.write(f"**Απόδοση αποδέσμευσης κεφαλαίου:** {format_number_gr(value_of_released_capital)} €")
    st.write(f"**Κόστος έκπτωσης:** {format_number_gr(discount_cost)} €")
    st.write(f"**Συνολικό οικονομικό όφελος:** {format_number_gr(total_economic_gain)} €")
    st.write("---")

    st.write(f"**NPV:** {format_number_gr(npv)} €")
    if max_discount_break_even is not None:
        st.write(f"**Μέγιστη έκπτωση (NPV Break-Even):** {format_percentage_gr(max_discount_break_even)}")
    else:
        st.write("**Μέγιστη έκπτωση (NPV Break-Even):** Δεν υπολογίζεται (διαίρεση με μηδέν)")

    st.write(f"**Βέλτιστη έκπτωση:** {format_percentage_gr(optimal_discount)}")
