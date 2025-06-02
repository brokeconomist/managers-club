def calculate_discount_cash_fixed_pct(
    current_sales,
    additional_sales,
    discount_percentage,
    acceptance_rate,
    days_discount,
    days_no_discount,
    cost_percentage,
    wacc,
    supplier_days,
    current_collection_days
):
    # Μετατροπή ποσοστών σε δεκαδικούς
    discount_pct = discount_percentage / 100
    acceptance_pct = acceptance_rate / 100
    cost_pct = cost_percentage / 100
    wacc_daily = wacc / 100 / 365

    # Μεσοσταθμική παλιά περίοδος είσπραξης
    old_dso_weighted = acceptance_pct * days_discount + (1 - acceptance_pct) * days_no_discount

    # Cash flows
    total_sales = current_sales + additional_sales
    cost_of_goods = total_sales * cost_pct

    # Εισπράξεις από πελάτες με έκπτωση
    inflow_discount = (
        total_sales * acceptance_pct * (1 - discount_pct)
        / (1 + wacc_daily) ** days_discount
    )

    # Εισπράξεις από πελάτες χωρίς έκπτωση
    inflow_no_discount = (
        total_sales * (1 - acceptance_pct)
        / (1 + wacc_daily) ** days_no_discount
    )

    # Εξερχόμενες πληρωμές σε προμηθευτές
    outflow_suppliers = cost_of_goods / (1 + wacc_daily) ** supplier_days

    # NPV
    npv = inflow_discount + inflow_no_discount - outflow_suppliers

    # Μέγιστη δυνητική έκπτωση (NPV Break Even)
    try:
        d_max = 1 - (
            (1 + wacc_daily) ** (days_discount - days_no_discount)
            * (
                (1 - (1 / acceptance_pct))
                + (
                    (1 + wacc_daily) ** (days_no_discount - supplier_days)
                    + cost_pct * (1 + wacc_daily) ** (days_no_discount - supplier_days)
                )
                / (acceptance_pct * (1 + cost_pct))
            )
        )
        d_max_pct = d_max * 100
    except Exception:
        d_max_pct = 0.0

    # Βέλτιστη έκπτωση
    try:
        d_opt = (1 - (1 + wacc_daily) ** (days_discount - supplier_days)) / 2
        d_opt_pct = d_opt * 100
    except Exception:
        d_opt_pct = 0.0

    return {
        "NPV": round(npv, 2),
        "max_discount_pct": round(d_max_pct, 2),
        "optimal_discount_pct": round(d_opt_pct, 2)
    }