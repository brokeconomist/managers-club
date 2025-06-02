import streamlit as st
from discount_cash_final import calculate_discount_cash_fixed_pct

def show_discount_cash_app():
    st.title("Ανάλυση Έκπτωσης για Πληρωμή Τοις Μετρητοίς")

    current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=1000.0)
    additional_sales = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", value=250.0)
    discount_pct = st.number_input("Ποσοστό Έκπτωσης (%)", value=2.0)
    acceptance_rate = st.number_input("Ποσοστό Πελατών που Αποδέχονται την Έκπτωση (%)", value=50.0)
    discount_days = st.number_input("Μέρες Πληρωμής για Έκπτωση", value=10)
    no_discount_days = st.number_input("Μέρες Πληρωμής χωρίς Έκπτωση", value=120)
    cost_pct = st.number_input("Κόστος Πωλήσεων (% επί των Πωλήσεων)", value=80.0)
    capital_cost_rate = st.number_input("Κόστος Κεφαλαίου (% Ετησίως)", value=20.0)
    supplier_payment_days = st.number_input("Μέση Περίοδος Αποπληρωμής Προμηθευτών (ημέρες)", value=0)
    current_collection_days_old = st.number_input("Τρέχουσα Μέση Περίοδος Είσπραξης (ημέρες)", value=90)

    if st.button("Υπολογισμός"):
        result = calculate_discount_cash_fixed_pct(
            current_sales=current_sales,
            additional_sales=additional_sales,
            discount_pct=discount_pct,
            acceptance_rate=acceptance_rate,
            discount_days=discount_days,
            no_discount_days=no_discount_days,
            cost_pct=cost_pct,
            capital_cost_rate=capital_cost_rate,
            supplier_payment_days=supplier_payment_days,
            current_collection_days_old=current_collection_days_old
        )

        st.markdown("## Αποτελέσματα")
        st.write(f"**NPV (€):** {result['npv']}")
        st.write(f"**Μέγιστη Δυνητική Έκπτωση (%):** {result['max_discount']}%")
        st.write(f"**Βέλτιστη Έκπτωση (%):** {result['optimal_discount']}%")
        st.write(f"**Νέα Μέση Περίοδος Είσπραξης (ημέρες):** {result['new_collection_days']}")
        st.write(f"**Παλιά Μέση Περίοδος Είσπραξης (ημέρες):** {result['old_collection_days']}")
