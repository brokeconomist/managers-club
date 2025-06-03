from utils import format_number_gr

def calculate_discount_cash_efficiency(
    current_sales,
    extra_sales,
    discount_rate,
    pct_accepts_discount,
    pct_accepts_pays_in_days,
    pct_declines_discount,
    pct_declines_pays_in_days,
    cash_days,
    cost_pct,
    wacc,
    supplier_payment_days,
    current_collection_days,
    current_receivables,
    new_collection_days_discount,
    receivables_after_discount,
    release_discount,
    pct_follows_new_policy,
    pct_old_policy,
    new_collection_days_total,
    receivables_after_increase,
    release_total,
    profit_extra_sales,
    profit_release,
    discount_cost
):
    npv = profit_extra_sales + profit_release - discount_cost

    max_discount_pct = (
        (profit_extra_sales + profit_release) / (current_sales + extra_sales)
        if current_sales + extra_sales != 0 else 0
    )

    best_discount_pct = (
        discount_cost / (current_sales + extra_sales)
        if current_sales + extra_sales != 0 else 0
    )

    return {
        "NPV (€)": format_number_gr(npv),
        "Μέγιστη έκπτωση (%)": format_number_gr(max_discount_pct * 100),
        "Βέλτιστη έκπτωση (%)": format_number_gr(best_discount_pct * 100),
    }
