import streamlit as st

# --------- ΥΠΟΛΟΓΙΣΤΙΚΗ ΣΥΝΑΡΤΗΣΗ ---------
def calculate_cash_discount_analysis(
    current_sales,
    current_avg_collection,
    variable_cost,
    cash_discount_pct,
    pct_accept_discount,
    extra_sales,
    days_cash_payment,
    wacc
):
    discount_rate_daily = wacc / 365
    unit_margin = 1 - variable_cost

    current_receivables = current_sales * current_avg_collection / 365

    discount_sales = (current_sales * pct_accept_discount) + extra_sales
    total_sales = current_sales + extra_sales
    pct_follow_new_policy = discount_sales / total_sales if total_sales > 0 else 0

    new_avg_collection = (
        days_cash_payment * pct_follow_new_policy +
        current_avg_collection * (1 - pct_follow_new_policy)
    )

    new_receivables = total_sales * new_avg_collection / 365
    released_capital = current_receivables - new_receivables

    profit_extra_sales = extra_sales * unit_margin
    discount_cost = discount_sales * cash_discount_pct
    net_benefit = profit_extra_sales + released_capital * wacc - discount_cost

    if discount_sales > 0:
        max_discount_break_even = (profit_extra_sales + released_capital * wacc) / discount_sales
    else:
        max_discount_break_even = 0

    return {
        "discount_sales": discount_sales,
        "total_sales": total_sales,
        "pct_follow_new_policy": pct_follow_new_policy,
        "new_avg_collection": new_avg_collection,
        "released_capital": released_capital,
        "profit_extra_sales": profit_extra_sales,
        "discount_cost": discount_cost,
        "net_benefit": net_benefit,
        "max_discount_break_even": max_discount_break_even
    }

# --------- ΕΛΛΗΝΙΚΗ ΜΟΡΦΟΠΟΙΗΣΗ ---------
def format_number_gr(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(x):
    return f"{x*100:.1f}%".replace(".", ",")

def format_days(x):
    return f"{x:.1f} ημέρες".replace(".", ",")

# --------- UI ΜΕ STREAMLIT ---------
def main():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    st.markdown("Υπολογίζει αν συμφέρει η παροχή έκπτωσης για άμεση πληρωμή, λαμβάνοντας υπόψη αποδέσμευση κεφαλαίου και πρόσθετες πωλήσεις.")

    with st.form("input_form"):
        st.subheader("Εισαγωγή Δεδομένων")

        col1, col2 = st.columns(2)
        with col1:
            current_sales = st.number_input("Τρέχουσες ετήσιες πωλήσεις (€)", min_value=0.0, step=1000.0, format="%.2f")
            current_avg_collection = st.number_input("Μέσες ημέρες είσπραξης σήμερα", min_value=0.0, step=1.0, format="%.1f")
            variable_cost = st.number_input("Μεταβλητό κόστος (ποσοστό)", min_value=0.0, max_value=1.0, step=0.05, format="%.2f")

        with col2:
            cash_discount_pct = st.number_input("Προσφερόμενη έκπτωση (%)", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
            pct_accept_discount = st.number_input("Ποσοστό πελατών που αποδέχεται την έκπτωση", min_value=0.0, max_value=1.0, step=0.05, format="%.2f")
            extra_sales = st.number_input("Πρόσθετες ετήσιες πωλήσεις (€)", min_value=0.0, step=100.0, format="%.2f")

        col3, col4 = st.columns(2)
        with col3:
            days_cash_payment = st.number_input("Μέρες καθυστέρησης όσων πληρώνουν μετρητοίς", min_value=0.0, step=1.0, format="%.1f")
        with col4:
            wacc = st.number_input("Κόστος κεφαλαίου (WACC)", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_cash_discount_analysis(
            current_sales,
            current_avg_collection,
            variable_cost,
            cash_discount_pct,
            pct_accept_discount,
            extra_sales,
            days_cash_payment,
            wacc
        )

        st.subheader("Αποτελέσματα")

        st.metric("Πωλήσεις με έκπτωση", format_number_gr(results["discount_sales"]) + " €")
        st.metric("Νέος μέσος χρόνος είσπραξης", format_days(results["new_avg_collection"]))
        st.metric("Αποδέσμευση κεφαλαίου", format_number_gr(results["released_capital"]) + " €")
        st.metric("Κέρδος από πρόσθετες πωλήσεις", format_number_gr(results["profit_extra_sales"]) + " €")
        st.metric("Κόστος έκπτωσης", format_number_gr(results["discount_cost"]) + " €")
        st.metric("Καθαρό όφελος", format_number_gr(results["net_benefit"]) + " €")

        with st.expander("Οριακή έκπτωση ισοδυναμίας (break-even):"):
            st.write(f"Η μέγιστη αποδεκτή έκπτωση ώστε το καθαρό όφελος να μηδενιστεί είναι **{format_percentage_gr(results['max_discount_break_even'])}**.")

if __name__ == "__main__":
    main()
