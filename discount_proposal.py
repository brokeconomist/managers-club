import streamlit as st
from discount_proposal_logic import calculate_discount_analysis

def show_discount_proposal_ui():
    st.title("Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς")

    # Εισαγωγή δεδομένων
    current_sales = st.number_input("Τρέχουσες Πωλήσεις", value=1000.0, step=100.0)
    cost_of_sales = st.number_input("Κόστος Πωλήσεων", value=800.0, step=100.0)
    additional_sales_discount = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης", value=250.0, step=10.0)
    cash_discount_rate = st.number_input("Έκπτωση για Πληρωμή τοις Μετρητοίς (%)", value=0.02, step=0.01)
    pct_sales_with_discount = st.number_input("Ποσοστό Πωλήσεων με Έκπτωση (%)", value=0.40, step=0.1)
    days_collection_discounted = st.number_input("Μέρες Είσπραξης Πωλήσεων με Έκπτωση", value=30)
    pct_sales_without_discount = st.number_input("Ποσοστό Πωλήσεων χωρίς Έκπτωση (%)", value=0.60, step=0.1)
    days_collection_undiscounted = st.number_input("Μέρες Είσπραξης Πωλήσεων χωρίς Έκπτωση", value=60)
    days_cash_payment_deadline = st.number_input("Μέρες Προθεσμία για Πληρωμή τοις Μετρητοίς", value=10)
    pct_sales_with_discount_after_increase = st.number_input("Ποσοστό Πωλήσεων με Έκπτωση μετά την Αύξηση (%)", value=0.70, step=0.1)
    pct_sales_without_discount_after_increase = st.number_input("Ποσοστό Πωλήσεων χωρίς Έκπτωση μετά την Αύξηση (%)", value=0.30, step=0.1)
    pct_current_bad_debts = st.number_input("% Τρεχουσών Επισφαλειών", value=1.0, step=0.1) / 100
    pct_bad_debt_reduction_after_discount = st.number_input("% Μείωσης Επισφαλειών λόγω Πληρωμών μετρητοίς", value=0.05, step=0.01)
    cost_of_capital = st.number_input("Κόστος Κεφαλαίου (%)", value=0.20, step=0.01)
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
        st.write(f"Τρέχουσες Απαιτήσεις: {results['current_receivables']} μονάδες")
        st.write(f"Μέση Περίοδος Είσπραξης μετά την Αύξηση Πωλήσεων: {results['new_avg_collection_days']} ημέρες")
        st.write(f"Απαιτήσεις μετά την Αύξηση Πωλήσεων: {results['new_receivables']} μονάδες")
        st.write(f"Αποδέσμευση Κεφαλαίων: {results['released_capital']} μονάδες")
        st.write(f"Κέρδος από Επιπλέον Πωλήσεις: {results['profit_from_additional_sales']} μονάδες")
        st.write(f"Κέρδος από Αποδέσμευση Κεφαλαίων: {results['profit_from_released_capital']} μονάδες")
        st.write(f"Κέρδος από Μείωση Επισφαλειών: {results['profit_from_bad_debt_reduction']} μονάδες")
        st.write(f"Κόστος Έκπτωσης: {results['discount_cost']} μονάδες")
        st.write(f"Εκτιμώμενο Συνολικό Κέρδος: {results['total_estimated_profit']} μονάδες")
        st.write(f"Μέγιστη Έκπτωση που μπορεί να δοθεί: {results['max_discount_pct']}%")
        st.write(f"Εκτιμώμενη Βέλτιστη Έκπτωση που πρέπει να δοθεί: {results['estimated_best_discount_pct']}%")
