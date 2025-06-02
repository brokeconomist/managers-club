from math import pow
from scipy.optimize import minimize_scalar

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
    r = cost_of_capital_annual / 365

    def discount_factor(days):
        return 1 / pow(1 + r, days)

    weighted_pct_discounted_total = (
        (current_sales * pct_customers_accept) + extra_sales
    ) / (current_sales + extra_sales)

    pv_discount_customers = (
        total_sales
        * weighted_pct_discounted_total
        * (1 - cash_discount_rate)
        * discount_factor(days_cash)
    )

    pv_other_customers = (
        total_sales
        * (1 - weighted_pct_discounted_total)
        * discount_factor(days_reject)
    )

    pv_cost_extra_sales = (
        cost_of_sales_pct
        * (extra_sales / current_sales)
        * current_sales
        * discount_factor(avg_supplier_pay_days)
    )

    pv_current_sales = current_sales * discount_factor(current_collection_days)

    npv = pv_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales

    # Υπολογισμός Break-even έκπτωσης (όπου NPV=0)
    def npv_for_discount(discount_pct):
        pv_discount_cust = (
            total_sales
            * weighted_pct_discounted_total
            * (1 - discount_pct)
            * discount_factor(days_cash)
        )
        return (
            pv_discount_cust
            + pv_other_customers
            - pv_cost_extra_sales
            - pv_current_sales
        )

    res = minimize_scalar(
        lambda x: abs(npv_for_discount(x)),
        bounds=(0, 0.5),  # 0% έως 50% έκπτωση λογικά
        method='bounded'
    )
    break_even_discount = res.x if res.success else 0

    # Βέλτιστη έκπτωση (συντηρητική προσέγγιση)
    optimal_discount = break_even_discount / 4  # πχ 1/4 της μέγιστης

    return {
        "NPV": round(npv, 2),
        "Break-even Discount %": round(break_even_discount * 100, 2),
        "Optimal Discount %": round(optimal_discount * 100, 2)
    }
