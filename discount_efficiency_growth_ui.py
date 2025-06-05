import streamlit as st
from discount_efficiency_growth import calculate_discount_efficiency_growth
from utils import format_number_gr, parse_gr_number, format_percentage_gr

st.header("Αποδοτικότητα Πολιτικής Έκπτωσης με Ανάπτυξη Πωλήσεων")

with st.form("discount_form"):
    col1, col2 = st.columns(2)

    with col1:
        current_sales = parse_gr_number(st.text_input("Τρέχουσες πωλήσεις", "1.000"))
        extra_sales = parse_gr_number(st.text_input("Επιπλέον πωλήσεις λόγω έκπτωσης", "250"))
        discount_rate = st.number_input("Έκπτωση (%)", 0.0, 100.0, 2.0)
        discount_acceptance = st.number_input("% πελατών που αποδέχονται την έκπτωση", 0.0, 100.0, 60.0)
        discount_days = st.number_input("Μέρες για πληρωμή τοις μετρητοίς", 0, 365, 10)
        cost_percent = st.number_input("Κόστος πωλήσεων (%)", 0.0, 100.0, 80.0)

    with col2:
        non_acceptance = st.number_input("% πελατών που δεν αποδέχονται", 0.0, 100.0, 40.0)
        non_discount_days = st.number_input("Μέρες πληρωμής αν δεν αποδεχθούν", 0, 365, 120)
        wacc = st.number_input("Κόστος κεφαλαίου (WACC %)", 0.0, 100.0, 20.0)
        suppliers_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών", 0, 365, 30)
        current_collection_days = st.number_input("Τρέχουσα μέση περίοδος είσπραξης", 0, 365, 84)

    submitted = st.form_submit_button("Υπολογισμός")

if submitted:
    results = calculate_discount_efficiency_growth(
        current_sales,
        extra_sales,
        discount_rate,
        discount_acceptance,
        discount_days,
        non_acceptance,
        non_discount_days,
        discount_days,
        cost_percent,
        wacc,
        suppliers_days,
        current_collection_days,
    )

    st.subheader("Αποτελέσματα")

    st.write(f"**Καθαρή Παρούσα Αξία (NPV)**: {format_number_gr(results['npv'])} €")

    if results["max_discount"] is not None:
        st.write(f"**Μέγιστη έκπτωση για μηδενική NPV (Break-even)**: {format_percentage_gr(results['max_discount'])}")
    else:
        st.write("**Μέγιστη έκπτωση**: Δεν μπορεί να υπολογιστεί (πιθανό μηδενισμός).")

    st.write(f"**Βέλτιστη έκπτωση (προσέγγιση)**: {format_percentage_gr(results['optimal_discount'])}")
