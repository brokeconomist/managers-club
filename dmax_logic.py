def calculate_dmax_excel_compatible(
    current_sales,
    extra_sales,
    prc_clients_take_disc,
    days_clients_take_discount,
    days_clients_not_take_discount,
    new_days_payment_clients_take_discount,
    COGS,
    WACC,
    avg_days_pay_suppliers,
    avg_current_collection_days
):
    WACC_daily = WACC / 365
    Δsales_over_sales = extra_sales / current_sales
    p = prc_clients_take_disc

    try:
        power1 = (1 + WACC_daily) ** (new_days_payment_clients_take_discount - days_clients_not_take_discount)
        power2 = (1 + WACC_daily) ** (days_clients_not_take_discount - avg_current_collection_days)
        power3 = (1 + WACC_daily) ** (days_clients_not_take_discount - avg_days_pay_suppliers)

        numerator = (
            1 - (1 / p) +
            power2 +
            COGS * Δsales_over_sales * power3
        )

        denominator = p * (1 + Δsales_over_sales)

        dmax = 1 - (power1 * (numerator / denominator))
        return dmax
    except Exception:
        return 0.0
