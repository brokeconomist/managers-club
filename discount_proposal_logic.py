from decimal import Decimal, getcontext

# Ορίζουμε υψηλή ακρίβεια
getcontext().prec = 20

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
    # === Υπολογισμός της τρέχουσας μέσης περιόδου είσπραξης με ακρίβεια ===
    pct_sales_with_discount_dec = Decimal(str(pct_sales_with_discount))
    pct_sales_without_discount_dec = Decimal(str(pct_sales_without_discount))
    days_collection_discounted_dec = Decimal(str(days_collection_discounted))
    days_collection_undiscounted_dec = Decimal(str(days_collection_undiscounted))

    current_avg_collection_days = (
        pct_sales_with_discount_dec * days_collection_discounted_dec +
        pct_sales_without_discount_dec * days_collection_undiscounted_dec
    )

    current_sales_dec = Decimal(str(current_sales))
    cost_of_sales_dec = Decimal(str(cost_of_sales))
    additional_sales_discount_dec = Decimal(str(additional_sales_discount))

    # Τρέχουσες απαιτήσεις με ακρίβεια
    current_receivables = current_sales_dec * current_avg_collection_days / Decimal('365')

    # Νέα μέση περίοδος είσπραξης
    new_avg_collection_days = (
        Decimal(str(pct_sales_with_discount_after_increase)) * Decimal(str(days_cash_payment_deadline)) +
        Decimal(str(pct_sales_without_discount_after_increase)) * Decimal(str(days_collection_undiscounted))
    )

    new_receivables = (current_sales_dec + additional_sales_discount_dec) * new_avg_collection_days / Decimal('365')
    released_capital = current_receivables - new_receivables

    profit_from_additional_sales = additional_sales_discount * ((current_sales - cost_of_sales) / current_sales)
    profit_from_released_capital = float(released_capital) * cost_of_capital
    profit_from_bad_debt_reduction = (
        (current_sales * pct_current_bad_debts) -
        ((current_sales + additional_sales_discount) * pct_bad_debt_reduction_after_discount)
    )

    discount_cost = (
        (current_sales + additional_sales_discount) *
        pct_sales_with_discount_after_increase *
        cash_discount_rate
    )

    total_estimated_profit = (
        profit_from_additional_sales +
        profit_from_released_capital +
        profit_from_bad_debt_reduction -
        discount_cost
    )

    # === Μέγιστη Έκπτωση με Decimal ===
    i = Decimal(str(cost_of_capital)) / Decimal('365')
    M = Decimal(str(days_cash_payment_deadline))
    N = current_avg_collection_days
    D = Decimal(str(avg_supplier_payment_days))
    C = D
    p = Decimal(str(pct_sales_with_discount_after_increase))
    b = Decimal(str(pct_current_bad_debts))
    k = Decimal(str(pct_bad_debt_reduction_after_discount))
    V = cost_of_sales_dec / current_sales_dec
    g = additional_sales_discount_dec / current_sales_dec

    time_diff1 = M - N
    time_diff2 = N - D
    time_diff3 = N - C

    base = Decimal('1') + i
    numerator = (
        Decimal('1') - (Decimal('1') / p)
        + ((Decimal('1') - b) * base ** time_diff2 + V * g * base ** time_diff3)
        / (p * (Decimal('1') + g) * (Decimal('1') - b + k))
    )

    max_discount = Decimal('1') - (base ** time_diff1) * numerator
    estimated_best_discount = (Decimal('1') - (base ** (M - N))) / Decimal('2')

    # === Υπολογισμός NPV με Decimal ===
    total_sales = current_sales_dec + additional_sales_discount_dec
    pct_new_policy = p
    pct_old_policy = Decimal('1') - p

    npv = (
        total_sales * pct_new_policy * (Decimal('1') - Decimal(str(cash_discount_rate))) / (base ** M) +
        total_sales * pct_old_policy / (base ** Decimal(str(days_collection_undiscounted))) -
        V * additional_sales_discount_dec / (base ** D) -
        current_sales_dec / (base ** N)
    )

    return {
        "current_avg_collection_days": float(current_avg_collection_days),
        "current_receivables": float(current_receivables),
        "new_avg_collection_days": float(new_avg_collection_days),
        "new_receivables": float(new_receivables),
        "released_capital": float(released_capital),
        "profit_from_additional_sales": round(profit_from_additional_sales, 0),
        "profit_from_released_capital": round(profit_from_released_capital, 0),
        "profit_from_bad_debt_reduction": round(profit_from_bad_debt_reduction, 0),
        "discount_cost": round(discount_cost, 0),
        "total_estimated_profit": round(total_estimated_profit, 0),
        "max_discount_pct": round(float(max_discount) * 100, 2),
        "estimated_best_discount_pct": round(float(estimated_best_discount) * 100, 2),
        "npv": round(float(npv), 2),
    }
