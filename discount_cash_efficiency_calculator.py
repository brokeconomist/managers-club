import streamlit as st
from cash_discount_efficiency_chart import calculate_discount_cash_efficiency
from utils import parse_gr_number

def cash_discount_efficiency():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    with st.form("cash_discount_form"):
        col1, col2 = st.columns(2)

        with col1:
            current_sales = parse_gr_number(st.text_input("Τρέχουσες πωλήσεις", "1.000"))
            extra_sales = parse_gr_number(st.text_input("Επιπλέον πωλήσεις λόγω έκπτωσης", "250"))
            discount_rate = parse_gr_number(st.text_input("Έκπτωση (%)", "2")) / 100
            pct_accepts_discount = parse_gr_number(st.text_input("% πελατών που αποδέχονται την έκπτωση", "60")) / 100
            pct_accepts_pays_in_days = parse_gr_number(st.text_input("Πληρωμή σε (μέρες) αν αποδεχθούν", "60"))
            pct_declines_discount = parse_gr_number(st.text_input("% πελατών που δεν αποδέχονται", "40")) / 100
            pct_declines_pays_in_days = parse_gr_number(st.text_input("Πληρωμή σε (μέρες) αν δεν αποδεχθούν", "120"))
            cash_days = parse_gr_number(st.text_input("Μέρες για πληρωμή τοις μετρητοίς", "10"))
            cost_pct = parse_gr_number(st.text_input("Κόστος πωλήσεων (%)", "80")) / 100
            wacc = parse_gr_number(st.text_input("Κόστος κεφαλαίου (%)", "20")) / 100
            supplier_payment_days = parse_gr_number(st.text_input("Μέση περίοδος αποπληρωμής προμηθευτών", "30"))

        with col2:
            current_collection_days = parse_gr_number(st.text_input("Τρέχουσα μέση περίοδος είσπραξης", "84"))
            current_receivables = parse_gr_number(st.text_input("Τρέχουσες απαιτήσεις", "230,14"))
            new_collection_days_discount = parse_gr_number(st.text_input("Νέα μέση περίοδος είσπραξης (με έκπτωση)", "54"))
            receivables_after_discount = parse_gr_number(st.text_input("Νέες απαιτήσεις (με έκπτωση)", "147,90"))
            release_discount = parse_gr_number(st.text_input("Αποδέσμευση κεφαλαίων (με έκπτωση)", "82,20"))
            pct_follows_new_policy = parse_gr_number(st.text_input("% πελατών με νέα πολιτική", "68")) / 100
            pct_old_policy = parse_gr_number(st.text_input("% πελατών με παλαιά πολιτική", "32")) / 100
            new_collection_days_total = parse_gr_number(st.text_input("Νέα μέση περίοδος είσπραξης (σύνολο)", "45"))
            receivables_after_increase = parse_gr_number(st.text_input("Απαιτήσεις μετά την αύξηση πωλήσεων", "155"))
            release_total = parse_gr_number(st.text_input("Αποδέσμευση κεφαλαίων (τελική)", "75,34"))
            profit_extra_sales = parse_gr_number(st.text_input("Κέρδος από επιπλέον πωλήσεις", "50"))
            profit_release = parse_gr_number(st.text_input("Κέρδος από αποδέσμευση κεφαλαίων", "15,07"))
            discount_cost = parse_gr_number(st.text_input("Κόστος έκπτωσης", "17"))

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_discount_cash_efficiency(
            current_sales,
            extra_sales,
            discount_rate,
            pct_accepts_discount,
            pct_accepts_pays_in_days,
            pct_declines_discount,
            pct_declines_pays_in_days,
            cash_days,
            cost_pct,
            wacc,
            supplier_payment_days,
            current_collection_days,
            current_receivables,
            new_collection_days_discount,
            receivables_after_discount,
            release_discount,
            pct_follows_new_policy,
            pct_old_policy,
            new_collection_days_total,
            receivables_after_increase,
            release_total,
            profit_extra_sales,
            profit_release,
            discount_cost
        )

        st.success("Αποτελέσματα:")
        for label, value in results.items():
            st.write(f"**{label}**: {value}")
