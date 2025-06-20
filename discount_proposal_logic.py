def calculate_discount_analysis(
    current_sales,
    cost_of_sales,
    additional_sales_discount,
    cash_discount_rate,
    pct_sales_with_discount,
    days_collection_discounted,
    pct_sales_without_discount,
    days_collection_undiscounted,
    days_cash_payment_deadline,
    pct_sales_with_discount_after_increase,
    pct_sales_without_discount_after_increase,
    pct_current_bad_debts,
    pct_bad_debt_reduction_after_discount,
    cost_of_capital,
    avg_supplier_payment_days,
):
    # Τρέχουσα μέση περίοδος είσπραξης απαιτήσεων
    current_avg_collection_days = (
        days_collection_discounted * pct_sales_with_discount +
        days_collection_undiscounted * pct_sales_without_discount
    )

    # Τρέχουσες απαιτήσεις
    current_receivables = current_sales * current_avg_collection_days / 365

    # Νέα μέση περίοδος είσπραξης μετά την αύξηση πωλήσεων
    new_avg_collection_days = (
        pct_sales_with_discount_after_increase * days_cash_payment_deadline +
        pct_sales_without_discount_after_increase * days_collection_undiscounted
    )

    # Απαιτήσεις μετά την αύξηση πωλήσεων
    new_receivables = (
        (current_sales + additional_sales_discount) * new_avg_collection_days / 365
    )

    # Αποδέσμευση κεφαλαίων
    released_capital = current_receivables - new_receivables

    # Κέρδος από επιπλέον πωλήσεις
    profit_from_additional_sales = additional_sales_discount * ((current_sales - cost_of_sales) / current_sales)

    # Κέρδος από αποδέσμευση
    profit_from_released_capital = released_capital * cost_of_capital

    # Κέρδος μείωσης επισφαλειών
    profit_from_bad_debt_reduction = (
        (current_sales * pct_current_bad_debts) -
        ((current_sales + additional_sales_discount) * pct_bad_debt_reduction_after_discount)
    )

    # Κόστος έκπτωσης
    discount_cost = (
        (current_sales + additional_sales_discount) *
        pct_sales_with_discount_after_increase *
        cash_discount_rate
    )

    # Εκτιμώμενο συνολικό κέρδος
    total_estimated_profit = (
        profit_from_additional_sales +
        profit_from_released_capital +
        profit_from_bad_debt_reduction -
        discount_cost
    )

    # === Μέγιστη Έκπτωση με τον Ακριβή Τύπο από το Βιβλίο ===
    r = cost_of_capital / 365
    M = days_cash_payment_deadline
    Q = days_collection_undiscounted
    P = pct_sales_with_discount_after_increase
    Y = pct_current_bad_debts
    N = current_avg_collection_days
    C = avg_supplier_payment_days
    G = additional_sales_discount / current_sales
    Z = pct_bad_debt_reduction_after_discount

    term1 = 1 - (1 / P)
    term2 = (1 - Y) * ((1 + r) ** (Q - N))
    term3 = (cost_of_sales / current_sales) * G * ((1 + r) ** (Q - C))
    denominator = P * (1 + G) * (1 - Y + Z)
    bracket = term1 + term2 + (term3 / denominator)
    max_discount = 1 - ((1 + r) ** (M - Q)) * bracket

    # Βέλτιστη Έκπτωση
    estimated_best_discount = (
        1 - ((1 + r) ** (M - N))
    ) / 2

    return {
        "current_avg_collection_days": round(current_avg_collection_days, 0),
        "current_receivables": round(current_receivables, 0),
        "new_avg_collection_days": round(new_avg_collection_days, 0),
        "new_receivables": round(new_receivables, 0),
        "released_capital": round(released_capital, 0),
        "profit_from_additional_sales": round(profit_from_additional_sales, 0),
        "profit_from_released_capital": round(profit_from_released_capital, 0),
        "profit_from_bad_debt_reduction": round(profit_from_bad_debt_reduction, 0),
        "discount_cost": round(discount_cost, 0),
        "total_estimated_profit": round(total_estimated_profit, 0),
        "max_discount_pct": round(max_discount * 100, 2),
        "estimated_best_discount_pct": round(estimated_best_discount * 100, 2),
    }
