import streamlit as st
from decimal import Decimal, getcontext

# Ακρίβεια για Decimal υπολογισμούς
getcontext().prec = 20

def format_percentage_gr(value, decimals=2):
    if value is None:
        return "-"
    sign = "-" if value < 0 else ""
    abs_val = abs(value * 100)
    formatted = f"{abs_val:,.{decimals}f}".replace(",", "#").replace(".", ",").replace("#", ".")
    return f"{sign}{formatted}%"

def format_number_gr(value, decimals=2):
    return f"{value:,.{decimals}f}".replace(",", "#").replace(".", ",").replace("#", ".")

def show_discount_efficiency_ui():
    st.title("Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς")

    st.markdown("### Εισαγωγή Δεδομένων")
    col1, col2 = st.columns(2)

    with col1:
        current_sales = st.number_input("Τρέχουσες πωλήσεις", value=1000, step=1, format="%d")
        extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης", value=250, step=1, format="%d")
        cash_discount_pct = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0) / 100
        pct_accept_discount = st.number_input("% πελατών που αποδέχεται την έκπτωση", value=60.0) / 100
        days_accept_discount = st.number_input("Μέρες που πληρώνουν όσοι αποδέχονται την έκπτωση", value=60)

    with col2:
        pct_reject_discount = st.number_input("% πελατών που δεν αποδέχεται την έκπτωση", value=40.0) / 100
        days_reject_discount = st.number_input("Μέρες που πληρώνουν όσοι δεν αποδέχονται την έκπτωση", value=120)
        days_cash_payment = st.number_input("Μέρες για πληρωμή τοις μετρητοίς", value=10)
        cost_of_sales_pct = st.number_input("Κόστος πωλήσεων σε %", value=80.0) / 100
        wacc = st.number_input("Κόστος κεφαλαίου (WACC) σε %", value=20.0) / 100
        supplier_payment_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών", value=30)

    st.markdown("---")

    # Υπολογισμοί με Decimal
    cs = Decimal(str(current_sales))
    es = Decimal(str(extra_sales))
    t_sales = cs + es
    discount = Decimal(str(cash_discount_pct))
    acc = Decimal(str(pct_accept_discount))
    rej = Decimal(str(pct_reject_discount))
    days_acc = Decimal(str(days_accept_discount))
    days_rej = Decimal(str(days_reject_discount))
    days_cash = Decimal(str(days_cash_payment))
    cost_pct = Decimal(str(cost_of_sales_pct))
    wacc_d = Decimal(str(wacc))
    spd = Decimal(str(supplier_payment_days))

    d_rate = wacc_d / Decimal('365')
    base = Decimal('1') + d_rate

    # Τρέχουσα μέση είσπραξη & απαιτήσεις
    current_avg_collection = acc * days_acc + rej * days_rej
    current_receivables = cs * current_avg_collection / Decimal('365')

    # Νέες μέσες περίοδοι
    pct_follow_policy = ((cs * acc) + es) / (cs + es)
    pct_old_policy = Decimal('1') - pct_follow_policy
    new_avg_collection = pct_follow_policy * days_cash + pct_old_policy * days_rej
    new_receivables = t_sales * new_avg_collection / Decimal('365')
    released_capital = current_receivables - new_receivables

    # Κέρδη/κόστη
    profit_extra_sales = es * (Decimal('1') - cost_pct)
    value_of_released_capital = released_capital * wacc_d
    discount_cost = t_sales * pct_follow_policy * discount

    # NPV
    npv = (
        t_sales * pct_follow_policy * (Decimal('1') - discount) / (base ** days_cash) +
        t_sales * pct_old_policy / (base ** days_rej) -
        cost_pct * es / (base ** spd) -
        cs / (base ** current_avg_collection)
    )

    # Κέρδος από επισφάλειες (αν υποθέσουμε 2% πριν και 1% μετά)
    bad_debt_current = cs * Decimal('0.02')
    bad_debt_new = t_sales * Decimal('0.01')
    bad_debt_gain = bad_debt_current - bad_debt_new

    # Βέλτιστη έκπτωση
    optimal_discount = (Decimal('1') - base ** (days_cash - current_avg_collection)) / Decimal('2')

    # Τελικό NPV με επισφάλειες
    npv_total = npv + bad_debt_gain

    # Εμφάνιση αποτελεσμάτων
    st.header("Αποτελέσματα")
    st.write(f"Τρέχουσα μέση περίοδος είσπραξης: {current_avg_collection:.2f} ημέρες")
    st.write(f"Τρέχουσες απαιτήσεις: {format_number_gr(current_receivables)} €")
    st.write(f"Νέα μέση περίοδος είσπραξης: {new_avg_collection:.2f} ημέρες")
    st.write(f"Νέες απαιτήσεις: {format_number_gr(new_receivables)} €")
    st.write(f"Αποδέσμευση κεφαλαίων: {format_number_gr(released_capital)} €")
    st.write(f"Κέρδος από επιπλέον πωλήσεις: {format_number_gr(profit_extra_sales)} €")
    st.write(f"Κέρδος από αποδέσμευση κεφαλαίων: {format_number_gr(value_of_released_capital)} €")
    st.write(f"Κόστος έκπτωσης: {format_number_gr(discount_cost)} €")
    st.write(f"Κέρδος από μείωση επισφαλειών: {format_number_gr(bad_debt_gain)} €")
    st.write(f"Καθαρή Παρούσα Αξία (NPV): {format_number_gr(npv)} €")
    st.write(f"Συνολικό NPV (με επισφάλειες): {format_number_gr(npv_total)} €")
    st.write(f"Βέλτιστη έκπτωση που πρέπει να δοθεί: {format_percentage_gr(float(optimal_discount))}")
