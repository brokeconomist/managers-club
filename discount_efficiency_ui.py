import streamlit as st
from discount_efficiency_value import calculate_cash_discount_metrics
from utils import format_number_gr, parse_gr_number, format_percentage_gr

def show_discount_efficiency_ui():
    st.title("💶 Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    st.markdown("Εξετάστε αν μια έκπτωση τοις μετρητοίς οδηγεί σε **καθαρό όφελος** μέσω της αποδέσμευσης κεφαλαίου από τις απαιτήσεις.")

    with st.form("discount_form"):
        col1, col2 = st.columns(2)

        with col1:
            old_sales = parse_gr_number(st.text_input("📊 Τρέχουσες Πωλήσεις (€)", "100.000"))
            avg_days = parse_gr_number(st.text_input("📅 Τρέχουσες Ημέρες Είσπραξης", "45"))
            discount_rate = parse_gr_number(st.text_input("🔻 Προσφερόμενη Έκπτωση (%)", "2")) / 100

        with col2:
            new_sales = parse_gr_number(st.text_input("📈 Νέες Πωλήσεις (€)", "120.000"))
            new_avg_days = parse_gr_number(st.text_input("📆 Νέες Ημέρες Είσπραξης", "25"))
            cash_percent = parse_gr_number(st.text_input("💵 Ποσοστό Πελατών που Πληρώνουν Μετρητοίς (%)", "40")) / 100

        wacc = parse_gr_number(st.text_input("📉 Επιτόκιο / WACC (%)", "8")) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        result = calculate_cash_discount_metrics(
            old_sales, new_sales, avg_days, new_avg_days,
            discount_rate, cash_percent, wacc
        )

        st.success("✅ Υπολογισμοί Ολοκληρώθηκαν")

        st.subheader("📌 Αποτελέσματα")

        st.write(f"💰 **Αποδέσμευση Κεφαλαίου**: {format_number_gr(result['release'])} €")
        st.write(f"📈 **Όφελος από Αποδέσμευση (NPV)**: {format_number_gr(result['benefit'])} €")
        st.write(f"📉 **Ζημία λόγω Έκπτωσης**: {format_number_gr(result['loss'])} €")
        st.write(f"📊 **Καθαρό Όφελος (NPV)**: {format_number_gr(result['npv'])} €")

        st.subheader("🔍 Προτεινόμενα Όρια Έκπτωσης")
        st.write(f"💡 **Μέγιστη αποδεκτή έκπτωση**: {format_percentage_gr(result['max_discount'])}")
        st.write(f"📌 **Βέλτιστη έκπτωση (NPV = 0)**: {format_percentage_gr(result['optimal_discount'])}")
