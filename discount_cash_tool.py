import streamlit as st

def calculate_discount_cash_tool(
    current_sales,
    additional_sales,
    discount_pct,
    pct_customers_accept,
    days_pay_discount,
    pct_customers_reject,
    days_pay_no_discount,
    days_pay_cash,
    cost_pct,
    capital_cost,
    avg_days_suppliers_payment,
    avg_days_receivable_current
):
    # Μετατροπή ποσοστών σε δεκαδικά
    discount = discount_pct / 100
    pct_accept = pct_customers_accept / 100
    pct_reject = pct_customers_reject / 100
    cost = cost_pct / 100
    capital_cost_rate = capital_cost / 100

    new_total_sales = current_sales + additional_sales

    # Προεξοφλητικοί παράγοντες για πληρωμή τοις μετρητοίς και χωρίς έκπτωση
    discount_factor_cash = 1 / (1 + (capital_cost_rate / 365)) ** days_pay_cash
    discount_factor_no_discount = 1 / (1 + (capital_cost_rate / 365)) ** days_pay_no_discount

    # Υπολογισμός παρούσας αξίας εισπράξεων με νέα πολιτική πληρωμών
    pv_receivables = (
        new_total_sales * pct_accept * (1 - discount) * discount_factor_cash
        + new_total_sales * pct_reject * discount_factor_no_discount
    )

    # Κόστος πωλήσεων αναλογικά με τις επιπλέον πωλήσεις
    cost_of_sales = cost * (additional_sales / current_sales) * current_sales

    # Προεξόφληση κόστους πωλήσεων με βάση μέση περίοδο αποπληρωμής προμηθευτών
    discount_factor_suppliers = 1 / (1 + (capital_cost_rate / 365)) ** avg_days_suppliers_payment
    pv_cost_of_sales = cost_of_sales * discount_factor_suppliers

    # Προεξόφληση τρεχουσών πωλήσεων με βάση τρέχουσα μέση περίοδο είσπραξης
    discount_factor_receivable_current = 1 / (1 + (capital_cost_rate / 365)) ** avg_days_receivable_current
    pv_current_sales = current_sales * discount_factor_receivable_current

    # Τελικός υπολογισμός ΚΠΑ
    npv = pv_receivables - pv_cost_of_sales - pv_current_sales

    # Κέρδος από επιπλέον πωλήσεις χωρίς έκπτωση (κόστος από επιπλέον πωλήσεις)
    profit_additional_sales = additional_sales * (1 - cost)

    # Μέγιστη έκπτωση break-even (όπως πριν)
    if additional_sales != 0:
        max_discount_break_even = profit_additional_sales / additional_sales
    else:
        max_discount_break_even = 0

    # Βέλτιστη έκπτωση 25% του μέγιστου
    optimal_discount = max_discount_break_even * 0.25

    # Μετατροπή σε ποσοστά
    max_discount_break_even_pct = max_discount_break_even * 100
    optimal_discount_pct = optimal_discount * 100

    # Υπολογισμός αποδέσμευσης κεφαλαίου (όπως πριν)
    avg_days_before = pct_accept * days_pay_discount + pct_reject * days_pay_no_discount
    capital_before = current_sales * cost * avg_days_before / 365
    capital_after = new_total_sales * cost * avg_days_before / 365
    released_capital = capital_before - capital_after

    return {
        "profit_additional_sales": profit_additional_sales,
        "released_capital": released_capital,
        "npv": npv,
        "max_discount_break_even_pct": max_discount_break_even_pct,
        "optimal_discount_pct": optimal_discount_pct,
    }

def show_discount_cash_tool():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    st.markdown("Υπολογισμός καθαρής παρούσας αξίας (ΚΠΑ) και βέλτιστης έκπτωσης με βάση τα δεδομένα πληρωμών και πωλήσεων.")

    current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", min_value=0.0, value=1000.0, step=100.0)
    additional_sales = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", min_value=0.0, value=250.0, step=10.0)
    discount_pct = st.number_input("Έκπτωση για Πληρωμή Τοις Μετρητοίς (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1)
    pct_customers_accept = st.number_input("% Πελατών που Αποδέχεται την Έκπτωση (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    days_pay_discount = st.number_input("Μέρες Πληρωμής Πελατών με Έκπτωση", min_value=0, max_value=365, value=60, step=1)
    pct_customers_reject = st.number_input("% Πελατών που ΔΕΝ Αποδέχεται την Έκπτωση (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    days_pay_no_discount = st.number_input("Μέρες Πληρωμής Πελατών χωρίς Έκπτωση", min_value=0, max_value=365, value=120, step=1)
    days_pay_cash = st.number_input("Μέρες για Πληρωμή Τοις Μετρητοίς", min_value=0, max_value=365, value=10, step=1)
    cost_pct = st.number_input("Κόστος Πωλήσεων σε %", min_value=0.0, max_value=100.0, value=80.0, step=0.1)
    capital_cost = st.number_input("Κόστος Κεφαλαίου σε %", min_value=0.0, max_value=100.0, value=20.0, step=0.1)

    if st.button("Υπολόγισε ΚΠΑ και Έκπτωση"):
        results = calculate_discount_cash_tool(
            current_sales=current_sales,
            additional_sales=additional_sales,
            discount_pct=discount_pct,
            pct_customers_accept=pct_customers_accept,
            days_pay_discount=days_pay_discount,
            pct_customers_reject=pct_customers_reject,
            days_pay_no_discount=days_pay_no_discount,
            days_pay_cash=days_pay_cash,
            cost_pct=cost_pct,
            capital_cost=capital_cost
        )

        st.subheader("Αποτελέσματα")
        st.write(f"Κέρδος από επιπλέον πωλήσεις: €{results['profit_additional_sales']:.2f}")
        # Αφαιρέθηκε η γραμμή με το released_capital
        st.write(f"Καθαρή Παρούσα Αξία (NPV): €{results['npv']:.2f}")
        st.write(f"Μέγιστη έκπτωση Break Even: {results['max_discount_break_even_pct']:.2f} %")
        st.write(f"Προτεινόμενη βέλτιστη έκπτωση: {results['optimal_discount_pct']:.2f} %")
