import streamlit as st
from discount_efficiency_growth import calculate_discount_efficiency_growth
from utils import format_number_gr, parse_gr_number, format_percentage_gr

st.header("Αποδοτικότητα Πολιτικής Έκπτωσης με Ανάπτυξη Πωλήσεων")

with st.form("discount_form"):
    col1, col2 = st.columns(2)

    with col1:
        current_sales = parse_gr_number(st.text_input("Τρέχουσες πωλήσεις (€)", "1.000"))
        extra_sales = parse_gr_number(st.text_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", "250"))
        discount_rate = st.number_input("Έκπτωση (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1)
        discount_acceptance = st.number_input("% πελατών που αποδέχονται την έκπτωση", min_value=0.0, max_value=100.0, value=60.0, step=0.1)
        discount_days = st.number_input("Μέρες πληρωμής αν αποδεχθούν την έκπτωση", min_value=0, max_value=365, value=60)
        cost_percent = st.number_input("Κόστος πωλήσεων (%)", min_value=0.0, max_value=100.0, value=80.0, step=0.1)

    with col2:
        non_acceptance = st.number_input("% πελατών που δεν αποδέχονται την έκπτωση", min_value=0.0, max_value=100.0, value=40.0, step=0.1)
        non_discount_days = st.number_input("Μέρες πληρωμής αν δεν αποδεχθούν την έκπτωση", min_value=0, max_value=365, value=120)
        cash_days = st.number_input("Μέρες για πληρωμή τοις μετρητοίς (χωρίς πίστωση)", min_value=0, max_value=365, value=10)
        wacc = st.number_input("Κόστος κεφαλαίου (WACC %)", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
        suppliers_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών (ημέρες)", min_value=0, max_value=365, value=30)
        current_collection_days = st.number_input("Τρέχουσα μέση περίοδος είσπραξης (ημέρες)", min_value=0, max_value=365, value=84)

    total_acceptance = discount_acceptance + non_acceptance
    if total_acceptance != 100.0:
        st.warning(f"Το ποσοστό πελατών που αποδέχονται και δεν αποδέχονται την έκπτωση πρέπει να αθροίζει 100% (τώρα είναι {total_acceptance}%).")

    submitted = st.form_submit_button("Υπολογισμός")

if submitted:
    if total_acceptance == 100.0:
        results = calculate_discount_efficiency_growth(
            current_sales=current_sales,
            extra_sales=extra_sales,
            discount_rate=discount_rate,
            discount_acceptance=discount_acceptance,
            discount_days=discount_days,
            non_acceptance=non_acceptance,
            non_discount_days=non_discount_days,
            cash_days=cash_days,
            cost_percent=cost_percent,
            wacc=wacc,
            suppliers_days=suppliers_days,
            current_collection_days=current_collection_days
        )

        st.subheader("Αποτελέσματα")

        st.write(f"**Καθαρή Παρούσα Αξία (NPV)**: {format_number_gr(results['npv'])} €")

        if results["max_discount"] is not None:
            st.write(f"**Μέγιστη έκπτωση για μηδενική NPV (Break-even)**: {format_percentage_gr(results['max_discount'])}")
        else:
            st.write("**Μέγιστη έκπτωση**: Δεν μπορεί να υπολογιστεί (πιθανός μηδενισμός).")

        st.write(f"**Βέλτιστη έκπτωση (προσέγγιση)**: {format_percentage_gr(results['optimal_discount'])}")
    else:
        st.error("Διορθώστε το ποσοστό πελατών ώστε να αθροίζει 100%.")
