import streamlit as st
from utils import parse_gr_number, format_number_gr, format_percentage_gr

def calculate_cash_discount_efficiency(
    current_sales,
    extra_sales,
    discount_rate,
    discount_acceptance,
    discount_days,
    non_acceptance,
    non_discount_days,
    cash_days,
    cost_percent,
    wacc,
    suppliers_days,
    current_collection_days
):
    # Υπολογισμός απαιτήσεων πριν την έκπτωση
    current_receivables = (current_sales / 365) * current_collection_days

    # Υπολογισμός νέας μέσης περιόδου είσπραξης λόγω πολιτικής έκπτωσης
    new_collection_days_discounted = (discount_acceptance / 100) * discount_days + \
                                     (non_acceptance / 100) * non_discount_days
    new_receivables_discounted = (current_sales / 365) * new_collection_days_discounted
    capital_release_discounted = current_receivables - new_receivables_discounted

    # Νέες απαιτήσεις με επιπλέον πωλήσεις
    new_receivables_with_extra_sales = (extra_sales / 365) * new_collection_days_discounted

    # Τελική αποδέσμευση κεφαλαίων
    final_capital_release = capital_release_discounted - new_receivables_with_extra_sales

    # Κέρδος από επιπλέον πωλήσεις
    profit_from_extra_sales = extra_sales * (1 - cost_percent / 100)

    # Κέρδος από αποδέσμευση κεφαλαίου
    profit_from_release = final_capital_release * (wacc / 100)

    # Κόστος έκπτωσης
    discount_cost = (discount_rate / 100) * (discount_acceptance / 100) * (current_sales + extra_sales)

    # Καθαρή Παρούσα Αξία (NPV)
    npv = profit_from_extra_sales + profit_from_release - discount_cost

    # Υπολογισμός νέας συνολικής μέσης περιόδου είσπραξης (τρέχουσες + νέες πωλήσεις)
    total_sales = current_sales + extra_sales
    weighted_collection_days_total = (
        ((current_sales / total_sales) * new_collection_days_discounted) +
        ((extra_sales / total_sales) * new_collection_days_discounted)
    )

    # Υπολογισμός μέγιστης επιτρεπτής έκπτωσης (break-even)
    if (discount_acceptance * (current_sales + extra_sales)) > 0:
        max_discount_percent = 100 * (profit_from_extra_sales + profit_from_release) / \
                               (discount_acceptance / 100 * (current_sales + extra_sales))
    else:
        max_discount_percent = 0

    # Υπολογισμός βέλτιστης έκπτωσης (προσεγγιστικά, ως 80% της μέγιστης)
    optimal_discount_percent = 0.8 * max_discount_percent

    return {
        "current_receivables": current_receivables,
        "new_collection_days_discounted": new_collection_days_discounted,
        "new_receivables_discounted": new_receivables_discounted,
        "capital_release_discounted": capital_release_discounted,
        "customers_new_policy": discount_acceptance / 100,
        "total_new_collection_days": weighted_collection_days_total,
        "new_receivables_with_extra_sales": new_receivables_with_extra_sales,
        "final_capital_release": final_capital_release,
        "profit_from_extra_sales": profit_from_extra_sales,
        "profit_from_release": profit_from_release,
        "discount_cost": discount_cost,
        "npv": npv,
        "max_discount_percent": max_discount_percent,
        "optimal_discount_percent": optimal_discount_percent
    }


def discount_efficiency_ui():
    st.subheader("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς – Ανάλυση NPV")

    with st.form("discount_efficiency_form"):
        st.markdown("### Εισαγωγή Δεδομένων")

        col1, col2 = st.columns(2)

        with col1:
            current_sales = parse_gr_number(st.text_input("Τρέχουσες Πωλήσεις (€)", "1000"))
            extra_sales = parse_gr_number(st.text_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", "250"))
            discount_rate = parse_gr_number(st.text_input("Ποσοστό Έκπτωσης (%)", "2"))
            discount_acceptance = parse_gr_number(st.text_input("Ποσοστό Πελατών που Δέχεται την Έκπτωση (%)", "60"))
            discount_days = parse_gr_number(st.text_input("Ημέρες Είσπραξης με Έκπτωση", "60"))
            non_discount_days = parse_gr_number(st.text_input("Ημέρες Είσπραξης χωρίς Έκπτωση", "120"))

        with col2:
            cash_days = parse_gr_number(st.text_input("Ημέρες Πληρωμής Τοις Μετρητοίς", "10"))
            cost_percent = parse_gr_number(st.text_input("Μέσο Κόστος επί των Πωλήσεων (%)", "80"))
            wacc = parse_gr_number(st.text_input("Κόστος Κεφαλαίου (WACC %) ετησίως", "20"))
            suppliers_days = parse_gr_number(st.text_input("Μέση Περίοδος Πληρωμής Προμηθευτών", "30"))
            current_collection_days = parse_gr_number(st.text_input("Τρέχουσα Μέση Περίοδος Είσπραξης", "84"))

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        non_acceptance = 100 - discount_acceptance

        results = calculate_cash_discount_efficiency(
            current_sales,
            extra_sales,
            discount_rate,
            discount_acceptance,
            discount_days,
            non_acceptance,
            non_discount_days,
            cash_days,
            cost_percent,
            wacc,
            suppliers_days,
            current_collection_days
        )

        st.markdown("### Αποτελέσματα")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Τρέχουσες Απαιτήσεις (€)", format_number_gr(results["current_receivables"]))
            st.metric("Νέα Μέση Περίοδος Είσπραξης (με Έκπτωση)", format_number_gr(results["new_collection_days_discounted"]) + " ημέρες")
            st.metric("Νέες Απαιτήσεις (με Έκπτωση)", format_number_gr(results["new_receivables_discounted"]))
            st.metric("Αποδέσμευση Κεφαλαίων (παλιές πωλήσεις)", format_number_gr(results["capital_release_discounted"]))
            st.metric("% Πελατών με Νέα Πολιτική", format_percentage_gr(results["customers_new_policy"]))
            st.metric("Νέα Μέση Περίοδος Είσπραξης (σύνολο)", format_number_gr(results["total_new_collection_days"]) + " ημέρες")

        with col2:
            st.metric("Νέες Απαιτήσεις (με επιπλέον πωλήσεις)", format_number_gr(results["new_receivables_with_extra_sales"]))
            st.metric("Τελική Αποδέσμευση Κεφαλαίων", format_number_gr(results["final_capital_release"]))
            st.metric("Κέρδος από Επιπλέον Πωλήσεις", format_number_gr(results["profit_from_extra_sales"]))
            st.metric("Κέρδος από Αποδέσμευση Κεφαλαίων", format_number_gr(results["profit_from_release"]))
            st.metric("Κόστος Έκπτωσης", format_number_gr(results["discount_cost"]))
        
        st.markdown("---")
        st.markdown("### Υπολογισμός NPV & Ορίων Έκπτωσης")
        st.metric("Καθαρή Παρούσα Αξία (NPV)", format_number_gr(results["npv"]))
        st.metric("Μέγιστη Επιτρεπτή Έκπτωση για Break-Even (%)", format_percentage_gr(results["max_discount_percent"]))
        st.metric("Βέλτιστη Έκπτωση (%)", format_percentage_gr(results["optimal_discount_percent"]))
