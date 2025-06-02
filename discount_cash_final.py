import streamlit as st

# Συνάρτηση υπολογισμού - αυτή την εισάγεις κανονικά από cash_discount_calculator.py
def calculate_cash_discount(P3, P4, P9, P10, P11, P12, P13, P15, P20):
    r = P12 / 365
    ratio_extra_sales = P4 / P3

    term1 = 1 - (1 / P20)
    term2 = pow(1 + r, P9 - P15)
    term3 = P11 * ratio_extra_sales * pow(1 + r, P9 - P13)
    denom = P20 * (1 + ratio_extra_sales)

    max_discount = 1 - pow(1 + r, P10 - P9) * (term1 + (term2 + term3) / denom)
    optimal_discount = (1 - pow(1 + r, P10 - P15)) / 2

    return {
        "Max Discount": max_discount,
        "Optimal Discount": optimal_discount
    }

# Προαιρετικά: συνάρτηση υπολογισμού NPV με μέγιστη έκπτωση (μπορείς να την επεκτείνεις)
def calculate_npv(current_sales, extra_sales, cash_discount_rate, pct_customers_accept,
                  days_cash, days_reject, cost_of_sales_pct, wacc_annual,
                  avg_supplier_pay_days, current_collection_days):
    r = wacc_annual / 365
    ratio_extra_sales = extra_sales / current_sales

    # Απλοποιημένος υπολογισμός με βάση τα inputs (προσαρμόζεται ανάλογα)
    npv = (
        (current_sales * (1 - ratio_extra_sales) * (1 - cost_of_sales_pct)) +
        (extra_sales * (1 - cost_of_sales_pct) * (1 - cash_discount_rate)) * pct_customers_accept
    ) / (1 + r * (days_cash)) - (current_sales * cost_of_sales_pct)

    return npv

# Streamlit UI
st.title("Υπολογιστής Μέγιστης και Βέλτιστης Έκπτωσης Ταμειακών Πληρωμών")

st.markdown("Συμπλήρωσε τις παρακάτω παραμέτρους:")

P3 = st.number_input("Υφιστάμενες πωλήσεις (ποσότητα)", value=5000)
P4 = st.number_input("Επιπλέον πωλήσεις (ποσότητα)", value=2000)
P9 = st.number_input("Ημέρες είσπραξης μετά την έκπτωση", value=30)
P10 = st.number_input("Τρέχουσες ημέρες είσπραξης", value=60)
P11 = st.number_input("Μεταβλητό κόστος επιπλέον πωλήσεων (σε δεκαδικό, π.χ. 0.6)", value=0.6)
P12 = st.number_input("WACC (ετήσιο, π.χ. 0.12 για 12%)", value=0.12)
P13 = st.number_input("Ημέρες είσπραξης πελατών για τις αυξημένες πωλήσεις", value=30)
P15 = st.number_input("Ημέρες πληρωμής προμηθευτών", value=45)
P20 = st.number_input("Περιθώριο κέρδους (π.χ. 1.3)", value=1.3)

if st.button("Υπολόγισε Μέγιστη και Βέλτιστη Έκπτωση"):
    results = calculate_cash_discount(P3, P4, P9, P10, P11, P12, P13, P15, P20)
    max_disc = results["Max Discount"]
    opt_disc = results["Optimal Discount"]

    st.success(f"Μέγιστη Δυνητική Έκπτωση: {max_disc*100:.2f}%")
    st.success(f"Βέλτιστη Έκπτωση: {opt_disc*100:.2f}%")

    st.markdown("---")
    st.subheader("Προαιρετικός Υπολογισμός NPV με Μέγιστη Έκπτωση")

    pct_customers_accept = st.slider("Ποσοστό πελατών που αποδέχονται την έκπτωση", 0.0, 1.0, 0.6)
    days_cash = st.number_input("Μέρες είσπραξης πελατών με έκπτωση", value=15)
    cost_of_sales_pct = st.number_input("Κόστος πωλήσεων (ποσοστό, π.χ. 0.6)", value=0.6)

    if st.button("Υπολόγισε NPV"):
        npv = calculate_npv(
            current_sales=P3,
            extra_sales=P4,
            cash_discount_rate=max_disc,
            pct_customers_accept=pct_customers_accept,
            days_cash=days_cash,
            days_reject=P9,
            cost_of_sales_pct=cost_of_sales_pct,
            wacc_annual=P12,
            avg_supplier_pay_days=P15,
            current_collection_days=P10
        )
        st.success(f"NPV με Μέγιστη Έκπτωση: {npv:.2f}")
