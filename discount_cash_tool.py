import streamlit as st

def discount_cash_tool():
    st.title("Υπολογιστής Απόδοσης Έκπτωσης Πληρωμής τοις Μετρητοίς")

    # Εισαγόμενες παράμετροι
    current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", value=1000.0, min_value=0.0)
    additional_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", value=250.0, min_value=0.0)
    discount_cash_payment = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0, min_value=0.0) / 100
    pct_customers_accept_discount = st.number_input("Ποσοστό πελατών που αποδέχεται την έκπτωση (%)", value=50.0, min_value=0.0, max_value=100.0) / 100
    days_payment_accept_discount = st.number_input("Μέρες πληρωμής πελατών που αποδέχονται την έκπτωση", value=60, min_value=0)
    pct_customers_no_discount = st.number_input("Ποσοστό πελατών που δεν αποδέχεται την έκπτωση (%)", value=50.0, min_value=0.0, max_value=100.0) / 100
    days_payment_no_discount = st.number_input("Μέρες πληρωμής πελατών που δεν αποδέχονται την έκπτωση", value=120, min_value=0)
    days_cash_payment = st.number_input("Μέρες για πληρωμή τοις μετρητοίς", value=10, min_value=0)
    cost_of_sales_pct = st.number_input("Κόστος πωλήσεων (%)", value=80.0, min_value=0.0, max_value=100.0) / 100
    cost_of_capital = st.number_input("Κόστος κεφαλαίου (%)", value=20.0, min_value=0.0) / 100
    avg_supplier_payment_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών (ημέρες)", value=0, min_value=0)

    # Υπολογισμοί
    current_avg_collection_days = (
        days_payment_accept_discount * pct_customers_accept_discount
        + days_payment_no_discount * pct_customers_no_discount
    )
    
    pct_customers_new_policy = st.number_input("Ποσοστό πελατών που θα ακολουθεί τη νέα πολιτική επί του νέου συνόλου (%)", value=60.0, min_value=0.0, max_value=100.0) / 100

    profit_additional_sales = additional_sales * (1 - cost_of_sales_pct)

    # Υπολογισμός NPV
    discount_factor_cash = (1 + cost_of_capital / 365) ** days_cash_payment
    discount_factor_accept = (1 + cost_of_capital / 365) ** days_payment_accept_discount
    discount_factor_no_accept = (1 + cost_of_capital / 365) ** days_payment_no_discount
    discount_factor_supplier = (1 + cost_of_capital / 365) ** avg_supplier_payment_days
    discount_factor_current = (1 + cost_of_capital / 365) ** current_avg_collection_days

    npv = (
        (current_sales + additional_sales)
        * pct_customers_new_policy
        * (1 - discount_cash_payment)
        / discount_factor_cash
        + (current_sales + additional_sales)
        * (1 - pct_customers_new_policy)
        / discount_factor_no_accept
        - cost_of_sales_pct
        * (additional_sales / current_sales)
        * current_sales
        / discount_factor_supplier
        - current_sales / discount_factor_current
    )

    npv -= current_sales / discount_factor_current  # Αφαίρεση αρχικής αξίας

    # Μέγιστη έκπτωση (Break Even)
    if additional_sales > 0:
        max_discount = 1 - (npv / profit_additional_sales)
    else:
        max_discount = 0

    # Βέλτιστη έκπτωση (για παράδειγμα μικρό ποσοστό του max)
    optimal_discount = max_discount * 0.25

    # Εμφάνιση αποτελεσμάτων
    st.markdown("### Αποτελέσματα")
    st.write(f"Τρέχουσα μέση περίοδος είσπραξης: {current_avg_collection_days:.2f} ημέρες")
    st.write(f"% πελατών που θα ακολουθεί τη νέα πολιτική επί του νέου συνόλου: {pct_customers_new_policy*100:.2f}%")
    st.write(f"Κέρδος από επιπλέον πωλήσεις: {profit_additional_sales:.2f} €")
    st.write(f"NPV: {npv:.2f} €")
    st.write(f"Μέγιστη έκπτωση που μπορεί να δοθεί επί των πωλήσεων (NPV Break Even): {max_discount*100:.2f}%")
    st.write(f"Βέλτιστη έκπτωση που πρέπει να δοθεί: {optimal_discount*100:.2f}%")

if __name__ == "__main__":
    discount_cash_tool()
