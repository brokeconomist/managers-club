import streamlit as st
from utils import format_number_gr, parse_gr_number, format_percentage_gr

def calculate_discount_efficiency(
    current_sales, extra_sales, discount_rate, pct_accepting, days_accepting,
    pct_rejecting, days_rejecting, cash_days, cost_pct, wacc, supplier_days
):
    pct_accepting /= 100
    pct_rejecting /= 100
    discount_rate /= 100
    cost_pct /= 100
    wacc /= 100

    # Αρχικές παράμετροι
    current_avg_collection = days_accepting * pct_accepting + days_rejecting * pct_rejecting
    current_receivables = current_sales * current_avg_collection / 365

    # Νέα πολιτική χωρίς αύξηση πωλήσεων
    new_avg_collection = cash_days * pct_accepting + days_rejecting * pct_rejecting
    new_receivables = current_sales * new_avg_collection / 365
    release1 = current_receivables - new_receivables

    # Με αύξηση πωλήσεων
    total_sales = current_sales + extra_sales
    pct_new_policy = ((current_sales * pct_accepting) + extra_sales) / total_sales
    pct_old_policy = 1 - pct_new_policy

    avg_collection_after_growth = pct_new_policy * cash_days + pct_old_policy * days_rejecting
    receivables_after_growth = total_sales * avg_collection_after_growth / 365
    release2 = current_receivables - receivables_after_growth

    # Κέρδη
    profit_extra_sales = extra_sales * (1 - cost_pct)
    release_profit = release2 * wacc
    discount_cost = total_sales * pct_new_policy * discount_rate
    total_profit = profit_extra_sales + release_profit - discount_cost

    # NPV
    factor_accepting = 1 / ((1 + (wacc / 365)) ** cash_days)
    factor_rejecting = 1 / ((1 + (wacc / 365)) ** days_rejecting)
    factor_suppliers = 1 / ((1 + (wacc / 365)) ** supplier_days)
    factor_old = 1 / ((1 + (wacc / 365)) ** current_avg_collection)

    npv = (
        total_sales * pct_new_policy * (1 - discount_rate) * factor_accepting +
        total_sales * (1 - pct_new_policy) * factor_rejecting -
        cost_pct * (extra_sales / current_sales) * current_sales * factor_suppliers -
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
        break_even_discount = 0

    # Βέλτιστη έκπτωση
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

def discount_efficiency_ui():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς με Παράλληλη Αύξηση Πωλήσεων")

    col1, col2 = st.columns(2)
    with col1:
        current_sales = parse_gr_number(st.number_input("Τρέχουσες πωλήσεις", value=1000.0))
        extra_sales = parse_gr_number(st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης", value=250.0))
        discount_rate = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0)
        pct_accepting = st.number_input("% των πελατών που αποδέχεται την έκπτωση", value=50.0)
        days_accepting = st.number_input("Μέρες πληρωμής για όσους αποδέχονται", value=60)
        cash_days = st.number_input("Μέρες πληρωμής μετρητοίς", value=10)
        cost_pct = st.number_input("Κόστος πωλήσεων (%)", value=80.0)

    with col2:
        pct_rejecting = st.number_input("% των πελατών που δεν αποδέχεται την έκπτωση", value=50.0)
        days_rejecting = st.number_input("Μέρες πληρωμής για όσους δεν αποδέχονται", value=120)
        wacc = st.number_input("Κόστος κεφαλαίου (WACC) (%)", value=20.0)
        supplier_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών", value=30.0)

    if st.button("Υπολογισμός"):
        results = calculate_discount_efficiency(
            current_sales, extra_sales, discount_rate, pct_accepting, days_accepting,
            pct_rejecting, days_rejecting, cash_days, cost_pct, wacc, supplier_days
        )

        st.subheader("Αποτελέσματα:")
        st.write("Τρέχουσες απαιτήσεις:", format_number_gr(results["current_receivables"]))
        st.write("Νέες απαιτήσεις μετά την έκπτωση:", format_number_gr(results["new_receivables"]))
        st.write("Αποδέσμευση κεφαλαίων:", format_number_gr(results["release2"]))
        st.write("Κέρδος από επιπλέον πωλήσεις:", format_number_gr(results["profit_extra_sales"]))
        st.write("Κέρδος αποδέσμευσης:", format_number_gr(results["release_profit"]))
        st.write("Κόστος έκπτωσης:", format_number_gr(results["discount_cost"]))
        st.write("Συνολικό καθαρό κέρδος:", format_number_gr(results["total_profit"]))
        st.write("NPV:", format_number_gr(results["npv"]))
        st.write("Μέγιστη αποδεκτή έκπτωση (NPV break-even):", format_percentage_gr(results["break_even_discount"]))
        st.write("Βέλτιστη έκπτωση:", format_percentage_gr(results["optimal_discount"]))
