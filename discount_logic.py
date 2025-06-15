import numpy as np

def calculate_discount_analysis(
    sales,
    extra_sales,
    discount_rate,
    acceptance_rate,
    acceptance_days,
    rejection_rate,
    rejection_days,
    cash_payment_days,
    cost_rate,
    wacc,
    current_collection_days,
    supplier_payment_days,
):
    r = wacc / 365
    g = extra_sales / sales
    p = acceptance_rate
    y = cost_rate
    M = cash_payment_days
    Q = rejection_days
    N = current_collection_days
    C = supplier_payment_days

    # Κόστος της έκπτωσης
    discount_cost = (sales + extra_sales) * p * discount_rate

    # Κέρδος από επιπλέον πωλήσεις
    profit_extra_sales = extra_sales * (1 - y)

    # Αποδέσμευση κεφαλαίων (NPV of freed working capital)
    current_receivables = sales * current_collection_days / 365
    new_collection_days = p * M + (1 - p) * Q
    new_receivables = (sales + extra_sales) * new_collection_days / 365
    freed_capital = (current_receivables - new_receivables) * wacc

    # Συνολικό όφελος
    total_net_gain = profit_extra_sales + freed_capital - discount_cost

    # NPV προσέγγιση (τύπος Bhattacharya για μέγιστη έκπτωση)
    try:
        d_max = 1 - (1 + r) ** (M - Q) * (
            (1 - 1 / p)
            + (1 + r) ** (Q - N)
            + y * g * (1 + r) ** (Q - C) / (p * (1 + g))
        )
    except ZeroDivisionError:
        d_max = None

    return {
        "profit_extra_sales": profit_extra_sales,
        "freed_capital": freed_capital,
        "discount_cost": discount_cost,
        "total_net_gain": total_net_gain,
        "d_max": d_max,
    }


def optimize_discount(
    sales,
    extra_sales,
    acceptance_rate,
    acceptance_days,
    rejection_days,
    cash_payment_days,
    cost_rate,
    wacc,
    current_collection_days,
    supplier_payment_days,
):
    results = []
    for d in np.arange(0.001, 0.20, 0.0005):
        metrics = calculate_discount_analysis(
            sales,
            extra_sales,
            d,
            acceptance_rate,
            60,
            1 - acceptance_rate,
            rejection_days,
            cash_payment_days,
            cost_rate,
            wacc,
            current_collection_days,
            supplier_payment_days,
        )
        results.append((d, metrics["total_net_gain"]))

    best = max(results, key=lambda x: x[1])
    return best
