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
    ) / (current_sales + extra_sales)

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

    # Μέγιστη Έκπτωση - ΝΕΟΣ τύπος από Excel
    r = cost_of_capital_annual
    P3 = current_sales
    P4 = extra_sales
    P5 = cash_discount_rate
    P9 = days_reject
    P10 = days_cash
    P11 = cost_of_sales_pct
    P12 = r
    P13 = avg_supplier_pay_days
    P15 = current_collection_days
    P20 = pct_customers_accept

    denom_inner = (
        (1 - (1 / P20))
        + (
            pow(1 + P12 / 365, P9 - P15)
            + P11 * (P4 / P3) * pow(1 + P12 / 365, P9 - P13)
        ) / (P20 * (1 + (P4 / P3)))
    )

    max_discount = 1 - pow(1 + P12 / 365, P10 - P9) * denom_inner
    optimal_discount = (1 - pow(1 + P12 / 365, P10 - P15)) / 2

    return {
        "NPV": round(npv, 2),
        "Max Discount %": round(max_discount * 100, 2),
        "Optimal Discount %": round(optimal_discount * 100, 2)
    }
