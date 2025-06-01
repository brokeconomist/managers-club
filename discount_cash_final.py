from math import pow

def calculate_discount_cash_fixed_pct(
    current_sales,
    extra_sales,
    cash_discount_rate,
    pct_customers_accept,
    days_cash,
    days_reject,
    cost_of_sales_pct,
    cost_of_capital_annual,
    avg_supplier_pay_days,
    current_collection_days
):
    total_sales = current_sales + extra_sales
    gross_profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)

    def discount_factor(days):
        return 1 / pow(1 + cost_of_capital_annual / 365, days)

    # Μέσο ποσοστό πελατών που ακολουθούν την πολιτική
    weighted_pct_discounted_total = (
        (current_sales * pct_customers_accept) + extra_sales
    ) / (current_sales + extra_sales)

    # Τμήμα 1: Πελάτες που δέχονται έκπτωση
    pv_discount_customers = (
        total_sales
        * weighted_pct_discounted_total
        * (1 - cash_discount_rate)
        * discount_factor(days_cash)
    )

    # Τμήμα 2: Πελάτες που δεν δέχονται
    pv_other_customers = (
        total_sales
        * (1 - weighted_pct_discounted_total)
        * discount_factor(days_reject)
    )

    # Τμήμα 3: Κόστος πωλήσεων των extra πωλήσεων
    pv_cost_extra_sales = (
        cost_of_sales_pct
        * (extra_sales / current_sales)
        * current_sales
        * discount_factor(avg_supplier_pay_days)
    )

    # Τμήμα 4: Υφιστάμενες πωλήσεις (τρέχουσες)
    pv_current_sales = current_sales * discount_factor(current_collection_days)

    # Συνολικό NPV
    npv = pv_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales

    max_discount = gross_profit_extra_sales / total_sales
    optimal_discount = max_discount * 0.25

    return {
        "NPV": round(npv, 2),
        "Max Discount %": round(max_discount * 100, 2),
        "Optimal Discount %": round(optimal_discount * 100, 2),
        "Gross Profit Extra Sales": round(gross_profit_extra_sales, 2),
        "Weighted Acceptance Rate": round(weighted_pct_discounted_total * 100, 2)
    }
