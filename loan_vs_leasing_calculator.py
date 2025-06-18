import streamlit as st
from loan_vs_leasing_logic import calculate_final_burden
from utils import format_number_gr

def loan_vs_leasing_ui():
    st.header("📊 Σύγκριση Δανείου vs Leasing")

    st.subheader("🔢 Εισαγωγή Δεδομένων")
    col1, col2 = st.columns(2)

    with col1:
        loan_rate = st.number_input("Επιτόκιο Δανείου (%)", value=6.0) / 100
        wc_rate = st.number_input("Επιτόκιο Κεφαλαίου Κίνησης (%)", value=8.0) / 100
        duration_years = st.number_input("Διάρκεια (έτη)", value=15)
        pay_when = st.radio("Πληρωμή στην αρχή ή στο τέλος;", ["Αρχή", "Τέλος"]) == "Αρχή"
        pay_when = 1 if pay_when else 0
        tax_rate = st.number_input("Φορολογικός Συντελεστής (%)", value=35.0) / 100

    with col2:
        property_value = st.number_input("Εμπορική Αξία Ακινήτου (€)", value=250000.0)
        loan_financing = st.number_input("Ποσοστό Χρηματοδότησης Δανείου (%)", value=70.0) / 100
        leasing_financing = st.number_input("Ποσοστό Χρηματοδότησης Leasing (%)", value=100.0) / 100
        add_expenses_loan = st.number_input("Επιπλέον Έξοδα Απόκτησης (Δάνειο)", value=35000.0)
        add_expenses_leasing = st.number_input("Επιπλέον Έξοδα Απόκτησης (Leasing)", value=30000.0)
        residual_value = st.number_input("Υπολειμματική Αξία Leasing (€)", value=3530.0)
        depreciation_years = st.number_input("Χρόνος Απόσβεσης (έτη)", value=30)

    st.subheader("📉 Υπολογισμός")

    final_loan, final_leasing = calculate_final_burden(
        loan_rate,
        wc_rate,
        duration_years,
        property_value,
        loan_financing,
        leasing_financing,
        add_expenses_loan,
        add_expenses_leasing,
        residual_value,
        depreciation_years,
        tax_rate,
        pay_when
    )

    col1, col2 = st.columns(2)
    col1.metric("📉 Τελική Επιβάρυνση Δανείου", f"{format_number_gr(final_loan)} €")
    col2.metric("📉 Τελική Επιβάρυνση Leasing", f"{format_number_gr(final_leasing)} €")

    st.write("---")
    st.markdown("✅ Η μικρότερη επιβάρυνση δείχνει την οικονομικά συμφερότερη επιλογή.")
