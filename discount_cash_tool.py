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
    capital_cost
):
    # Μετατροπή ποσοστών σε δεκαδικά
    discount = discount_pct / 100
    pct_accept = pct_customers_accept / 100
    pct_reject = pct_customers_reject / 100
    cost = cost_pct / 100
    capital_cost_rate = capital_cost / 100

    # Κέρδος από επιπλέον πωλήσεις χωρίς έκπτωση (κόστος από επιπλέον πωλήσεις)
    profit_additional_sales = additional_sales * (1 - cost)

    # Νέο σύνολο πωλήσεων μετά την αύξηση
    new_total_sales = current_sales + additional_sales

    # Μέση περίοδος είσπραξης πριν
    avg_days_before = pct_accept * days_pay_discount + pct_reject * days_pay_no_discount

    # Μέση περίοδος είσπραξης μετά την εφαρμογή της έκπτωσης (λαμβάνοντας υπόψη και το % πελατών που θα ακολουθήσουν τη νέα πολιτική)
    avg_days_after = (pct_accept * days_pay_discount + pct_reject * days_pay_no_discount)  # χωρίς % πελατών που ακολουθούν νέα πολιτική

    # *** ΑΦΑΙΡΕΜΕΝΟ το κομμάτι αποδέσμευσης κεφαλαίων ***

    # Υπολογισμός NPV (προεξόφληση κεφαλαίου)
    # Θα υπολογίσουμε NPV μόνο ως κέρδος προεξόφλησης έκπτωσης επί επιπλέον πωλήσεις

    # Ας υποθέσουμε NPV σαν κέρδος από μείωση εκπτώσεων (απλοποιημένο παράδειγμα):
    npv = profit_additional_sales * capital_cost_rate  # απλοποιημένος υπολογισμός

    # Μέγιστη έκπτωση που ισοσκελίζει το NPV (Break-Even discount)
    if additional_sales != 0:
        max_discount_break_even = profit_additional_sales / additional_sales
    else:
        max_discount_break_even = 0

    # Βέλτιστη έκπτωση: 25% του μέγιστου
    optimal_discount = max_discount_break_even * 0.25

    max_discount_break_even_pct = max_discount_break_even * 100
    optimal_discount_pct = optimal_discount * 100

    return {
        "profit_additional_sales": profit_additional_sales,
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
