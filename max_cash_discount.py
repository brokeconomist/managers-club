# max_cash_discount.py
import streamlit as st

def calculate_max_cash_discount_advanced(
    current_sales,
    extra_sales,
    discount_trial,
    prcnt_of_total_new_clients_in_new_policy,
    days_curently_paying_clients_take_discount,
    days_curently_paying_clients_not_take_discount,
    new_days_payment_clients_take_discount,
    COGS,
    WACC,
    avg_days_pay_suppliers,
    avg_current_collection_days
):
    # Μετατροπή ποσοστών σε δεκαδικά
    discount_trial = discount_trial / 100
    COGS = COGS / 100
    WACC = WACC / 100
    prcnt_of_total_new_clients_in_new_policy = prcnt_of_total_new_clients_in_new_policy / 100

    daily_rate = WACC / 365

    part1 = (1 + daily_rate) ** (new_days_payment_clients_take_discount - days_curently_paying_clients_not_take_discount)

    numerator = (
        1
        - (1 / prcnt_of_total_new_clients_in_new_policy)
        + (1 + daily_rate) ** (days_curently_paying_clients_not_take_discount - avg_current_collection_days)
        + COGS * (extra_sales / current_sales) * (1 + daily_rate) ** (days_curently_paying_clients_not_take_discount - avg_days_pay_suppliers)
    )

    denominator = prcnt_of_total_new_clients_in_new_policy * (1 + (extra_sales / current_sales))

    discount = 1 - part1 * (numerator / denominator)

    return discount


def show_max_cash_discount_ui():
    st.header("📉 Υπολογισμός Μέγιστης Αποδεκτής Έκπτωσης Τοις Μετρητοίς")

    st.markdown("Εισάγετε τις τιμές για τον υπολογισμό:")

    col1, col2 = st.columns(2)
    with col1:
        current_sales = st.number_input("Τρέχουσες Πωλήσεις (current_sales)", value=1000, step=1)
        extra_sales = st.number_input("Επιπλέον Πωλήσεις (extra_sales)", value=250, step=1)
        discount_trial = st.number_input("Πειραματική Έκπτωση (%)", value=2.0, step=0.01, format="%.2f")
        prcnt_of_total_new_clients_in_new_policy = st.number_input("Ποσοστό Νέων Πελατών που παίρνουν έκπτωση (%)", value=40.0, step=0.01, format="%.2f")
        days_curently_paying_clients_take_discount = st.number_input("Μέρες Πληρωμής πελατών με έκπτωση", value=60, step=1)
        days_curently_paying_clients_not_take_discount = st.number_input("Μέρες Πληρωμής πελατών χωρίς έκπτωση", value=120, step=1)
    with col2:
        new_days_payment_clients_take_discount = st.number_input("Νέες Μέρες Πληρωμής πελατών με έκπτωση", value=10, step=1)
        COGS = st.number_input("Κόστος Πωληθέντων (%)", value=80.0, step=0.1, format="%.1f")
        WACC = st.number_input("WACC (%)", value=20.0, step=0.1, format="%.1f")
        avg_days_pay_suppliers = st.number_input("Μέσες Μέρες Πληρωμής Προμηθευτών", value=30.0, step=1)
        avg_current_collection_days = st.number_input("Μέσες Μέρες Είσπραξης", value=60, step=1)

    if st.button("Υπολογισμός"):
        try:
            discount = calculate_max_cash_discount_advanced(
                current_sales,
                extra_sales,
                discount_trial,
                prcnt_of_total_new_clients_in_new_policy,
                days_curently_paying_clients_take_discount,
                days_curently_paying_clients_not_take_discount,
                new_days_payment_clients_take_discount,
                COGS,
                WACC,
                avg_days_pay_suppliers,
                avg_current_collection_days
            )
            st.success(f"✅ Υπολογιζόμενη Μέγιστη Αποδεκτή Έκπτωση: {discount*100:.2f}%")
        except Exception as e:
            st.error(f"Σφάλμα στον υπολογισμό: {e}")
