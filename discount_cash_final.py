import numpy as np
from scipy.optimize import brentq

def npv_discount_cash(
    discount_rate,
    current_sales,
    additional_sales,
    days_full_payment,
    days_discount_payment,
    cost_ratio,
    annual_cost_of_capital,
    supplier_payment_days,
    current_collection_period,
    discount_acceptance_ratio,
):
    discount_sales = discount_acceptance_ratio * additional_sales
    full_price_sales = (1 - discount_acceptance_ratio) * additional_sales

    new_collection_days = (
        discount_acceptance_ratio * days_discount_payment +
        (1 - discount_acceptance_ratio) * days_full_payment
    )

    capital_released_days = (
        (current_collection_period * current_sales + new_collection_days * additional_sales)
        / (current_sales + additional_sales)
        - supplier_payment_days
    )

    capital_freed_value = capital_released_days * (current_sales + additional_sales) * cost_ratio / 360

    profit_new_sales = additional_sales * (1 - cost_ratio)
    discount_cost = discount_sales * discount_rate

    npv = profit_new_sales - discount_cost + capital_freed_value / (1 + annual_cost_of_capital)

    return npv

def find_break_even_discount(params):
    def objective(discount_rate):
        return npv_discount_cash(discount_rate=discount_rate, **params)

    try:
        return brentq(objective, 0.0001, 0.5)
    except ValueError:
        return None

# Δεδομένα εισόδου (τα ίδια με αυτά που έβαλες στην εικόνα)
params = dict(
    current_sales=1000.00,
    additional_sales=250.00,
    days_full_payment=120,
    days_discount_payment=10,
    cost_ratio=0.8,
    annual_cost_of_capital=0.20,
    supplier_payment_days=30,
    current_collection_period=90,
    discount_acceptance_ratio=0.5
)

# Υπολογισμός για έκπτωση 2.14%
optimal_discount = 0.0214
npv_optimal = npv_discount_cash(discount_rate=optimal_discount, **params)

# Υπολογισμός break-even έκπτωσης (NPV = 0)
break_even_discount = find_break_even_discount(params)

# Εκτύπωση αποτελεσμάτων με έλεγχο
print(f"NPV για έκπτωση 2.14%: {npv_optimal:.2f} €")

if break_even_discount is not None:
    print(f"Μέγιστη έκπτωση που μηδενίζει το NPV (Break-Even): {break_even_discount:.2%}")
else:
    print("Δεν βρέθηκε έκπτωση που μηδενίζει το NPV.")

print(f"Βέλτιστη έκπτωση που πρέπει να δοθεί: {optimal_discount:.2%}")
