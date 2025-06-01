from math import pow

def calculate_discount_cash_fixed_pct(
    current_sales,
    extra_sales,
    cash_discount_rate,
    pct_customers_accept,
    days_cash,
    days_reject,
    cost_of_sales_pct,
    cost_of_capital_annual,
    avg_supplier_pay_days,
    current_collection_days
):
    # Σύνολο νέων πωλήσεων
    total_sales = current_sales + extra_sales

    # Προεξοφλητικός συντελεστής
    def discount_factor(days):
        return 1 / pow(1 + cost_of_capital_annual / 365, days)

    # Σταθμισμένο ποσοστό αποδοχής στο ΣΥΝΟΛΟ νέων πωλήσεων
    weighted_pct_discounted_total = (
        (current_sales * pct_customers_accept) + extra_sales
    ) / (current_sales + extra_sales)

    # Παρούσα αξία πωλήσεων σε πελάτες που αποδέχονται την έκπτωση
    pv_discount_customers = (
        total_sales
        * weighted_pct_discounted_total
        * (1 - cash_discount_rate)
        * discount_factor(days_cash)
    )

    # Παρούσα αξία πωλήσεων σε πελάτες που ΔΕΝ αποδέχονται την έκπτωση
    pv_other_customers = (
        total_sales
        * (1 - weighted_pct_discounted_total)
        * discount_factor(days_reject)
    )

    # Παρούσα αξία κόστους επιπλέον πωλήσεων
    pv_cost_extra_sales = (
        cost_of_sales_pct
        * (extra_sales / current_sales)
        * current_sales
        * discount_factor(avg_supplier_pay_days)
    )

    # Παρούσα αξία τρεχουσών πωλήσεων
    pv_current_sales = current_sales * discount_factor(current_collection_days)

    # ✅ Τελικό NPV
    npv = pv_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales

    # ✅ Υπολογισμός μέσης νέας περιόδου είσπραξης
    new_weighted_collection_days = (
        days_cash * pct_customers_accept +
        days_reject * (1 - pct_customers_accept)
    )

    # ✅ Υπολογισμός μέγιστης δυνητικής έκπτωσης (NPV = 0)
    r = cost_of_capital_annual
    D = new_weighted_collection_days
    d = days_cash
    cogs_pct = cost_of_sales_pct
    extra_ratio = extra_sales / current_sales

    # Τύπος Excel από το βιβλίο
    numerator = 1 - 1 / (1 + extra_ratio)
    denominator = pow(1 + r / 365, D - d) * (
        numerator +
        (
            pow(1 + r / 365, d - current_collection_days)
            + cogs_pct * extra_ratio * pow(1 + r / 365, d - avg_supplier_pay_days)
        ) / (1 + extra_ratio)
    )
    max_discount = 1 - denominator

    # ✅ Βέλτιστη έκπτωση
    optimal_discount = (1 - pow(1 + r / 365, d - current_collection_days)) / 2

    return {
        "NPV": round(npv, 2),
        "Max Discount %": round(max_discount * 100, 2),
        "Optimal Discount %": round(optimal_discount * 100, 2),
    }
