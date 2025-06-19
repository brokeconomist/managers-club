def calculate_discount_analysis(
    current_sales,
    cogs,
    extra_sales,
    discount_rate,
    share_discount_before,
    days_discount_before,
    days_no_discount_before,
    days_discount_after,
    share_discount_after,
    share_no_discount_after,
    bad_debt_rate,
    bad_debt_reduction_rate,
    wacc,
    supplier_payment_days
):
    avg_days_before = (
        share_discount_before * days_discount_before +
        (1 - share_discount_before) * days_no_discount_before
    )

    current_receivables = current_sales * avg_days_before / 365

    avg_days_after = (
        share_discount_after * days_discount_after +
        share_no_discount_after * days_no_discount_before
    )

    new_receivables = (current_sales + extra_sales) * avg_days_after / 365

    capital_release = current_receivables - new_receivables

    margin = (current_sales - cogs) / current_sales
    profit_extra_sales = extra_sales * margin

    profit_from_release = capital_release * wacc

    profit_from_risk_reduction = (
        current_sales * bad_debt_rate -
        (current_sales + extra_sales) * bad_debt_reduction_rate
    )

    discount_cost = (current_sales + extra_sales) * share_discount_after * discount_rate

    total_profit = (
        profit_extra_sales +
        profit_from_release +
        profit_from_risk_reduction -
        discount_cost
    )

    try:
        r_daily = wacc / 365
        part1 = (1 + r_daily) ** (days_discount_after - days_no_discount_before)

        part2 = (
            1 - (1 / share_discount_after) +
            (1 - bad_debt_rate) * (1 + r_daily) ** (days_no_discount_before - avg_days_before) +
            (cogs / current_sales) *
            (extra_sales / current_sales) *
            (1 + r_daily) ** (days_no_discount_before - supplier_payment_days)
        )

        part3 = (
            share_discount_after *
            ((current_sales + extra_sales) / current_sales) *
            (1 - bad_debt_rate + bad_debt_reduction_rate)
        )

        dmax = 1 - part1 * (part2 / part3)
    except:
        dmax = 0.0

    try:
        suggested_discount = (
            1 - ((1 + r_daily) ** (days_discount_after - avg_days_before))
        ) / 2
    except:
        suggested_discount = 0.0

    return {
        "avg_days_before": avg_days_before,
        "current_receivables": current_receivables,
        "avg_days_after": avg_days_after,
        "new_receivables": new_receivables,
        "capital_release": capital_release,
        "profit_extra_sales": profit_extra_sales,
        "profit_from_release": profit_from_release,
        "profit_from_risk_reduction": profit_from_risk_reduction,
        "discount_cost": discount_cost,
        "total_profit": total_profit,
        "dmax": dmax,
        "suggested_discount": suggested_discount
    }
