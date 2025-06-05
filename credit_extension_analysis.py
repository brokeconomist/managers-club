from utils import format_number_gr

def calculate_credit_extension_simple(
    current_credit_days: int,
    new_credit_days: int,
    sales_increase_pct: float,
    current_sales: float,
    unit_price: float,
    total_unit_cost: float,
    variable_unit_cost: float,
    bad_debt_pct: float,
    capital_cost_pct: float,
):
    units = current_sales / unit_price
    increased_sales = current_sales * (1 + sales_increase_pct)
    increased_units = units * (1 + sales_increase_pct)

    # Net profit from additional sales
    net_profit = units * sales_increase_pct * (unit_price - variable_unit_cost)

    # Weighted average unit cost after increase
    total_cost_old = units * total_unit_cost
    total_cost_new = (increased_units - units) * variable_unit_cost
    total_combined_cost = total_cost_old + total_cost_new
    weighted_unit_cost = total_combined_cost / increased_units

    # Capital tied up before and after credit extension
    capital_old = current_sales / 360 * current_credit_days * (total_unit_cost / unit_price)
    capital_new = increased_sales / 360 * new_credit_days * (weighted_unit_cost / unit_price)
    additional_capital = capital_new - capital_old

    # Total cost: cost of capital + bad debts
    capital_cost = additional_capital * capital_cost_pct
    bad_debt_cost = increased_sales * bad_debt_pct
    total_cost = capital_cost + bad_debt_cost

    # Final anticipated gain
    anticipated_gain = net_profit - total_cost

    return {
        "Net Profit": net_profit,
        "Total Cost from Increase": total_cost,
        "Anticipated Gain": anticipated_gain,
        "Formatted": {
            "Net Profit": format_number_gr(net_profit),
            "Total Cost from Increase": format_number_gr(total_cost),
            "Anticipated Gain": format_number_gr(anticipated_gain)
        },
        "Suggestion": "✅ Αύξησε την Πίστωση" if anticipated_gain > 0 else "⛔ Μην Αυξήσεις την Πίστωση"
    }
