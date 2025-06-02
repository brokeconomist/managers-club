import numpy as np
from scipy.optimize import brentq

# Υπολογισμός καθαρής παρούσας αξίας (NPV) από την έκπτωση
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
    # Νέες πωλήσεις με έκπτωση
    discount_sales = discount_acceptance_ratio * additional_sales
    # Νέες πωλήσεις χωρίς έκπτωση
    full_price_sales = (1 - discount_acceptance_ratio) * additional_sales

    # Υπολογισμός ημερών αποδέσμευσης κεφαλαίου
    new_collection_days = (discount_acceptance_ratio * days_discount_payment +
                           (1 - discount_acceptance_ratio) * days_full_payment)

    capital_released = (
        (current_collection_period * current_sales + new_collection_days * additional_sales)
        / (current_sales + additional_sales)
        - supplier_payment_days
    )

    # Αποδέσμευση κεφαλαίου σε €
    capital_freed_value = capital_released * (current_sales + additional_sales) * cost_ratio / 360

    # Κέρδος από τις νέες πωλήσεις
    profit_new_sales = additional_sales * (1 - cost_ratio)

    # Κόστος της έκπτωσης
    discount_cost = discount_sales * discount_rate

    # NPV = Κέρδος - Έκπτωση + Αποδέσμευση κεφαλαίου αποπληρωμένη στην αρχή
    npv = profit_new_sales - discount_cost + capital_freed_value / (1 + annual_cost_of_capital)

    return npv

# Συνάρτηση για εύρεση μέγιστης έκπτωσης (NPV = 0)
def find_break_even_discount(params):
    def objective(discount_rate):
        return npv_discount_cash(discount_rate=discount_rate, **params)

    try:
        return brentq(objective, 0.0001, 0.5)
    except ValueError:
        return None

# Εισαγωγή δεδομένων
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

# Υπολογισμός NPV με έκπτωση 2.14%
optimal_discount = 0.0214
npv_optimal = npv_discount_cash(discount_rate=optimal_discount, **params)

# Εύρεση μέγιστης έκπτωσης για NPV=0
break_even_discount = find_break_even_discount(params)

# Εμφάνιση αποτελεσμάτων
print(f"NPV για έκπτωση 2.14%: {npv_optimal:.2f} €")
print(f"Μέγιστη έκπτωση για NPV=0 (Break-Even): {break_even_discount:.2%}")
print(f"Βέλτιστη έκπτωση (δοσμένη): {optimal_discount:.2%}")
