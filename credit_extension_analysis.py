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

    # Καθαρό κέρδος από επιπλέον πωλήσεις
    net_profit = units * sales_increase_pct * (unit_price - variable_unit_cost)

    # Σταθμισμένο κόστος ανά μονάδα μετά την αύξηση
    total_cost_old = units * total_unit_cost
    total_cost_new = (increased_units - units) * variable_unit_cost
    total_combined_cost = total_cost_old + total_cost_new
    weighted_unit_cost = total_combined_cost / increased_units

    # Κεφάλαιο που δεσμεύεται πριν και μετά την επέκταση πίστωσης
    capital_old = current_sales / 360 * current_credit_days * (total_unit_cost / unit_price)
    capital_new = increased_sales / 360 * new_credit_days * (weighted_unit_cost / unit_price)
    additional_capital = capital_new - capital_old

    # Συνολικό κόστος (κόστος κεφαλαίου + επισφάλειες)
    capital_cost = additional_capital * capital_cost_pct
    bad_debt_cost = increased_sales * bad_debt_pct
    total_cost = capital_cost + bad_debt_cost

    # Εκτιμώμενο καθαρό όφελος
    anticipated_gain = net_profit - total_cost

    return {
        "Net Profit": round(net_profit, 2),
        "Total Cost from Increase": round(total_cost, 2),
        "Anticipated Gain": round(anticipated_gain, 2),
        "Suggestion": "Αύξησε Πίστωση" if anticipated_gain > 0 else "Μην Αυξήσεις Πίστωση"
    }
