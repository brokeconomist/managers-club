from utils import parse_gr_number
from math import isclose

def pv(rate, nper, pmt, fv=0, when=1):
    """Υπολογισμός παρούσας αξίας ταμειακών ροών ως κόστους (πάντα θετικός αριθμός)"""
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

def calculate_scenario(params):
    loan_rate = params["loan_rate"]
    wc_rate = params["wc_rate"]
    years = params["years"]
    months = params["months"]
    when = params["when"]
    asset_value = params["asset_value"]
    funding_rate = params["funding_rate"]
    monthly_payment = params["monthly_payment"]
    extra_costs = params["extra_costs"]
    working_capital = params["working_capital"]
    working_cap_payment = params["working_cap_payment"]
    residual_value = params.get("residual_value", 0)
    depreciation_years = params["depreciation_years"]
    tax_rate = params["tax_rate"]

    nper = years * months
    pv_installments = pv(loan_rate / months, nper, monthly_payment, -residual_value, when)
    pv_working_cap = pv(wc_rate / months, nper, working_cap_payment, 0, when)
    interest_total = monthly_payment * nper - (asset_value * funding_rate)
    depreciation = limited_depreciation(asset_value, extra_costs, depreciation_years, years)
    tax_benefit = tax_savings(loan_rate, years, interest_total, depreciation, tax_rate)
    total = pv_installments + pv_working_cap + extra_costs - tax_benefit

    return {
        "pv_installments": pv_installments,
        "pv_working_cap": pv_working_cap,
        "depreciation": depreciation,
        "interest_total": interest_total,
        "tax_savings": tax_benefit,
        "total_cost": total
    }
