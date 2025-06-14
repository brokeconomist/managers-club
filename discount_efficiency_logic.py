def calculate_discount_efficiency(sales, credit_days, discount_days, discount_pct, wacc_pct):
    amount_received = sales * (1 - discount_pct / 100)
    capital_released = sales - amount_received
    days_saved = credit_days - discount_days

    if capital_released > 0 and days_saved > 0:
        annualized_return = (capital_released / amount_received) * (365 / days_saved) * 100
    else:
        annualized_return = 0

    return {
        'amount_received': amount_received,
        'capital_released': capital_released,
        'annualized_return': annualized_return,
        'wacc_pct': wacc_pct
    }
