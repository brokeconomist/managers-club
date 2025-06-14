import streamlit as st
from utils import format_number_gr, format_percentage_gr

def show_discount_efficiency_ui():
    st.title("Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς")
    st.markdown("### Εισαγωγή Δεδομένων")
    col1, col2 = st.columns(2)

    with col1:
        current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", value=1000, step=1, format="%d")
        extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", value=250, step=1, format="%d")
        cash_discount_pct = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0, step=0.1) / 100
        pct_accept_discount = st.number_input("% πελατών που αποδέχεται την έκπτωση", value=60.0, step=0.1) / 100
        days_accept_discount = st.number_input("Μέρες πληρωμής όσων αποδέχονται την έκπτωση", value=60, step=1)

    with col2:
        pct_reject_discount = st.number_input("% πελατών που δεν αποδέχεται την έκπτωση", value=40.0, step=0.1) / 100
        days_reject_discount = st.number_input("Μέρες πληρωμής όσων δεν αποδέχονται την έκπτωση", value=120, step=1)
        days_cash_payment = st.number_input("Μέρες πληρωμής τοις μετρητοίς", value=10, step=1)
        cost_of_sales_pct = st.number_input("Κόστος πωλήσεων (%)", value=80.0, step=0.1) / 100
        wacc = st.number_input("Κόστος κεφαλαίου (WACC) (%)", value=20.0, step=0.1) / 100
        supplier_payment_days = st.number_input("Ημέρες αποπληρωμής προμηθευτών", value=30, step=1)

    only_new_sales = st.checkbox("Υπολογισμός μόνο για τις επιπλέον πωλήσεις;", value=True)

    st.markdown("---")

    # Υπολογισμοί
    current_avg_collection = days_accept_discount * pct_accept_discount + days_reject_discount * pct_reject_discount
    current_receivables = current_sales * current_avg_collection / 365

    # Νέα μέση είσπραξη και απαιτήσεις μετά την πολιτική
    new_total_sales = current_sales + extra_sales
    pct_follow_new_policy = ((current_sales * pct_accept_discount) + extra_sales) / new_total_sales
    pct_remain_old = 1 - pct_follow_new_policy

    new_avg_collection = pct_follow_new_policy * days_cash_payment + pct_remain_old * days_reject_discount
    receivables_after = new_total_sales * new_avg_collection / 365
    released_capital = current_receivables - receivables_after

    profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)
    profit_released_capital = released_capital * wacc
    discount_cost = new_total_sales * pct_follow_new_policy * cash_discount_pct

    total_profit = profit_extra_sales + profit_released_capital - discount_cost

    # Υπολογισμός NPV
    discount_rate_daily = wacc / 365

    if only_new_sales:
        base_amount = extra_sales
        current_term = 0  # Δεν υπήρχε καθυστέρηση γιατί δεν υπήρχαν αυτές οι πωλήσεις
    else:
        base_amount = new_total_sales
        current_term = current_avg_collection

    try:
        npv = (
            base_amount * pct_follow_new_policy * (1 - cash_discount_pct)
            / ((1 + discount_rate_daily) ** days_cash_payment)
            + base_amount * (1 - pct_follow_new_policy)
            / ((1 + discount_rate_daily) ** days_reject_discount)
            - base_amount * (1 / ((1 + discount_rate_daily) ** current_term))
            - extra_sales * cost_of_sales_pct / ((1 + discount_rate_daily) ** supplier_payment_days)
        )
    except ZeroDivisionError:
        npv = None

    try:
        if only_new_sales:
            max_discount_break_even = 1 - (
                ((1 + discount_rate_daily) ** (days_cash_payment - days_reject_discount)) *
                (
                    ((1 - (1 / pct_follow_new_policy)) +
                     (1 + discount_rate_daily) ** (days_reject_discount - supplier_payment_days))
                )
                / pct_follow_new_policy
            )
        else:
            max_discount_break_even = 1 - (
                ((1 + discount_rate_daily) ** (days_cash_payment - days_reject_discount)) *
                (
                    ((1 - (1 / pct_follow_new_policy)) +
                     ((1 + discount_rate_daily) ** (days_reject_discount - current_avg_collection)
                      + (extra_sales / current_sales) * (1 + discount_rate_daily) ** (days_reject_discount - supplier_payment_days)))
                ) / (pct_follow_new_policy * (1 + (extra_sales / current_sales)))
            )
    except ZeroDivisionError:
        max_discount_break_even = None

    optimal_discount = (1 - ((1 + discount_rate_daily) ** (days_cash_payment - current_avg_collection))) / 2

    st.header("Αποτελέσματα")

    st.write(f"**Μέση περίοδος είσπραξης πριν:** {format_number_gr(current_avg_collection)} μέρες")
    st.write(f"**Τρέχουσες απαιτήσεις:** {format_number_gr(current_receivables)} €")
    st.write(f"**Νέα μέση περίοδος είσπραξης:** {format_number_gr(new_avg_collection)} μέρες")
    st.write(f"**Απαιτήσεις μετά την πολιτική:** {format_number_gr(receivables_after)} €")
    st.write(f"**Αποδέσμευση κεφαλαίων:** {format_number_gr(released_capital)} €")

    st.write(f"**Κέρδος από επιπλέον πωλήσεις:** {format_number_gr(profit_extra_sales)} €")
    st.write(f"**Κέρδος από αποδέσμευση κεφαλαίων:** {format_number_gr(profit_released_capital)} €")
    st.write(f"**Κόστος έκπτωσης:** {format_number_gr(discount_cost)} €")
    st.write(f"**Συνολικό όφελος:** {format_number_gr(total_profit)} €")

    if npv is not None:
        st.write(f"**Καθαρή Παρούσα Αξία (NPV):** {format_number_gr(npv)} €")
    else:
        st.write("**Καθαρή Παρούσα Αξία (NPV):** Δεν υπολογίστηκε (διαίρεση με μηδέν)")

    if max_discount_break_even is not None:
        st.write(f"**Μέγιστη Έκπτωση για NPV = 0:** {format_percentage_gr(max_discount_break_even)}")
    else:
        st.write("**Μέγιστη Έκπτωση για NPV = 0:** Δεν υπολογίστηκε (διαίρεση με μηδέν)")

    st.write(f"**Ενδεικτικά Βέλτιστη Έκπτωση:** {format_percentage_gr(optimal_discount)}")
