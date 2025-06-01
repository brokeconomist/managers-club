import streamlit as st

# discount_cash_final.py

def calculate_discount_cash_fixed_pct(
    current_sales,
    extra_sales,
    cash_discount_rate,
    pct_customers_accept,
    days_accept,
    days_reject,
    cost_of_sales_pct,
    cost_of_capital_annual,
    avg_supplier_pay_days
):
    total_sales = current_sales + extra_sales
    gross_profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)

    def discount_factor(days):
        return 1 / ((1 + cost_of_capital_annual / 365) ** days)

    # Μέσο σταθμικό ποσοστό αποδοχής έκπτωσης επί του νέου συνόλου πωλήσεων
    weighted_pct_discounted_total = (
        (current_sales * pct_customers_accept) + extra_sales
    ) / (current_sales + extra_sales)

    # Παρούσα αξία εσόδων από πελάτες που αποδέχονται την έκπτωση
    pv_discount_customers = (
        total_sales * weighted_pct_discounted_total
        * (1 - cash_discount_rate)
        * discount_factor(days_accept)
    )

    # Παρούσα αξία εσόδων από πελάτες που **δεν** αποδέχονται την έκπτωση
    pv_other_customers = (
        total_sales * (1 - weighted_pct_discounted_total)
        * discount_factor(days_reject)
    )

    # Κόστος επιπλέον πωλήσεων (discounted)
    pv_cost_extra_sales = (
        cost_of_sales_pct * (extra_sales / current_sales) * current_sales
        * discount_factor(avg_supplier_pay_days)
    )

    # Παρούσα αξία των υφιστάμενων πωλήσεων
    pv_current_sales = current_sales * discount_factor(days_reject)

    # Τελική NPV
    npv = pv_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales

    # Υπολογισμός μέγιστης & "βέλτιστης" έκπτωσης (αν θέλεις να δείχνεις προτεινόμενο ποσοστό)
    max_discount = gross_profit_extra_sales / total_sales if total_sales else 0
    optimal_discount = max_discount * 0.25

    return {
        "NPV": round(npv, 2),
        "Max Discount %": round(max_discount * 100, 2),
        "Optimal Discount %": round(optimal_discount * 100, 2),
        "Gross Profit Extra Sales": round(gross_profit_extra_sales, 2),
        "Weighted Acceptance Rate": round(weighted_pct_discounted_total * 100, 2)
    }
