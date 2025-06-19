def calculate_discount_analysis_strict(
    current_sales,
    cogs,
    extra_sales,
    discount_rate,
    share_discount_before,
    days_discount_before,
    share_no_discount_before,
    days_no_discount_before,
    days_discount_after,
    share_discount_after,
    share_no_discount_after,
    bad_debt_rate,
    bad_debt_reduction_rate,
    wacc,
    supplier_payment_days
):
    # 1. Τρέχουσα μέση περίοδος είσπραξης
    avg_days_before = share_discount_before * days_discount_before + share_no_discount_before * days_no_discount_before

    # 2. Τρέχουσες απαιτήσεις
    current_receivables = current_sales * avg_days_before / 365

    # 3. Νέα μέση περίοδος είσπραξης
    avg_days_after = share_discount_after * days_discount_after + share_no_discount_after * days_no_discount_before

    # 4. Νέες απαιτήσεις
    total_sales_after = current_sales + extra_sales
    new_receivables = total_sales_after * avg_days_after / 365

    # 5. Αποδέσμευση κεφαλαίων
    capital_release = current_receivables - new_receivables

    # 6. Κέρδος από επιπλέον πωλήσεις
    margin = (current_sales - cogs) / current_sales
    profit_extra_sales = extra_sales * margin

    # 7. Κέρδος από αποδέσμευση
    profit_from_release = capital_release * wacc

    # 8. Κέρδος από μείωση επισφαλειών
    profit_from_risk_reduction = (
        current_sales * bad_debt_rate -
        total_sales_after * bad_debt_reduction_rate
    )

    # 9. Κόστος έκπτωσης
    discount_cost = total_sales_after * share_discount_after * discount_rate

    # 10. Καθαρό όφελος
    total_profit = profit_extra_sales + profit_from_release + profit_from_risk_reduction - discount_cost

    # 11. Dmax
    try:
        r_daily = wacc / 365
        part1 = (1 + r_daily) ** (days_discount_after - days_no_discount_before)

        part2 = (
            1 - (1 / share_discount_after) +
            (1 - bad_debt_rate) * (1 + r_daily) ** (days_no_discount_before - avg_days_before) +
            (cogs / current_sales) * (extra_sales / current_sales) * (1 + r_daily) ** (days_no_discount_before - supplier_payment_days)
        )

        part3 = share_discount_after * ((total_sales_after) / current_sales) * (1 - bad_debt_rate + bad_debt_reduction_rate)

        dmax = 1 - part1 * (part2 / part3)
    except:
        dmax = 0.0

    # 12. Προτεινόμενη έκπτωση
    try:
        suggested_discount = (1 - ((1 + r_daily) ** (days_discount_after - avg_days_before))) / 2
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
