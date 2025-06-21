import streamlit as st
from discount_proposal_logic import calculate_discount_analysis
from utils import format_number_gr

def show_discount_proposal_ui():
    st.title("Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς")

    # Εισαγωγή δεδομένων
    current_sales = st.number_input("Τρέχουσες Πωλήσεις", value=1000.0, step=100.0)
    cost_of_sales = st.number_input("Κόστος Πωλήσεων", value=800.0, step=100.0)
    additional_sales_discount = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης", value=250.0, step=10.0)
    cash_discount_rate = st.number_input("Έκπτωση για Πληρωμή τοις Μετρητοίς (0.02 = 2%)", value=0.02, step=0.01)
    pct_sales_with_discount = st.number_input("Ποσοστό Πωλήσεων με Έκπτωση (0.40 = 40%)", value=0.40, step=0.05)
    days_collection_discounted = st.number_input("Μέρες Είσπραξης Πωλήσεων με Έκπτωση", value=30)
    pct_sales_without_discount = st.number_input("Ποσοστό Πωλήσεων χωρίς Έκπτωση (0.60 = 60%)", value=0.60, step=0.05)
    days_collection_undiscounted = st.number_input("Μέρες Είσπραξης Πωλήσεων χωρίς Έκπτωση", value=60)
    days_cash_payment_deadline = st.number_input("Μέρες Προθεσμία για Πληρωμή τοις Μετρητοίς", value=10)
    pct_sales_with_discount_after_increase = st.number_input("Ποσοστό Πωλήσεων με Έκπτωση μετά την Αύξηση (0.70 = 70%)", value=0.70, step=0.05)
    pct_sales_without_discount_after_increase = st.number_input("Ποσοστό Πωλήσεων χωρίς Έκπτωση μετά την Αύξηση (0.30 = 30%)", value=0.30, step=0.05)
    pct_current_bad_debts = st.number_input("Ποσοστό Τρεχουσών Επισφαλειών (0.02 = 2%)", value=0.02, step=0.01)
    pct_bad_debt_reduction_after_discount = st.number_input("Μείωση Επισφαλειών λόγω Μετρητών (0.01 = 1%)", value=0.01, step=0.01)
    cost_of_capital = st.number_input("Κόστος Κεφαλαίου (0.20 = 20%)", value=0.20, step=0.01)
    avg_supplier_payment_days = st.number_input("Μέση Περίοδος Αποπληρωμής Προμηθευτών", value=30)

    if st.button("Υπολογισμός"):
        results = calculate_discount_analysis(
            current_sales,
            cost_of_sales,
            additional_sales_discount,
            cash_discount_rate,
            pct_sales_with_discount,
            days_collection_discounted,
            pct_sales_without_discount,
            days_collection_undiscounted,
            days_cash_payment_deadline,
            pct_sales_with_discount_after_increase,
            pct_sales_without_discount_after_increase,
            pct_current_bad_debts,
            pct_bad_debt_reduction_after_discount,
            cost_of_capital,
            avg_supplier_payment_days,
        )

        st.subheader("Αποτελέσματα")
        st.write(f"Τρέχουσα Μέση Περίοδος Είσπραξης Απαιτήσεων: {results['current_avg_collection_days']} ημέρες")
        st.write(f"Τρέχουσες Απαιτήσεις: {results['current_receivables']} €")
        st.write(f"Μέση Περίοδος Είσπραξης μετά την Αύξηση Πωλήσεων: {results['new_avg_collection_days']} ημέρες")
        st.write(f"Απαιτήσεις μετά την Αύξηση Πωλήσεων: {results['new_receivables']} €")
        st.write(f"Αποδέσμευση Κεφαλαίων: {results['released_capital']} €")
        st.write(f"Κέρδος από Επιπλέον Πωλήσεις: {results['profit_from_additional_sales']} €")
        st.write(f"Κέρδος από Αποδέσμευση Κεφαλαίων: {results['profit_from_released_capital']} €")
        st.write(f"Κέρδος από Μείωση Επισφαλειών: {results['profit_from_bad_debt_reduction']} €")
        st.write(f"Κόστος Έκπτωσης: {results['discount_cost']} €")
        st.write(f"Μέγιστη Έκπτωση που μπορεί να δοθεί: {results['max_discount_pct']}%")
        st.write(f"Εκτιμώμενη Βέλτιστη Έκπτωση που πρέπει να δοθεί: {results['estimated_best_discount_pct']}%")
        st.write(f"Καθαρή Παρούσα Αξία (NPV): {format_number_gr(results['npv'])} €")

