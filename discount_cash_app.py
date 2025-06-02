def show_discount_cash_app():
    import streamlit as st
    from discount_cash_final import calculate_discount_cash_fixed_pct

    st.title("Ανάλυση Έκπτωσης για Πληρωμή Τοις Μετρητοίς")

    st.header("Εισαγωγή Δεδομένων")

    current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", min_value=0.0, value=1000.0)
    additional_sales = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", min_value=0.0, value=250.0)
    discount_pct = st.number_input("Ποσοστό Έκπτωσης (%)", min_value=0.0, value=2.0)
    acceptance_rate = st.number_input("Ποσοστό Πελατών που Αποδέχονται την Έκπτωση (%)", min_value=0.0, max_value=100.0, value=50.0)
    discount_days = st.number_input("Μέρες Πληρωμής για Έκπτωση", min_value=0, value=10)
    full_days = st.number_input("Μέρες Πληρωμής χωρίς Έκπτωση", min_value=0, value=120)
    cost_pct = st.number_input("Κόστος Πωλήσεων (% επί των Πωλήσεων)", min_value=0.0, max_value=100.0, value=80.0)
    capital_cost_pct = st.number_input("Κόστος Κεφαλαίου (% Ετησίως)", min_value=0.0, max_value=100.0, value=20.0)
    supplier_days = st.number_input("Μέση Περίοδος Αποπληρωμής Προμηθευτών (ημέρες)", min_value=0, value=0)

    st.subheader("Τρέχουσα Κατάσταση Πριν την Πολιτική")
    current_collection_days_old = st.number_input("Τρέχουσα Μέση Περίοδος Είσπραξης (ημέρες)", min_value=0, value=90)

    if st.button("Υπολογισμός"):
        result = calculate_discount_cash_fixed_pct(
            current_sales=current_sales,
            additional_sales=additional_sales,
            discount_pct=discount_pct,
            acceptance_rate=acceptance_rate,
            discount_days=discount_days,
            full_days=full_days,
            cost_pct=cost_pct,
            capital_cost_pct=capital_cost_pct,
            supplier_days=supplier_days,
            current_collection_days=current_collection_days_old
        )

        st.subheader("Αποτελέσματα")
        st.write(f"NPV (€): {result['npv']:.2f}")
        st.write(f"Μέγιστη Δυνητική Έκπτωση (%): {result['max_discount_pct']:.2f}%")
        st.write(f"Βέλτιστη Έκπτωση (%): {result['optimal_discount_pct']:.2f}%")
