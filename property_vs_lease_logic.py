import numpy as np
import numpy_financial as npf

def calculate_property_vs_lease(
    rent_per_month, years, annual_rate, property_price,
    acquisition_costs, annual_maintenance, tax_rate
):
    months = years * 12
    monthly_rate = annual_rate / 12 / 100
    tax_rate_decimal = tax_rate / 100

    # Μίσθωση
    total_rent = rent_per_month * 12 * years
    rent_cashflows = np.full(months, -rent_per_month)
    rent_npv = npf.npv(monthly_rate, rent_cashflows)

    # Δάνειο για αγορά
    loan_amount = property_price
    monthly_payment = npf.pmt(monthly_rate, months, -loan_amount)
    total_loan_payments = monthly_payment * months
    total_interest = total_loan_payments - loan_amount

    # Φορολογικά εκπιπτόμενα
    annual_depreciation = (property_price + acquisition_costs) / years
    annual_tax_shield = (
        (total_interest / years) + annual_depreciation + annual_maintenance
    ) * tax_rate_decimal
    total_tax_savings = annual_tax_shield * years

    # Συνολικό κόστος απόκτησης (με φόρους)
    net_acquisition_cost = total_loan_payments + acquisition_costs - total_tax_savings

    return {
        "total_rent": total_rent,
        "rent_npv": rent_npv,
        "monthly_payment": monthly_payment,
        "total_loan_payments": total_loan_payments,
        "total_interest": total_interest,
        "tax_savings": total_tax_savings,
        "net_acquisition_cost": net_acquisition_cost,
        "cost_difference": net_acquisition_cost - rent_npv
    }
