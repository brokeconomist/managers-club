def calculate_discount_cash_npv(
    current_sales,
    extra_sales,
    cost_of_sales_pct,
    pct_customers_discount_total,
    cash_discount_rate,
    cost_of_capital_annual,
    days_accept,
    days_reject,
    avg_supplier_pay_days
):
    total_sales = current_sales + extra_sales
    gross_profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)

    def discount_factor(days):
        return 1 / ((1 + cost_of_capital_annual) ** (days / 365))

    pv_discount_customers = total_sales * pct_customers_discount_total * (1 - cash_discount_rate) * discount_factor(days_accept)
    pv_other_customers = total_sales * (1 - pct_customers_discount_total) * discount_factor(days_reject)
    pv_cost_extra_sales = cost_of_sales_pct * extra_sales * discount_factor(avg_supplier_pay_days)

    old_avg_days = (0.5 * days_accept) + (0.5 * days_reject)
    pv_current_sales = current_sales * discount_factor(old_avg_days)

    npv = pv_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales

    max_discount = gross_profit_extra_sales / total_sales
    optimal_discount = max_discount * 0.25

    return {
        "NPV": round(npv, 2),
        "Max Discount %": round(max_discount * 100, 2),
        "Optimal Discount %": round(optimal_discount * 100, 2)
    }
