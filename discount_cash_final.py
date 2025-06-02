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

    def discount_factor(days):
        return 1 / pow(1 + cost_of_capital_annual / 365, days)

    weighted_pct_discounted_total = (
        (current_sales * pct_customers_accept) + extra_sales
    ) / total_sales

    pv_discount_customers = (
        total_sales
        * weighted_pct_discounted_total
        * (1 - cash_discount_rate)
        * discount_factor(days_cash)
    )

    pv_other_customers = (
        total_sales
        * (1 - weighted_pct_discounted_total)
        * discount_factor(days_reject)
    )

    pv_cost_extra_sales = (
        cost_of_sales_pct
        * (extra_sales / current_sales)
        * current_sales
        * discount_factor(avg_supplier_pay_days)
    )

    pv_current_sales = current_sales * discount_factor(current_collection_days)

    npv = pv_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales

    # Μεταβλητές για τύπους Excel (σύμφωνα με τα C3, C4, C9, κλπ)
    P3 = current_sales
    P4 = extra_sales
    P5 = cash_discount_rate
    P9 = days_reject
    P10 = days_cash
    P11 = cost_of_sales_pct
    P12 = cost_of_capital_annual
    P13 = avg_supplier_pay_days
    P15 = current_collection_days
    P20 = pct_customers_accept

    r = P12 / 365
    ratio_extra_sales = P4 / P3

    term1 = 1 - (1 / P20)
    term2 = pow(1 + r, P9 - P15)
    term3 = P11 * ratio_extra_sales * pow(1 + r, P9 - P13)
    denom = P20 * (1 + ratio_extra_sales)

    max_discount = 1 - pow(1 + r, P10 - P9) * (term1 + (term2 + term3) / denom)

    optimal_discount = 1 - pow(1 + r, P10 - P9) * (term1 + (term2 + term3) / denom)

    return {
        "NPV": round(npv, 2),
        "Max Discount %": round(max_discount * 100, 2),
        "Optimal Discount %": round(optimal_discount * 100, 2)
    }
