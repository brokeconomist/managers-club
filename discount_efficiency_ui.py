import streamlit as st

def format_number_gr(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(x):
    return f"{x * 100:.2f}%".replace(".", ",")

def show_discount_efficiency_ui():
    st.title("Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς")

    col1, col2 = st.columns(2)

    with col1:
        current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", value=1000.0, step=10.0)
        extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", value=250.0, step=10.0)
        variable_cost_pct = st.number_input("Κόστος πωλήσεων (%)", value=80.0, min_value=0.0, max_value=100.0) / 100
        pct_accept_discount = st.number_input("% πελατών που αποδέχεται την έκπτωση", value=60.0, min_value=0.1, max_value=100.0) / 100
        days_cash_payment = st.number_input("Μέρες πληρωμής με έκπτωση", value=10, step=1)

    with col2:
        days_reject_discount = st.number_input("Μέρες πληρωμής χωρίς έκπτωση", value=120, step=1)
        current_avg_collection = st.number_input("Τρέχουσα μέση περίοδος είσπραξης", value=84.0, step=1.0)
        supplier_payment_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών", value=30, step=1)
        wacc = st.number_input("Κόστος κεφαλαίου (WACC %)", value=20.0, min_value=0.0, max_value=100.0) / 100
        discount_pct = st.number_input("Εφαρμοζόμενη έκπτωση (%)", value=2.0, min_value=0.0, max_value=100.0) / 100

    st.markdown("---")

    # Ορισμοί
    try:
        r = wacc / 365
        g = extra_sales / current_sales if current_sales > 0 else 0
        y = variable_cost_pct
        p = pct_accept_discount
        M = days_cash_payment
        Q = days_reject_discount
        N = current_avg_collection
        C = supplier_payment_days

        # Μέγιστη Έκπτωση
        numerator = (1 - (1 / p)) + (1 + r) ** (Q - N) + y * g * (1 + r) ** (Q - C)
        denominator = p * (1 + g)
        base = (1 + r) ** (M - Q)
        max_discount = 1 - base * (numerator / denominator)

        # NPV (σύμφωνα με τον τύπο σου από Excel)
        term_1 = (current_sales + extra_sales) * p * (1 - discount_pct) * (1 / (1 + r) ** M)
        term_2 = (current_sales + extra_sales) * (1 - p) * (1 / (1 + r) ** Q)
        term_3 = variable_cost_pct * (extra_sales / current_sales) * current_sales * (1 / (1 + r) ** C)
        term_4 = current_sales * (1 / (1 + r) ** N)
        npv = term_1 + term_2 - term_3 - term_4

        # Κέρδος από επιπλέον πωλήσεις
        profit_extra = extra_sales * (1 - variable_cost_pct)

        # Νέα μέση περίοδος είσπραξης
        new_avg_collection = p * M + (1 - p) * Q
        total_receivables_now = current_sales * current_avg_collection / 365
        total_receivables_after = (current_sales + extra_sales) * new_avg_collection / 365
        released_capital = total_receivables_now - total_receivables_after

        capital_profit = released_capital * wacc
        discount_cost = extra_sales * p * discount_pct
        net_benefit = profit_extra + capital_profit - discount_cost

    except Exception as e:
        max_discount = None
        npv = None
        net_benefit = None

    # Εμφάνιση
    st.subheader("Αποτελέσματα")

    if max_discount is not None:
        st.write(f"**Μέγιστη έκπτωση (NPV Break Even) επί των επιπλέον πωλήσεων:** {format_percentage_gr(max_discount)}")
    if npv is not None:
        st.write(f"**NPV:** {format_number_gr(npv)} €")
    if net_benefit is not None:
        st.write(f"**Καθαρό όφελος (Net Benefit):** {format_number_gr(net_benefit)} €")
