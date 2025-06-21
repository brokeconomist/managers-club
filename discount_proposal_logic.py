from decimal import Decimal, getcontext

# Υψηλή ακρίβεια για χρηματοοικονομικούς υπολογισμούς
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
    # === Υφιστάμενα ===
    current_avg_collection_days = (
        pct_sales_with_discount * days_collection_discounted +
        pct_sales_without_discount * days_collection_undiscounted
    )
    current_receivables = current_sales * current_avg_collection_days / 365
    new_avg_collection_days = (
        pct_sales_with_discount_after_increase * days_cash_payment_deadline +
        pct_sales_without_discount_after_increase * days_collection_undiscounted
    )
    new_receivables = (current_sales + additional_sales_discount) * new_avg_collection_days / 365
    released_capital = current_receivables - new_receivables
    profit_from_additional_sales = additional_sales_discount * ((current_sales - cost_of_sales) / current_sales)
    profit_from_released_capital = released_capital * cost_of_capital
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

    # === Μέγιστη & Βέλτιστη Έκπτωση με Decimal ===
    i = Decimal(str(cost_of_capital)) / Decimal('365')
    M = Decimal(str(days_cash_payment_deadline))
    N = Decimal(str(current_avg_collection_days))
    D = Decimal(str(avg_supplier_payment_days))
    C = D
    p = Decimal(str(pct_sales_with_discount_after_increase))
    b = Decimal(str(pct_current_bad_debts))
    k = Decimal(str(pct_bad_debt_reduction_after_discount))
    V = Decimal(str(cost_of_sales)) / Decimal(str(current_sales))
    g = Decimal(str(additional_sales_discount)) / Decimal(str(current_sales))

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

    # === Υπολογισμός NPV ===
    total_sales = current_sales + additional_sales_discount
    daily_discount_rate = Decimal(str(cost_of_capital)) / Decimal('365')

    npv = (
        Decimal(str(total_sales)) * Decimal(str(p)) * (Decimal('1') - Decimal(str(cash_discount_rate))) *
        (Decimal('1') / (Decimal('1') + daily_discount_rate) ** Decimal(str(days_cash_payment_deadline)))
        +
        Decimal(str(total_sales)) * (Decimal('1') - Decimal(str(p))) *
        (Decimal('1') / (Decimal('1') + daily_discount_rate) ** Decimal(str(days_collection_undiscounted)))
        -
        Decimal(str(cost_of_sales)) * Decimal(str(additional_sales_discount / current_sales)) *
        (Decimal('1') / (Decimal('1') + daily_discount_rate) ** Decimal(str(avg_supplier_payment_days)))
        -
        Decimal(str(current_sales)) * (Decimal('1') / (Decimal('1') + daily_discount_rate) ** Decimal(str(current_avg_collection_days)))
    )

    # === Επιστροφή αποτελεσμάτων ===
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
        "npv": round(npv, 0),
    }
