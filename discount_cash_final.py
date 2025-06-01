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

    # 1. Παρούσα αξία πωλήσεων από πελάτες που δέχονται την έκπτωση
    pv_discount_customers = (
        total_sales
        * pct_customers_accept
        * (1 - cash_discount_rate)
        * (1 / ((1 + cost_of_capital_daily) ** days_accept))
    )

    # 2. Παρούσα αξία πωλήσεων από πελάτες που δεν δέχονται την έκπτωση
    pv_other_customers = (
        total_sales
        * (1 - pct_customers_accept)
        * (1 / ((1 + cost_of_capital_daily) ** days_reject))
    )

    # 3. Παρούσα αξία κόστους πωλήσεων για τις επιπλέον πωλήσεις
    cost_extra_sales_ratio = extra_sales / current_sales
    pv_cost_extra_sales = (
        cost_of_sales_pct
        * cost_extra_sales_ratio
        * current_sales
        * (1 / ((1 + cost_of_capital_daily) ** avg_supplier_pay_days))
    )

    # 4. Παρούσα αξία των τρεχουσών πωλήσεων (status quo)
    pv_current_sales = current_sales * (1 / ((1 + cost_of_capital_daily) ** current_collection_days))

    # 5. Υπολογισμός NPV
    npv = pv_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales

    # Επιπλέον μεταβλητές για πληροφόρηση
    gross_profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)
    max_discount = gross_profit_extra_sales / total_sales
    optimal_discount = max_discount * 0.25
    weighted_pct_discounted_total = (
        (current_sales * pct_customers_accept) + extra_sales
    ) / (current_sales + extra_sales)

    return {
        "NPV": round(npv, 2),
        "Max Discount %": round(max_discount * 100, 2),
        "Optimal Discount %": round(optimal_discount * 100, 2),
        "Gross Profit Extra Sales": round(gross_profit_extra_sales, 2),
        "Weighted Acceptance Rate": round(weighted_pct_discounted_total * 100, 2)
    }
