import streamlit as st

def show_discount_efficiency_ui():
    st.title("Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς")

    # Είσοδοι από χρήστη
    col1, col2 = st.columns(2)
    with col1:
        current_sales = st.number_input("Τρέχουσες πωλήσεις", value=1000, step=1, format="%d")
        extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης", value=250, step=1, format="%d")
        cash_discount_pct = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0, min_value=0.0, max_value=100.0, step=0.1) / 100
        pct_accept_discount = st.number_input("% πελατών που αποδέχεται την έκπτωση", value=60.0, min_value=0.0, max_value=100.0, step=0.1) / 100
        days_accept_discount = st.number_input("Μέρες που πληρώνουν όσοι αποδέχονται την έκπτωση", value=60, step=1)
        pct_reject_discount = st.number_input("% πελατών που δεν αποδέχεται την έκπτωση", value=40.0, min_value=0.0, max_value=100.0, step=0.1) / 100
        days_reject_discount = st.number_input("Μέρες που πληρώνουν όσοι δεν αποδέχονται την έκπτωση", value=120, step=1)

    with col2:
        days_cash_payment = st.number_input("Μέρες για πληρωμή τοις μετρητοίς (π.χ. 10)", value=10, step=1)
        cost_of_sales_pct = st.number_input("Κόστος πωλήσεων σε %", value=80.0, min_value=0.0, max_value=100.0, step=0.1) / 100
        wacc = st.number_input("Κόστος κεφαλαίου (WACC) σε %", value=20.0, min_value=0.0, max_value=100.0, step=0.1) / 100
        supplier_payment_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών (σε μέρες)", value=30, step=1)

    st.markdown("---")

    # Υπολογισμοί
    # Μέση περίοδος είσπραξης πριν τη νέα πολιτική
    current_avg_collection = days_accept_discount * pct_accept_discount + days_reject_discount * pct_reject_discount

    # Τρέχουσες απαιτήσεις
    current_receivables = current_sales * current_avg_collection / 365

    # Νέα μέση περίοδος είσπραξης μετά την έκπτωση
    new_avg_collection_discount = days_accept_discount * pct_accept_discount + days_reject_discount * pct_reject_discount

    # Νέες απαιτήσεις μετά την έκπτωση (χωρίς επιπλέον πωλήσεις)
    new_receivables_discount = current_sales * new_avg_collection_discount / 365

    # Αποδέσμευση κεφαλαίων (χωρίς επιπλέον πωλήσεις)
    released_capital_discount = current_receivables - new_receivables_discount

    # % πελατών που ακολουθεί τη νέα πολιτική επί του νέου συνόλου
    pct_follow_new_policy = ((current_sales * pct_accept_discount) + extra_sales) / (current_sales + extra_sales)

    # % πελατών που παραμένει με την παλιά κατάσταση
    pct_remain_old = 1 - pct_follow_new_policy

    # Νέα μέση περίοδος είσπραξης μετά την αύξηση πωλήσεων
    new_avg_collection_after_increase = pct_follow_new_policy * days_cash_payment + pct_remain_old * days_reject_discount

    # Απαιτήσεις μετά την αύξηση πωλήσεων
    receivables_after_increase = ((current_sales + extra_sales) * new_avg_collection_after_increase) / 365

    # Αποδέσμευση κεφαλαίων μετά την αύξηση πωλήσεων
    released_capital_after_increase = current_receivables - receivables_after_increase

    # Κέρδος από επιπλέον πωλήσεις
    profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)

    # Κέρδος αποδέσμευσης κεφαλαίων
    profit_released_capital = released_capital_after_increase * wacc

    # Κόστος έκπτωσης
    discount_cost = (current_sales + extra_sales) * pct_follow_new_policy * cash_discount_pct

    # Συνολικό κέρδος από την πρόταση
    total_profit = profit_extra_sales + profit_released_capital - discount_cost

    # NPV (παραγωγή προεξοφλημένων ταμειακών ροών)
    discount_rate_daily = wacc / 365

    npv = (
        (current_sales + extra_sales) * pct_follow_new_policy * (1 - cash_discount_pct) * (1 / (1 + discount_rate_daily) ** days_cash_payment)
        + (current_sales + extra_sales) * (1 - pct_follow_new_policy) * (1 / (1 + discount_rate_daily) ** days_reject_discount)
        - current_sales * (extra_sales / current_sales) * (1 / (1 + discount_rate_daily) ** supplier_payment_days)
        - current_sales * (1 / (1 + discount_rate_daily) ** current_avg_collection)
    )

    # Μέγιστη έκπτωση που μπορεί να δοθεί (NPV break even)
    try:
        max_discount_break_even = 1 - (1 + discount_rate_daily) ** (days_cash_payment - days_reject_discount) * (
            ((1 - (1 / pct_follow_new_policy)) + 
            ((1 + discount_rate_daily) ** (days_reject_discount - current_avg_collection) + (extra_sales / current_sales) * (1 + discount_rate_daily) ** (days_reject_discount - supplier_payment_days))) /
            (pct_follow_new_policy * (1 + (extra_sales / current_sales)))
            )
        )
    except ZeroDivisionError:
        max_discount_break_even = None

    # Βέλτιστη έκπτωση
    optimal_discount = (1 - ((1 + discount_rate_daily) ** (days_cash_payment - current_avg_collection))) / 2

    # Εμφάνιση αποτελεσμάτων
    st.header("Αποτελέσματα")

    st.write(f"**Μέση περίοδος είσπραξης πριν τη νέα πολιτική:** {current_avg_collection:.2f} μέρες")
    st.write(f"**Τρέχουσες απαιτήσεις πριν τη νέα πολιτική:** {current_receivables:.2f} μονάδες")

    st.write(f"**Νέα μέση περίοδος είσπραξης μετά την έκπτωση:** {new_avg_collection_discount:.2f} μέρες")
    st.write(f"**Νέες απαιτήσεις μετά την έκπτωση:** {new_receivables_discount:.2f} μονάδες")
    st.write(f"**Αποδέσμευση κεφαλαίων (χωρίς επιπλέον πωλήσεις):** {released_capital_discount:.2f} μονάδες")

    st.write(f"**% πελατών που ακολουθεί τη νέα πολιτική επί του νέου συνόλου:** {pct_follow_new_policy:.2%}")
    st.write(f"**% πελατών που παραμένει με την παλιά κατάσταση:** {pct_remain_old:.2%}")

    st.write(f"**Νέα μέση περίοδος είσπραξης μετά την αύξηση πωλήσεων:** {new_avg_collection_after_increase:.2f} μέρες")
    st.write(f"**Απαιτήσεις μετά την αύξηση πωλήσεων:** {receivables_after_increase:.2f} μονάδες")
    st.write(f"**Αποδέσμευση κεφαλαίων μετά την αύξηση πωλήσεων:** {released_capital_after_increase:.2f} μονάδες")

    st.write(f"**Κέρδος από επιπλέον πωλήσεις:** {profit_extra_sales:.2f} μονάδες")
    st.write(f"**Κέρδος αποδέσμευσης κεφαλαίων:** {profit_released_capital:.2f} μονάδες")
    st.write(f"**Κόστος έκπτωσης:** {discount_cost:.2f} μονάδες")

    st.write(f"**Συνολικό κέρδος από την πρόταση:** {total_profit:.2f} μονάδες")
    st.write(f"**NPV:** {npv:.2f} μονάδες")

    if max_discount_break_even is not None:
        st.write(f"**Μέγιστη έκπτωση (NPV Break Even):** {max_discount_break_even:.2%}")
    else:
        st.write("**Μέγιστη έκπτωση (NPV Break Even):** Δεν υπολογίζεται (διαίρεση με μηδέν)")

    st.write(f"**Βέλτιστη έκπτωση:** {optimal_discount:.2%}")
