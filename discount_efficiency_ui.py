import streamlit as st
from utils import format_number_gr, format_percentage_gr

def show_discount_efficiency_ui():
    st.title("Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς")

    st.markdown("#### ➤ Εισαγωγή Δεδομένων")
    col1, col2 = st.columns(2)

    with col1:
        current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", value=1000, step=1, format="%d")
        extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", value=250, step=1, format="%d")
        cash_discount_pct = st.number_input("Έκπτωση τοις μετρητοίς (%)", value=2.0, step=0.1) / 100
        pct_accept_discount = st.number_input("% πελατών που αποδέχεται την έκπτωση", value=60.0, step=0.1) / 100
        days_accept_discount = st.number_input("Μέρες πληρωμής όσων αποδέχονται", value=60, step=1)

    with col2:
        pct_reject_discount = st.number_input("% πελατών που δεν αποδέχεται", value=40.0, step=0.1) / 100
        days_reject_discount = st.number_input("Μέρες πληρωμής όσων δεν αποδέχονται", value=120, step=1)
        days_cash_payment = st.number_input("Μέρες πληρωμής μετρητοίς", value=10, step=1)
        cost_of_sales_pct = st.number_input("Κόστος πωλήσεων (%)", value=80.0, step=0.1) / 100
        wacc = st.number_input("Κόστος κεφαλαίου (WACC) (%)", value=20.0, step=0.1) / 100
        supplier_payment_days = st.number_input("Περίοδος αποπληρωμής προμηθευτών (μέρες)", value=30, step=1)

    st.markdown("---")
    st.markdown("#### ➤ Υπολογισμοί")

    # Υπολογισμοί
    current_avg_collection = days_accept_discount * pct_accept_discount + days_reject_discount * pct_reject_discount
    current_receivables = current_sales * current_avg_collection / 365

    pct_follow_new_policy = ((current_sales * pct_accept_discount) + extra_sales) / (current_sales + extra_sales)
    pct_remain_old = 1 - pct_follow_new_policy

    new_avg_collection_after_increase = (
        pct_follow_new_policy * days_cash_payment +
        pct_remain_old * days_reject_discount
    )
    receivables_after_increase = (current_sales + extra_sales) * new_avg_collection_after_increase / 365
    released_capital_after_increase = current_receivables - receivables_after_increase

    profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)
    profit_released_capital = released_capital_after_increase * wacc
    discount_cost = (current_sales + extra_sales) * pct_follow_new_policy * cash_discount_pct
    total_profit = profit_extra_sales + profit_released_capital - discount_cost

    # NPV υπολογισμός
    discount_rate_daily = wacc / 365
    present_value_cash_inflow = (
        (current_sales + extra_sales) * (1 - cash_discount_pct)
        / ((1 + discount_rate_daily) ** days_cash_payment)
    )
    present_value_cash_outflow = (
        cost_of_sales_pct * (current_sales + extra_sales)
        / ((1 + discount_rate_daily) ** supplier_payment_days)
    )
    npv = present_value_cash_inflow - present_value_cash_outflow

    # Max έκπτωση για break-even
    try:
        max_discount_break_even = 1 - (1 + discount_rate_daily) ** (days_cash_payment - days_reject_discount) * (
            ((1 - (1 / pct_follow_new_policy)) +
             ((1 + discount_rate_daily) ** (days_reject_discount - current_avg_collection) + (extra_sales / current_sales) * (1 + discount_rate_daily) ** (days_reject_discount - supplier_payment_days))) /
            (pct_follow_new_policy * (1 + (extra_sales / current_sales)))
        )
    except ZeroDivisionError:
        max_discount_break_even = None

    optimal_discount = (1 - ((1 + discount_rate_daily) ** (days_cash_payment - current_avg_collection))) / 2

    # Παρουσίαση αποτελεσμάτων
    st.markdown("#### ➤ Αποτελέσματα")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Μέση περίοδος είσπραξης (πριν)", f"{format_number_gr(current_avg_collection)} μέρες")
        st.metric("Απαιτήσεις (πριν)", f"{format_number_gr(current_receivables)} €")
        st.metric("Νέα περίοδος είσπραξης", f"{format_number_gr(new_avg_collection_after_increase)} μέρες")
        st.metric("Απαιτήσεις (μετά)", f"{format_number_gr(receivables_after_increase)} €")

    with col2:
        st.metric("Κέρδος από επιπλέον πωλήσεις", f"{format_number_gr(profit_extra_sales)} €")
        st.metric("Αποδέσμευση κεφαλαίου", f"{format_number_gr(released_capital_after_increase)} €")
        st.metric("Κόστος έκπτωσης", f"{format_number_gr(discount_cost)} €")
        st.metric("NPV", f"{format_number_gr(npv)} €")

    col3, col4 = st.columns(2)
    with col3:
        st.metric("% ακολουθούν τη νέα πολιτική", format_percentage_gr(pct_follow_new_policy, decimals=0))
    with col4:
        st.metric("Βέλτιστη έκπτωση", format_percentage_gr(optimal_discount))

    if max_discount_break_even is not None:
        st.success(f"Μέγιστη έκπτωση (Break-Even): {format_percentage_gr(max_discount_break_even)}")
    else:
        st.warning("Μέγιστη έκπτωση: Δεν μπορεί να υπολογιστεί (διαίρεση με μηδέν)")
