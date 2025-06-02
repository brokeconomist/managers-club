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
    current_collection_days,
    discount_acceptance_ratio,
):
    # Νέες πωλήσεις με έκπτωση
    discount_sales = discount_acceptance_ratio * additional_sales
    # Νέες πωλήσεις χωρίς έκπτωση
    full_price_sales = (1 - discount_acceptance_ratio) * additional_sales

    # Νέες μέρες είσπραξης
    new_collection_days = current_collection_days

    # Υπολογισμός ημερών αποδέσμευσης κεφαλαίου
    capital_released = (
        (current_collection_days * current_sales + new_collection_days * additional_sales)
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

# ✅ Συνάρτηση που καλείται από την εφαρμογή
def calculate_discount_cash_fixed_pct(
    discount_rate,
    current_sales,
    additional_sales,
    days_full_payment,
    days_discount_payment,
    cost_ratio,
    annual_cost_of_capital,
    supplier_payment_days,
    current_collection_days,
    discount_acceptance_ratio
):
    npv = npv_discount_cash(
        discount_rate=discount_rate,
        current_sales=current_sales,
        additional_sales=additional_sales,
        days_full_payment=days_full_payment,
        days_discount_payment=days_discount_payment,
        cost_ratio=cost_ratio,
        annual_cost_of_capital=annual_cost_of_capital,
        supplier_payment_days=supplier_payment_days,
        current_collection_days=current_collection_days,
        discount_acceptance_ratio=discount_acceptance_ratio
    )

    # Εύρεση μέγιστης έκπτωσης για NPV=0
    params = dict(
        current_sales=current_sales,
        additional_sales=additional_sales,
        days_full_payment=days_full_payment,
        days_discount_payment=days_discount_payment,
        cost_ratio=cost_ratio,
        annual_cost_of_capital=annual_cost_of_capital,
        supplier_payment_days=supplier_payment_days,
        current_collection_days=current_collection_days,
        discount_acceptance_ratio=discount_acceptance_ratio
    )

    break_even_discount = find_break_even_discount(params)

    return {
        "npv": npv,
        "break_even_discount": break_even_discount
    }
