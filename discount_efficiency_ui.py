import streamlit as st

# --------- ΥΠΟΛΟΓΙΣΤΙΚΗ ΣΥΝΑΡΤΗΣΗ ΜΕ ΤΥΠΟ BHATTACHARYA ---------
def calculate_discount_analysis_bhattacharya(
    current_sales,
    current_avg_collection,
    variable_cost,
    cash_discount_pct,
    pct_accept_discount,
    extra_sales,
    days_cash_payment,
    days_reject_discount,
    supplier_payment_days,
    wacc
):
    discount_rate_daily = wacc / 365
    g = extra_sales / current_sales if current_sales > 0 else 0
    y = variable_cost
    p = pct_accept_discount
    M = days_cash_payment
    Q = days_reject_discount
    N = current_avg_collection
    C = supplier_payment_days
    r = discount_rate_daily

    # --- Ενδιάμεσοι Υπολογισμοί ---
    current_receivables = current_sales * current_avg_collection / 365
    total_sales = current_sales + extra_sales
    discount_sales = (current_sales * pct_accept_discount) + extra_sales
    pct_follow_new_policy = discount_sales / total_sales if total_sales > 0 else 0
    new_avg_collection = M * pct_follow_new_policy + Q * (1 - pct_follow_new_policy)
    new_receivables = total_sales * new_avg_collection / 365
    released_capital = current_receivables - new_receivables
    profit_extra_sales = extra_sales * (1 - variable_cost)
    discount_cost = discount_sales * cash_discount_pct
    net_benefit = profit_extra_sales + released_capital * wacc - discount_cost

    try:
        denom = p * (1 + g)
        if denom == 0:
            max_discount = None
        else:
            max_discount = 1 - (1 + r)**(M - Q) * (
                (
                    1 - (1 / p)
                    + (1 + r)**(Q - N)
                    + y * g * (1 + r)**(Q - C)
                ) / denom
            )
    except ZeroDivisionError:
        max_discount = None

    return {
        "released_capital": released_capital,
        "profit_extra_sales": profit_extra_sales,
        "discount_cost": discount_cost,
        "net_benefit": net_benefit,
        "max_discount_break_even": max_discount
    }

# --------- UI ΜΕ STREAMLIT ---------
def format_number_gr(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(x):
    return f"{x*100:.2f}%".replace(".", ",")

def show_discount_efficiency_ui():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς (Bhattacharya Model)")

    with st.form("input_form"):
        col1, col2 = st.columns(2)
        with col1:
            current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=1000.0)
            extra_sales = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", value=250.0)
            variable_cost = st.number_input("Μεταβλητό Κόστος (0-1)", value=0.80)
            cash_discount_pct = st.number_input("Έκπτωση (%)", value=0.02)
            pct_accept_discount = st.number_input("% Πελατών που Δέχεται Έκπτωση (0-1)", value=0.60)

        with col2:
            days_cash_payment = st.number_input("Μέρες Πληρωμής με Έκπτωση", value=10)
            days_reject_discount = st.number_input("Μέρες Πληρωμής χωρίς Έκπτωση", value=120)
            current_avg_collection = st.number_input("Τρέχουσα Μέση Περίοδος Είσπραξης", value=84.0)
            supplier_payment_days = st.number_input("Μέρες Πληρωμής Προμηθευτών", value=30)
            wacc = st.number_input("WACC (0-1)", value=0.20)

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_discount_analysis_bhattacharya(
            current_sales,
            current_avg_collection,
            variable_cost,
            cash_discount_pct,
            pct_accept_discount,
            extra_sales,
            days_cash_payment,
            days_reject_discount,
            supplier_payment_days,
            wacc
        )

        st.subheader("Αποτελέσματα")

        st.write(f"**Αποδέσμευση Κεφαλαίου:** {format_number_gr(results['released_capital'])} €")
        st.write(f"**Κέρδος από Επιπλέον Πωλήσεις:** {format_number_gr(results['profit_extra_sales'])} €")
        st.write(f"**Κόστος Έκπτωσης:** {format_number_gr(results['discount_cost'])} €")
        st.write(f"**Καθαρό Όφελος (Net Benefit):** {format_number_gr(results['net_benefit'])} €")

        if results["max_discount_break_even"] is not None:
            st.success(f"**Μέγιστη Έκπτωση (Break-Even):** {format_percentage_gr(results['max_discount_break_even'])}")
        else:
            st.error("Η Μέγιστη Έκπτωση δεν μπορεί να υπολογιστεί λόγω μηδενικού παρονομαστή.")
