def calculate_discount_cash_fixed_pct(
    current_sales,
    extra_sales,
    cash_discount_rate,
    pct_customers_accept,
    days_accept,
    days_reject,
    cost_of_sales_pct,
    cost_of_capital_annual,
    avg_supplier_pay_days,
    current_collection_days
):
    total_sales = current_sales + extra_sales
    cost_of_capital_daily = cost_of_capital_annual / 365

    # Σταθμισμένο ποσοστό πελατών που αποδέχεται την έκπτωση επί του νέου συνόλου
    weighted_accept_rate_total = (
        (current_sales * pct_customers_accept) + extra_sales
    ) / total_sales

    # Παρούσα αξία από πελάτες που αποδέχονται την έκπτωση και πληρώνουν τοις μετρητοίς
    pv_accept = (
        total_sales
        * weighted_accept_rate_total
        * (1 - cash_discount_rate)
        * (1 / ((1 + cost_of_capital_daily) ** days_accept))
    )

    # Παρούσα αξία από πελάτες που δεν αποδέχονται την έκπτωση
    pv_reject = (
        total_sales
        * (1 - weighted_accept_rate_total)
        * (1 / ((1 + cost_of_capital_daily) ** days_reject))
    )

    # Κόστος πωλήσεων σε παρούσα αξία λόγω επιπλέον πωλήσεων
    pv_cost_extra_sales = (
        cost_of_sales_pct
        * (extra_sales / current_sales)
        * current_sales
        * (1 / ((1 + cost_of_capital_daily) ** avg_supplier_pay_days))
    )

    # Παρούσα αξία από τρέχουσες πωλήσεις χωρίς καμία αλλαγή
    pv_current_sales = current_sales * (
        1 / ((1 + cost_of_capital_daily) ** current_collection_days)
    )

    # Υπολογισμός NPV
    npv = pv_accept + pv_reject - pv_cost_extra_sales - pv_current_sales

    return round(npv, 2)
