import streamlit as st
from utils import format_number_gr, parse_gr_number, format_percentage_gr
from discount_efficiency import calculate_discount_efficiency

def discount_efficiency_ui():
    st.header("Αποδοτικότητα Πολιτικής Έκπτωσης με Ανάπτυξη Πωλήσεων")

    with st.form("discount_form"):
        col1, col2 = st.columns(2)

        with col1:
            current_sales = parse_gr_number(st.text_input("Τρέχουσες πωλήσεις (€)", "1.000"))
            extra_sales = parse_gr_number(st.text_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", "250"))
            discount_rate = st.number_input("Έκπτωση (%)", 0.0, 100.0, 2.0)
            pct_accepting = st.number_input("% πελατών που αποδέχονται την έκπτωση", 0.0, 100.0, 60.0)
            days_accepting = st.number_input("Μέρες πληρωμής αν αποδεχθούν την έκπτωση", 0, 365, 60)
            cost_pct = st.number_input("Κόστος πωλήσεων (%)", 0.0, 100.0, 80.0)

        with col2:
            pct_rejecting = st.number_input("% πελατών που δεν αποδέχονται", 0.0, 100.0, 40.0)
            days_rejecting = st.number_input("Μέρες πληρωμής αν δεν αποδεχθούν", 0, 365, 120)
            cash_days = st.number_input("Μέρες για πληρωμή τοις μετρητοίς", 0, 365, 10)
            wacc = st.number_input("Κόστος κεφαλαίου (WACC %)", 0.0, 100.0, 20.0)
            supplier_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών", 0, 365, 30)
            current_collection_days = st.number_input("Τρέχουσα μέση περίοδος είσπραξης", 0, 365, 84)

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_discount_efficiency(
            current_sales=current_sales,
            extra_sales=extra_sales,
            discount_rate=discount_rate,
            pct_accepting=pct_accepting,
            days_accepting=days_accepting,
            pct_rejecting=pct_rejecting,
            days_rejecting=days_rejecting,
            cash_days=cash_days,
            cost_pct=cost_pct,
            wacc=wacc,
            supplier_days=supplier_days,
            current_collection_days=current_collection_days
        )

        st.subheader("Αποτελέσματα")
        st.write(f"Μέση τρέχουσα περίοδος είσπραξης: {format_number_gr(results['current_avg_collection'])} μέρες")
        st.write(f"Τρέχουσες απαιτήσεις: {format_number_gr(results['current_receivables'])} €")
        st.write(f"Απαιτήσεις μετά νέα πολιτική χωρίς ανάπτυξη: {format_number_gr(results['new_receivables'])} €")
        st.write(f"Αποδέσμευση κεφαλαίων (χωρίς ανάπτυξη): {format_number_gr(results['release1'])} €")
        st.write(f"Ποσοστό πελατών με νέα πολιτική: {format_percentage_gr(results['pct_new_policy']*100)}")
        st.write(f"Μέση περίοδος είσπραξης μετά ανάπτυξη: {format_number_gr(results['avg_collection_after_growth'])} μέρες")
        st.write(f"Απαιτήσεις μετά νέα πολιτική με ανάπτυξη: {format_number_gr(results['receivables_after_growth'])} €")
        st.write(f"Αποδέσμευση κεφαλαίων (με ανάπτυξη): {format_number_gr(results['release2'])} €")
        st.write(f"Κέρδη από επιπλέον πωλήσεις: {format_number_gr(results['profit_extra_sales'])} €")
        st.write(f"Κέρδη από αποδέσμευση κεφαλαίων: {format_number_gr(results['release_profit'])} €")
        st.write(f"Κόστος έκπτωσης: {format_number_gr(results['discount_cost'])} €")
        st.write(f"Συνολικά κέρδη: {format_number_gr(results['total_profit'])} €")
        st.write(f"Καθαρή Παρούσα Αξία (NPV): {format_number_gr(results['npv'])} €")

        if results['break_even_discount'] is not None:
            st.write(f"Break-even Έκπτωση: {format_percentage_gr(results['break_even_discount']*100)}")
        else:
            st.write("Break-even Έκπτωση: Δεν υπολογίζεται")

        st.write(f"Βέλτιστη Έκπτωση (προσεγγιστικά): {format_percentage_gr(results['optimal_discount']*100)}")
