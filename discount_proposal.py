import streamlit as st
from discount_proposal_logic import calculate_discount_analysis
from utils import parse_gr_number, format_number_gr, format_percentage_gr

def show_discount_proposal_ui():
    st.header("💸 Ανάλυση Πρότασης Έκπτωσης Τοις Μετρητοίς")

    st.markdown("""
    Η ανάλυση υπολογίζει αν μια έκπτωση για πληρωμή τοις μετρητοίς οδηγεί σε συνολικό οικονομικό όφελος,
    λαμβάνοντας υπόψη τις επιπλέον πωλήσεις, τη μείωση επισφαλειών, την αποδέσμευση κεφαλαίων και το κόστος της έκπτωσης.
    """)

    with st.form("discount_form"):
        st.subheader("📥 Είσοδοι")

        col1, col2 = st.columns(2)

        with col1:
            current_sales = parse_gr_number(st.text_input("Τρέχουσες Πωλήσεις (€)", "1.000"))
            cogs = parse_gr_number(st.text_input("Κόστος Πωλήσεων (€)", "800"))
            extra_sales = parse_gr_number(st.text_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", "250"))
            discount_rate = parse_gr_number(st.text_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", "2")) / 100
            share_discount_before = parse_gr_number(st.text_input("Ποσοστό Πωλήσεων με Έκπτωση (πριν)", "40")) / 100
            share_no_discount_before = parse_gr_number(st.text_input("Ποσοστό Πωλήσεων χωρίς Έκπτωση (πριν)", "60")) / 100
            days_discount_before = parse_gr_number(st.text_input("Μέρες είσπραξης με Έκπτωση (πριν)", "30"))
            days_no_discount_before = parse_gr_number(st.text_input("Μέρες είσπραξης χωρίς Έκπτωση (πριν)", "60"))
            supplier_payment_days = parse_gr_number(st.text_input("Μέρες πληρωμής προμηθευτών", "30"))

        with col2:
            days_discount_after = parse_gr_number(st.text_input("Μέρες πληρωμής μετρητοίς (μετά)", "10"))
            share_discount_after = parse_gr_number(st.text_input("Ποσοστό Πωλήσεων με Έκπτωση (μετά)", "70")) / 100
            share_no_discount_after = parse_gr_number(st.text_input("Ποσοστό Πωλήσεων χωρίς Έκπτωση (μετά)", "30")) / 100
            days_no_discount_after = parse_gr_number(st.text_input("Μέρες είσπραξης χωρίς Έκπτωση (μετά)", "60"))
            bad_debt_rate = parse_gr_number(st.text_input("% Επισφαλειών (τρέχον)", "1")) / 100
            bad_debt_reduction_rate = parse_gr_number(st.text_input("% Επισφαλειών (μετά την αλλαγή)", "0.5")) / 100
            wacc = parse_gr_number(st.text_input("Κόστος Κεφαλαίου (WACC, %)", "20")) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        result = calculate_discount_analysis(
            current_sales,
            cogs,
            extra_sales,
            discount_rate,
            share_discount_before,
            share_no_discount_before,
            days_discount_before,
            days_no_discount_before,
            days_discount_after,
            share_discount_after,
            share_no_discount_after,
            days_no_discount_after,
            bad_debt_rate,
            bad_debt_reduction_rate,
            wacc,
            supplier_payment_days
        )

        st.subheader("📊 Αποτελέσματα")

        st.markdown(f"• **Μέση περίοδος είσπραξης (πριν):** {format_number_gr(result['avg_days_before'])} ημέρες")
        st.markdown(f"• **Μέση περίοδος είσπραξης (μετά):** {format_number_gr(result['avg_days_after'])} ημέρες")
        st.markdown(f"• **Αποδέσμευση Κεφαλαίων:** {format_number_gr(result['capital_release'])} €")
        st.markdown(f"• **Κέρδος από επιπλέον πωλήσεις:** {format_number_gr(result['profit_extra_sales'])} €")
        st.markdown(f"• **Κέρδος από αποδέσμευση κεφαλαίων:** {format_number_gr(result['profit_from_release'])} €")
        st.markdown(f"• **Κέρδος από μείωση επισφαλειών:** {format_number_gr(result['profit_from_risk_reduction'])} €")
        st.markdown(f"• **Κόστος έκπτωσης:** {format_number_gr(result['discount_cost'])} €")
        st.success(f"🧾 **Καθαρό όφελος από την πρόταση:** {format_number_gr(result['total_profit'])} €")

        st.markdown("---")
        st.subheader("📌 Εκπτώσεις")
        st.markdown(f"• **Μέγιστη αποδεκτή έκπτωση (Dmax):** {format_percentage_gr(result['dmax'])}")
        st.markdown(f"• **Προτεινόμενη έκπτωση (ασφαλής):** {format_percentage_gr(result['suggested_discount'])}")
