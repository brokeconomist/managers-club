def manosv_cash_credit_control(
    current_cash_pct,
    current_credit_pct,
    current_credit_days,
    new_cash_pct,
    new_credit_pct,
    new_credit_days,
    sales_increase_pct,
    current_sales,
    unit_price,
    total_unit_cost,
    variable_unit_cost,
    expected_bad_debts_pct,
    interest_rate_pct
):
    # Βασικοί υπολογισμοί
    units = current_sales / unit_price
    increased_units = units * (1 + sales_increase_pct)
    increased_sales = current_sales * (1 + sales_increase_pct)

    # Καθαρό Κέρδος από αύξηση πωλήσεων
    net_profit = (units * sales_increase_pct) * (unit_price - variable_unit_cost)

    # Σταθμισμένο μοναδιαίο κόστος μετά την αύξηση
    total_cost_old = units * total_unit_cost
    total_cost_new = (increased_units - units) * variable_unit_cost
    weighted_unit_cost = (total_cost_old + total_cost_new) / increased_units

    # Παρούσα δέσμευση κεφαλαίου (πίστωση)
    credit_sales_current = current_sales * current_credit_pct
    capital_current = (credit_sales_current / 360) * current_credit_days * (total_unit_cost / unit_price)

    # Προτεινόμενη δέσμευση κεφαλαίου (πίστωση επί νέων πωλήσεων)
    credit_sales_new = increased_sales * new_credit_pct
    capital_new = (credit_sales_new / 360) * new_credit_days * (weighted_unit_cost / unit_price)

    # Επιπλέον δέσμευση κεφαλαίου
    additional_capital = capital_new - capital_current

    # Κόστος δέσμευσης + Επισφάλειες
    capital_cost = additional_capital * interest_rate_pct
    bad_debts_cost = (current_sales * expected_bad_debts_pct) + (current_sales * sales_increase_pct * expected_bad_debts_pct)
    total_cost = capital_cost + bad_debts_cost

    # Καθαρό αποτέλεσμα
    anticipated_gain = net_profit - total_cost

    return {
        "Net Profit": round(net_profit, 2),
        "Capital Cost": round(capital_cost, 2),
        "Bad Debts Cost": round(bad_debts_cost, 2),
        "Total Cost": round(total_cost, 2),
        "Anticipated Gain": round(anticipated_gain, 2),
        "Suggestion": "Increase Credit" if anticipated_gain > 0 else "Do Not Increase Credit"
    }
