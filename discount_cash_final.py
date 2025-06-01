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
    total_sales = current_sales + extra_sales
    gross_profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)

    def discount_factor(days):
        return 1 / pow(1 + cost_of_capital_annual / 365, days)

    # Σταθμισμένο ποσοστό αποδοχής πολιτικής
    weighted_pct_discounted_total = (
        (current_sales * pct_customers_accept) + extra_sales
    ) / total_sales

    # Παρούσα αξία πελατών που αποδέχονται την έκπτωση
    pv_discount_customers = (
        total_sales
        * weighted_pct_discounted_total
        * (1 - cash_discount_rate)
        * discount_factor(days_cash)
    )

    # Παρούσα αξία πελατών που δεν αποδέχονται την έκπτωση
    pv_other_customers = (
        total_sales
        * (1 - weighted_pct_discounted_total)
        * discount_factor(days_reject)
    )

    # Κόστος πωλήσεων των extra πωλήσεων
    pv_cost_extra_sales = (
        cost_of_sales_pct
        * (extra_sales / current_sales)
        * current_sales
        * discount_factor(avg_supplier_pay_days)
    )

    # Παρούσα αξία τρεχουσών εισπράξεων
    pv_current_sales = current_sales * discount_factor(current_collection_days)

    # Συνολικό NPV
    npv = pv_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales

    # 👉 Μέγιστη Δυνητική Έκπτωση (βάσει οικονομικού τύπου που οδηγεί σε ~8.34%)
    r = cost_of_capital_annual
    D = current_collection_days
    d = days_cash
    cogs_pct = cost_of_sales_pct
    extra_ratio = extra_sales / current_sales

    numerator = 1 - 1 / (1 + extra_ratio)
    denominator = (1 / (1 + r / 365)) ** (D - d) * (
        numerator + ((1 + r / 365) ** (d - avg_supplier_pay_days) + cogs_pct * extra_ratio * (1 + r / 365) ** (d - days_reject)) / (1 + extra_ratio)
    )

    max_discount = 1 - denominator
    optimal_discount = max_discount * 0.25

    return {
        "NPV": round(npv, 2),
        "Max Discount %": round(max_discount * 100, 2),
        "Optimal Discount %": round(optimal_discount * 100, 2),
        "Gross Profit Extra Sales": round(gross_profit_extra_sales, 2),
        "Weighted Acceptance Rate": round(weighted_pct_discounted_total * 100, 2)
    }
