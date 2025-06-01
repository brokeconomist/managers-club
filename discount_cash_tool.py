import streamlit as st
from utils import format_number_gr, format_percentage_gr

def show_discount_cash_tool():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    st.markdown("#### Εισαγωγή Παραμέτρων")

    current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    extra_sales = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", min_value=0.0, value=250.0, step=50.0, format="%.2f")
    cash_discount_rate = st.number_input("Ποσοστό Έκπτωσης (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.5, format="%.2f") / 100
    pct_customers_discount_total = st.number_input("Ποσοστό Πελατών που Πληρώνουν Τοις Μετρητοίς (%)", min_value=0.0, max_value=100.0, value=60.0, step=5.0, format="%.2f") / 100
    days_accept = st.number_input("Ημέρες Είσπραξης για Έκπτωση", min_value=0, value=10, step=5)
    days_reject = st.number_input("Ημέρες Είσπραξης Χωρίς Έκπτωση", min_value=0, value=120, step=10)
    cost_of_sales_pct = st.number_input("Κόστος Πωληθέντων (% των πωλήσεων)", min_value=0.0, max_value=100.0, value=80.0, step=1.0, format="%.2f") / 100
    cost_of_capital_annual = st.number_input("Ετήσιο Κόστος Κεφαλαίου (%)", min_value=0.0, max_value=100.0, value=20.0, step=1.0, format="%.2f") / 100
    avg_supplier_pay_days = st.number_input("Μέρες Πληρωμής Προμηθευτών", min_value=0, value=0, step=5)

    if st.button("Υπολογισμός"):
        results = calculate_discount_cash(
            current_sales=current_sales,
            extra_sales=extra_sales,
            cash_discount_rate=cash_discount_rate,
            pct_customers_discount_total=pct_customers_discount_total,
            days_accept=days_accept,
            days_reject=days_reject,
            cost_of_sales_pct=cost_of_sales_pct,
            cost_of_capital_annual=cost_of_capital_annual,
            avg_supplier_pay_days=avg_supplier_pay_days
        )

        st.success("Αποτελέσματα Υπολογισμού:")
        st.write("**Καθαρή Παρούσα Αξία (NPV):**", format_number_gr(results["NPV"]), "€")
        st.write("**Μέγιστη Επιτρεπόμενη Έκπτωση:**", format_percentage_gr(results["Max Discount %"]))
        st.write("**Βέλτιστη Έκπτωση:**", format_percentage_gr(results["Optimal Discount %"]))


def calculate_discount_cash(
    current_sales,                  # Τρέχουσες πωλήσεις (€)
    extra_sales,                    # Επιπλέον πωλήσεις από την έκπτωση (€)
    cash_discount_rate,             # Ποσοστό έκπτωσης (π.χ. 0.02 για 2%)
    pct_customers_discount_total,   # Ποσοστό όλων των πελατών που δέχονται την έκπτωση (π.χ. 0.6)
    days_accept,                    # Ημέρες είσπραξης για πελάτες με έκπτωση (π.χ. 10)
    days_reject,                    # Ημέρες είσπραξης για πελάτες χωρίς έκπτωση (π.χ. 120)
    cost_of_sales_pct,             # Κόστος πωληθέντων ως ποσοστό (π.χ. 0.8)
    cost_of_capital_annual,        # Ετήσιο κόστος κεφαλαίου (π.χ. 0.2)
    avg_supplier_pay_days          # Μέρες αποπληρωμής προμηθευτών (π.χ. 0)
):
    total_sales = current_sales + extra_sales
    gross_profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)

    # Συνάρτηση παρούσας αξίας
    def discount_factor(days):
        return 1 / ((1 + cost_of_capital_annual) ** (days / 365))

    # Παρούσα αξία εισροών από πελάτες που αποδέχονται την έκπτωση
    pv_discount_customers = total_sales * pct_customers_discount_total * (1 - cash_discount_rate) * discount_factor(days_accept)

    # Παρούσα αξία εισροών από πελάτες που δεν αποδέχονται την έκπτωση
    pv_other_customers = total_sales * (1 - pct_customers_discount_total) * discount_factor(days_reject)

    # Παρούσα αξία κόστους των νέων πωλήσεων
    pv_cost_extra_sales = cost_of_sales_pct * extra_sales * discount_factor(avg_supplier_pay_days)

    # Παρούσα αξία των υφιστάμενων πωλήσεων όπως πληρώνονταν πριν (χωρίς αλλαγή πολιτικής)
    old_avg_days = (0.5 * days_accept) + (0.5 * days_reject)
    pv_current_sales = current_sales * discount_factor(old_avg_days)

    # Καθαρή Παρούσα Αξία
    npv = pv_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales

    # Μέγιστη έκπτωση που μπορεί να δοθεί για να είναι NPV ≥ 0
    max_discount = gross_profit_extra_sales / total_sales
    optimal_discount = max_discount * 0.25

    return {
        "NPV": round(npv, 2),
        "Max Discount %": round(max_discount * 100, 2),
        "Optimal Discount %": round(optimal_discount * 100, 2)
    }
