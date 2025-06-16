import streamlit as st
from dmax_logic import calculate_dmax_excel_compatible
from utils import parse_gr_number, format_percentage_gr

def show_discount_efficiency_ui():
    st.header("💸 Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς (Dmax)")

    st.markdown("""
    Υπολογίζει τη **μέγιστη έκπτωση τοις μετρητοίς** που μπορεί να προσφέρει η επιχείρηση σε πελάτες, χωρίς να μειωθεί η συνολική οικονομική αξία της πίστωσης.
    """)

    col1, col2 = st.columns(2)

    with col1:
        current_sales_str = st.text_input("Τρέχουσες Πωλήσεις (€)", "1.000")
        extra_sales_str = st.text_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", "250")
        prc_clients_take_disc_str = st.text_input("Ποσοστό Πελατών που Αποδέχονται την Έκπτωση (%)", "40,0")
        COGS_str = st.text_input("Κόστος Πωληθέντων (COGS %)", "80,0")
        WACC_str = st.text_input("WACC (% ετησίως)", "20,0")

    with col2:
        days_clients_take_discount = st.number_input("Ημέρες Πληρωμής Πελατών με Έκπτωση", min_value=0, value=60)
        days_clients_not_take_discount = st.number_input("Ημέρες Πληρωμής χωρίς Έκπτωση", min_value=1, value=120)
        new_days_payment_clients_take_discount = st.number_input("Νέες Ημέρες Πληρωμής με Έκπτωση", min_value=0, value=10)
        avg_days_pay_suppliers = st.number_input("Μέσες Ημέρες Πληρωμής Προμηθευτών", min_value=0, value=30)
        avg_current_collection_days = st.number_input("Μέσος Τρέχων Χρόνος Είσπραξης", min_value=1, value=96)

    # Μετατροπή δεδομένων
    current_sales = parse_gr_number(current_sales_str)
    extra_sales = parse_gr_number(extra_sales_str)
    prc_clients_take_disc = parse_gr_number(prc_clients_take_disc_str) / 100
    COGS = parse_gr_number(COGS_str) / 100
    WACC = parse_gr_number(WACC_str) / 100

    dmax = calculate_dmax_excel_compatible(
        current_sales,
        extra_sales,
        prc_clients_take_disc,
        days_clients_take_discount,
        days_clients_not_take_discount,
        new_days_payment_clients_take_discount,
        COGS,
        WACC,
        avg_days_pay_suppliers,
        avg_current_collection_days
    )

    st.subheader("📈 Μέγιστη Επιτρεπτή Έκπτωση Τοις Μετρητοίς:")
    st.success(f"{format_percentage_gr(dmax)}")
