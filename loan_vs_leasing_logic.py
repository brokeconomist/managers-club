from utils import parse_gr_number, format_number_gr
from math import pow

def pv(rate, nper, pmt, fv=0, when=1):
    if rate == 0:
        return -pmt * nper - fv
    return (
        -pmt * ((1 - pow(1 + rate, -nper)) / rate) - fv / pow(1 + rate, nper)
        if when == 0 else
        -pmt * (((1 - pow(1 + rate, -nper)) / rate) * (1 + rate)) - fv / pow(1 + rate, nper)
    )

def limited_depreciation(asset_value, residual_value, extra_costs, dep_years, finance_years):
    total_cost = asset_value + extra_costs
    annual_dep = (total_cost - residual_value) / dep_years
    return min(dep_years, finance_years) * annual_dep

def tax_savings(rate, years, interest, depreciation, tax_rate):
    annual_deductible = (interest + depreciation) / years
    tax_benefit = pv(rate, years, -annual_deductible, 0, 0) * tax_rate
    return abs(tax_benefit)

def total_cost(pv_installments, pv_working_capital, extra_costs, tax_benefit):
    return abs(pv_installments + pv_working_capital + extra_costs - tax_benefit)
