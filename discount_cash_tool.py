import streamlit as st

def show_discount_cash_tool():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    # Εισαγωγή παραμέτρων
    current_sales = st.number_input("Τρέχουσες πωλήσεις", value=1000.0)
    additional_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης", value=250.0)
    discount_rate = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0) / 100
    pct_accept_discount = st.number_input("% των πελατών που αποδέχεται την έκπτωση", value=50.0) / 100
    days_pay_discount = st.number_input("% των πελατών που αποδέχεται την έκπτωση πληρώνει σε (μέρες)", value=60)
    pct_reject_discount = st.number_input("% των πελατών που δεν αποδέχεται την έκπτωση", value=50.0) / 100
    days_pay_no_discount = st.number_input("% πελατών που δεν αποδέχεται την έκπτωση πληρώνει σε (μέρες)", value=120)
    cash_days = st.number_input("Μέρες για πληρωμή τοις μετρητοίς", value=10)
    cost_of_sales_pct = st.number_input("Κόστος πωλήσεων σε %", value=80.0) / 100
    cost_of_capital = st.number_input("Κόστος κεφαλαίου (%)", value=20.0) / 100
    supplier_pay_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών (μέρες)", value=0)

    # Υπολογισμοί
    current_avg_collection_days = 90
    pct_follow_new_policy = 60.0 / 100

    # Κέρδος από επιπλέον πωλήσεις
    profit_per_sale = 1 - cost_of_sales_pct
    additional_profit = additional_sales * profit_per_sale

    # Μέση περίοδος είσπραξης μετά την πολιτική
    new_avg_collection_days = (
        pct_accept_discount * days_pay_discount +
        pct_reject_discount * days_pay_no_discount
    )

    weighted_avg_collection_days = (
        (current_sales * current_avg_collection_days + additional_sales * new_avg_collection_days) /
        (current_sales + additional_sales)
    )

    # Αποδέσμευση κεφαλαίου κίνησης σε ημέρες
    release_days = current_avg_collection_days - weighted_avg_collection_days

    # Αξία αποδέσμευσης κεφαλαίου (σε μονάδες πωλήσεων)
    net_working_capital_released = (release_days - supplier_pay_days) * cost_of_sales_pct * (current_sales + additional_sales) / 365

    # Παρούσα αξία αποδέσμευσης κεφαλαίου (PV)
    pv_working_capital_released = net_working_capital_released / (1 + cost_of_capital)

    # Καθαρό NPV (Κέρδη + PV κεφαλαίου - Κόστος έκπτωσης)
    discount_cost = discount_rate * pct_accept_discount * (current_sales + additional_sales)
    npv = additional_profit + pv_working_capital_released - discount_cost

    # Μέγιστη έκπτωση NPV break-even (όταν npv=0)
    max_discount = npv / (pct_accept_discount * (current_sales + additional_sales)) if pct_accept_discount > 0 else 0

    # Βέλτιστη έκπτωση (πχ βελτιστοποίηση με υποθέσεις)
    optimal_discount = discount_rate  # placeholder, μπορεί να προστεθεί optimization

    # Εμφάνιση αποτελεσμάτων
    st.write(f"**Κέρδος από επιπλέον πωλήσεις:** {additional_profit:.2f} €")
    st.write(f"**NPV:** {npv:.2f} €")
    st.write(f"**Μέγιστη έκπτωση που μπορεί να δοθεί επί των πωλήσεων (NPV Break Even):** {max_discount * 100:.2f} %")
    st.write(f"**Βέλτιστη έκπτωση που πρέπει να δοθεί:** {optimal_discount * 100:.2f} %")
