from utils import format_number_gr, parse_gr_number

def pv(rate, nper, pmt, fv=0, when=1):
    """Υπολογισμός παρούσας αξίας ταμειακών ροών"""
    if rate == 0:
        return pmt * nper + fv
    return pmt * (((1 - (1 + rate) ** -nper) / rate) * (1 + rate) if when else (1 - (1 + rate) ** -nper) / rate) + fv / ((1 + rate) ** nper)

def limited_depreciation(asset_value, additional_costs, dep_years, finance_years):
    total_cost = asset_value + additional_costs
    return min(dep_years, finance_years) * (total_cost / dep_years)

def tax_savings(rate, years, interest, depreciation, tax_rate):
    annual_deductible = (interest + depreciation) / years
    return pv(rate, years, annual_deductible, 0, 0) * tax_rate

def total_cost(pv_installments, pv_working_cap, extra_costs, tax_benefit):
    return pv_installments + pv_working_cap + extra_costs - tax_benefit
