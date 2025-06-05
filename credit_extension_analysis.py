def calculate_credit_extension_impact(
    old_credit_days,
    new_credit_days,
    sales_increase_pct,
    current_sales,
    unit_price,
    total_cost_per_unit,
    variable_cost_per_unit,
    bad_debt_rate,
    cost_of_capital
):
    # Υπολογισμός επιπλέον πωλήσεων και μονάδων
    new_sales = current_sales * (1 + sales_increase_pct / 100)
    extra_sales = new_sales - current_sales
    extra_units = extra_sales / unit_price

    # Υπολογισμός καθαρού οφέλους από νέες πωλήσεις
    benefit = extra_units * (unit_price - variable_cost_per_unit)

    # Υπολογισμός παρούσας & νέας δέσμευσης κεφαλαίων
    old_commitment = (current_sales / 365) * old_credit_days * (total_cost_per_unit / unit_price)
    new_total_cost_per_unit = (total_cost_per_unit * current_sales + variable_cost_per_unit * extra_sales) / new_sales
    new_commitment = (new_sales / 365) * new_credit_days * (new_total_cost_per_unit / unit_price)

    extra_commitment = new_commitment - old_commitment

    # Υπολογισμός κόστους επιπλέον δέσμευσης
    cost_extra_commitment = extra_commitment * (cost_of_capital / 100)

    # Κόστος επισφαλειών
    bad_debt_cost = extra_sales * (bad_debt_rate / 100)

    # Συνολικό κόστος & καθαρό εκτιμώμενο κέρδος
    total_cost = cost_extra_commitment + bad_debt_cost
    net_profit = benefit - total_cost

    return {
        "Νέες Πωλήσεις": new_sales,
        "Νέο Συνολικό Κόστος ανά Μονάδα": new_total_cost_per_unit,
        "Παρούσα Δέσμευση Κεφαλαίων (€)": old_commitment,
        "Νέα Δέσμευση Κεφαλαίων (€)": new_commitment,
        "Επιπλέον Δέσμευση Κεφαλαίων (€)": extra_commitment,
        "Συνολικό Όφελος (€)": benefit,
        "Κόστος Επιπλέον Δέσμευσης Κεφαλαίων (€)": cost_extra_commitment,
        "Κόστος Επισφαλειών (€)": bad_debt_cost,
        "Συνολικό Κόστος Αύξησης Πίστωσης (€)": total_cost,
        "Συνολικό Εκτιμώμενο Κέρδος (€)": net_profit
    }
