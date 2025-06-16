import numpy as np

def npv(rate, cashflows):
    """
    Υπολογίζει την Καθαρή Παρούσα Αξία (NPV).
    rate: επιτόκιο ανά περίοδο (π.χ. μηνιαίο, σε δεκαδική μορφή)
    cashflows: λίστα ή numpy array με χρηματικές ροές (αρνητικές/θετικές)
    """
    periods = np.arange(len(cashflows))
    discounted = cashflows / ((1 + rate) ** periods)
    return discounted.sum()

def pmt(rate, nper, pv, fv=0, when='end'):
    """
    Υπολογίζει τη σταθερή πληρωμή δανείου (PMT).
    rate: επιτόκιο ανά περίοδο (π.χ. μηνιαίο, σε δεκαδική μορφή)
    nper: αριθμός περιόδων
    pv: παρούσα αξία (ποσό δανείου, θετικό)
    fv: μελλοντική αξία (συνήθως 0)
    when: 'end' για πληρωμή στο τέλος περιόδου, 'begin' για αρχή
    """
    if rate == 0:
        return -(pv + fv) / nper
    else:
        when_val = 1 if when == 'begin' else 0
        payment = -(rate * (pv * (1 + rate)**nper + fv)) / ((1 + rate * when_val) * ((1 + rate)**nper - 1))
        return payment

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
    rent_npv = npv(monthly_rate, rent_cashflows)

    # Δάνειο για αγορά
    loan_amount = property_price
    monthly_payment = pmt(monthly_rate, months, -loan_amount)
    total_loan_payments = monthly_payment * months
    total_interest = total_loan_payments - loan_amount

    # Φορολογικά εκπιπτόμενα
    annual_depreciation = (property_price + acquisition_costs) / years
    annual_tax_shield = (
        total_interest / years + annual_depreciation + annual_maintenance
    ) * tax_rate_decimal
    total_tax_savings = annual_tax_shield * years

    # Συνολικό κόστος απόκτησης
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
