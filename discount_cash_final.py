def calculate_discount_cash_fixed_pct(
    current_sales,
    additional_sales,
    discount_pct,
    acceptance_rate,
    discount_days,
    no_discount_days,
    cost_pct,
    capital_cost_rate,
    supplier_payment_days,
    current_collection_days_old
):
    # 1. Υπολογισμός νέας μέσης περιόδου είσπραξης μετά την πολιτική
    new_collection_days = (
        acceptance_rate / 100 * discount_days +
        (1 - acceptance_rate / 100) * no_discount_days
    )

    # 2. Υπολογισμός παλιάς μέσης περιόδου είσπραξης (μεσοσταθμικά)
    current_collection_days = current_collection_days_old

    # 3. Καθαρές ταμειακές ροές με βάση το Excel
    total_sales = current_sales + additional_sales
    acceptance_ratio = acceptance_rate / 100
    cost_ratio = cost_pct / 100
    capital_daily = capital_cost_rate / 100 / 365

    npv = (
        total_sales * acceptance_ratio * (1 - discount_pct / 100) * (1 / (1 + capital_daily) ** discount_days) +
        total_sales * (1 - acceptance_ratio) * (1 / (1 + capital_daily) ** no_discount_days) -
        cost_ratio * (additional_sales / current_sales) * current_sales * (1 / (1 + capital_daily) ** supplier_payment_days) -
        current_sales * (1 / (1 + capital_daily) ** current_collection_days)
    )

    # 4. Μέγιστη έκπτωση (break-even)
    try:
        max_discount = 1 - (1 + capital_daily) ** (current_collection_days - discount_days) * (
            (1 - (1 / acceptance_ratio)) +
            (
                (1 + capital_daily) ** (discount_days - no_discount_days) +
                cost_ratio * (additional_sales / current_sales) * (1 + capital_daily) ** (discount_days - supplier_payment_days)
            ) / (acceptance_ratio * (1 + additional_sales / current_sales))
        )
    except ZeroDivisionError:
        max_discount = 0

    # 5. Βέλτιστη έκπτωση
    optimal_discount = (1 - ((1 + capital_daily) ** (current_collection_days - discount_days))) / 2

    return {
        "npv": round(npv, 2),
        "max_discount": round(max_discount * 100, 2),
        "optimal_discount": round(optimal_discount * 100, 2),
        "new_collection_days": round(new_collection_days, 2),
        "old_collection_days": round(current_collection_days, 2),
    }
