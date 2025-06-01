def calculate_discount_cash_fixed_pct(
    current_sales,
    extra_sales,
    cash_discount_rate,
    pct_customers_accept,
    days_accept,
    days_reject,
    cost_of_sales_pct,
    cost_of_capital_annual,
    avg_supplier_pay_days,
    current_collection_days
):
    total_sales = current_sales + extra_sales
    capital_daily_rate = cost_of_capital_annual / 365

    # Βάρος αποδοχής έκπτωσης στο νέο σύνολο
    weighted_acceptance = (current_sales * pct_customers_accept + extra_sales) / total_sales

    # (1) Πελάτες που αποδέχονται την έκπτωση
    pv_discount_customers = (
        total_sales
        * weighted_acceptance
        * (1 - cash_discount_rate)
        * (1 / ((1 + capital_daily_rate) ** days_accept))
    )

    # (2) Πελάτες που δεν την αποδέχονται
    pv_other_customers = (
        total_sales
        * (1 - weighted_acceptance)
        * (1 / ((1 + capital_daily_rate) ** days_reject))
    )

    # (3) Κόστος επιπλέον πωλήσεων
    pv_cost_extra_sales = (
        cost_of_sales_pct
        * (extra_sales / current_sales)
        * current_sales
        * (1 / ((1 + capital_daily_rate) ** avg_supplier_pay_days))
    )

    # (4) Παρούσα αξία τρεχουσών πωλήσεων με τις παλιές μέρες είσπραξης
    pv_current_sales = (
        current_sales
        * (1 / ((1 + capital_daily_rate) ** current_collection_days))
    )

    # Τελική καθαρή παρούσα αξία
    npv = pv_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales

    return round(npv, 2)
