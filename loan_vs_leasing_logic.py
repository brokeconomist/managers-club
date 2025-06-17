from math import isclose
from utils import format_number_gr, parse_gr_number


def pv(rate, nper, pmt, fv=0, when=1):
    """Υπολογισμός παρούσας αξίας ταμειακών ροών ως κόστους (θετικό αποτέλεσμα)"""
    if isclose(rate, 0):
        return abs(pmt * nper + fv)
    pv_val = pmt * ((1 - (1 + rate) ** -nper) / rate)
    if when == 1:
        pv_val *= (1 + rate)
    return abs(pv_val + fv / ((1 + rate) ** nper))


def limited_depreciation(asset_value, additional_costs, dep_years, finance_years):
    total_cost = asset_value + additional_costs
    return min(dep_years, finance_years) * (total_cost / dep_years)


def tax_savings(rate, years, interest, depreciation, tax_rate):
    annual_deductible = (interest + depreciation) / years
    return pv(rate, years, annual_deductible, 0, 0) * tax_rate


def total_cost(pv_installments, pv_working_cap, extra_costs, tax_benefit):
    return pv_installments + pv_working_cap + extra_costs - tax_benefit


def calculate_loan_vs_leasing(data):
    # Κοινές παράμετροι
    years = int(data['years'])
    months = int(data['months'])
    nper = years * months
    when = int(data['when'])
    tax_rate = float(data['tax_rate']) / 100
    dep_years = int(data['dep_years'])

    results = {}
    for option in ['loan', 'leasing']:
        asset_value = parse_gr_number(data[f'{option}_asset_value'])
        funding_percent = float(data[f'{option}_funding']) / 100
        monthly_payment = parse_gr_number(data[f'{option}_monthly_payment'])
        additional_costs = parse_gr_number(data[f'{option}_extra_costs'])
        residual_value = parse_gr_number(data.get(f'{option}_residual_value', '0'))
        working_cap_loan = parse_gr_number(data[f'{option}_working_cap_loan'])
        working_cap_payment = parse_gr_number(data[f'{option}_working_cap_monthly'])

        rate = float(data[f'{option}_rate']) / 100
        working_cap_rate = float(data['working_cap_rate']) / 100

        # Παρούσα αξία δόσεων
        pv_installments = pv(rate / months, nper, monthly_payment, -residual_value if residual_value else 0, when)

        # Παρούσα αξία δανείου κεφαλαίου κίνησης
        pv_working_cap = pv(working_cap_rate / months, nper, working_cap_payment, 0, when)

        # Αποσβέσεις
        depreciation = limited_depreciation(asset_value, additional_costs, dep_years, years)

        # Τόκοι = Σύνολο τόκων σε βάθος 15ετίας (υπολογίζεται χονδρικά: δόση*μήνες - ποσό χρηματοδότησης)
        total_funding = asset_value * funding_percent + working_cap_loan
        total_payments = (monthly_payment + working_cap_payment) * nper
        interest = total_payments - total_funding

        # Φορολογικό όφελος
        tax_benefit = tax_savings(rate / months, nper, interest, depreciation, tax_rate)

        # Τελικό κόστος
        final_cost = total_cost(pv_installments, pv_working_cap, additional_costs, tax_benefit)

        results[option] = {
            'pv_installments': pv_installments,
            'pv_working_cap': pv_working_cap,
            'extra_costs': additional_costs,
            'tax_benefit': tax_benefit,
            'final_cost': final_cost
        }

    return results
