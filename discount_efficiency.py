def calculate_discount_efficiency(
    current_sales, extra_sales, discount_rate, pct_accepting, days_accepting,
    pct_rejecting, days_rejecting, cash_days, cost_pct, wacc, supplier_days,
    current_collection_days=None
):
    # Μετατροπή ποσοστών σε δεκαδικά
    pct_accepting /= 100
    pct_rejecting /= 100
    discount_rate /= 100
    cost_pct /= 100
    wacc /= 100

    # Αν δεν δώθηκε τρέχουσα μέση περίοδος είσπραξης, υπολογίζουμε
    if current_collection_days is None:
        current_avg_collection = days_accepting * pct_accepting + days_rejecting * pct_rejecting
    else:
        current_avg_collection = current_collection_days
    current_receivables = current_sales * current_avg_collection / 365

    # Νέα πολιτική χωρίς αύξηση πωλήσεων (μετρητοίς για αποδεκτικούς)
    new_avg_collection = cash_days * pct_accepting + days_rejecting * pct_rejecting
    new_receivables = current_sales * new_avg_collection / 365
    release1 = current_receivables - new_receivables

    # Νέα πολιτική με αύξηση πωλήσεων
    total_sales = current_sales + extra_sales
    pct_new_policy = ((current_sales * pct_accepting) + extra_sales) / total_sales if total_sales != 0 else 0
    pct_old_policy = 1 - pct_new_policy

    avg_collection_after_growth = pct_new_policy * cash_days + pct_old_policy * days_rejecting
    receivables_after_growth = total_sales * avg_collection_after_growth / 365
    release2 = current_receivables - receivables_after_growth

    # Κέρδη από επιπλέον πωλήσεις και αποδέσμευση κεφαλαίων
    profit_extra_sales = extra_sales * (1 - cost_pct)
    release_profit = release2 * wacc
    discount_cost = total_sales * pct_new_policy * discount_rate
    total_profit = profit_extra_sales + release_profit - discount_cost

    # Παράγοντες προεξόφλησης
    factor_accepting = 1 / ((1 + (wacc / 365)) ** cash_days)
    factor_rejecting = 1 / ((1 + (wacc / 365)) ** days_rejecting)
    factor_suppliers = 1 / ((1 + (wacc / 365)) ** supplier_days)
    factor_old = 1 / ((1 + (wacc / 365)) ** current_avg_collection)

    # Καθαρή παρούσα αξία (NPV)
    npv = (
        total_sales * pct_new_policy * (1 - discount_rate) * factor_accepting +
        total_sales * (1 - pct_new_policy) * factor_rejecting -
        cost_pct * extra_sales * factor_suppliers -
        current_sales * factor_old
    )

    # Break-even έκπτωση
    try:
        break_even_discount = 1 - (
            (1 + (wacc / 365)) ** (cash_days - days_rejecting) *
            (
                (1 - (1 / pct_new_policy)) +
                ((1 + (wacc / 365)) ** (days_rejecting - current_avg_collection) +
                 cost_pct * (extra_sales / current_sales) * ((1 + (wacc / 365)) ** (days_rejecting - supplier_days)))
                / (pct_new_policy * (1 + (extra_sales / current_sales)))
            )
        )
    except ZeroDivisionError:
        break_even_discount = None

    # Βέλτιστη έκπτωση (προσέγγιση)
    optimal_discount = (1 - ((1 + (wacc / 365)) ** (cash_days - current_avg_collection))) / 2

    return {
        "current_avg_collection": current_avg_collection,
        "current_receivables": current_receivables,
        "new_avg_collection": new_avg_collection,
        "new_receivables": new_receivables,
        "release1": release1,
        "pct_new_policy": pct_new_policy,
        "pct_old_policy": pct_old_policy,
        "avg_collection_after_growth": avg_collection_after_growth,
        "receivables_after_growth": receivables_after_growth,
        "release2": release2,
        "profit_extra_sales": profit_extra_sales,
        "release_profit": release_profit,
        "discount_cost": discount_cost,
        "total_profit": total_profit,
        "npv": npv,
        "break_even_discount": break_even_discount,
        "optimal_discount": optimal_discount
    }
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
            discount_acceptance = st.number_input("% πελατών που αποδέχονται την έκπτωση", 0.0, 100.0, 60.0)
            payment_days_accept = st.number_input("Μέρες πληρωμής αν αποδεχθούν την έκπτωση", 0, 365, 60)
            cost_percent = st.number_input("Κόστος πωλήσεων (%)", 0.0, 100.0, 80.0)

        with col2:
            non_acceptance = st.number_input("% πελατών που δεν αποδέχονται", 0.0, 100.0, 40.0)
            non_discount_days = st.number_input("Μέρες πληρωμής αν δεν αποδεχθούν", 0, 365, 120)
            discount_days = st.number_input("Μέρες για πληρωμή τοις μετρητοίς", 0, 365, 10)
            wacc = st.number_input("Κόστος κεφαλαίου (WACC %)", 0.0, 100.0, 20.0)
            suppliers_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών", 0, 365, 30)
            current_collection_days = st.number_input("Τρέχουσα μέση περίοδος είσπραξης", 0, 365, 84)

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_discount_efficiency(
            current_sales,
            extra_sales,
            discount_rate,
            discount_acceptance,
            payment_days_accept,
            non_acceptance,
            non_discount_days,
            discount_days,
            cost_percent,
            wacc,
            suppliers_days,
            current_collection_days
        )

        st.subheader("Αποτελέσματα")

        st.write(f"**Καθαρή Παρούσα Αξία (NPV)**: {format_number_gr(results['npv'])} €")

        if results["break_even_discount"] is not None:
            st.write(f"**Μέγιστη έκπτωση για μηδενική NPV (Break-even)**: {format_percentage_gr(results['break_even_discount'])}")
        else:
            st.write("**Μέγιστη έκπτωση**: Δεν μπορεί να υπολογιστεί (πιθανό μηδενισμός).")

        st.write(f"**Βέλτιστη έκπτωση (προσέγγιση)**: {format_percentage_gr(results['optimal_discount'])}")
