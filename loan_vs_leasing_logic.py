def pv(rate, nper, pmt, fv=0, when=1):
    """Υπολογισμός παρούσας αξίας ταμειακών ροών"""
    if rate == 0:
        return -pmt * nper - fv
    return -pmt * ((1 - (1 + rate) ** -nper) / rate) - fv / ((1 + rate) ** nper) if when == 0 else \
           -pmt * (((1 - (1 + rate) ** -nper) / rate) * (1 + rate)) - fv / ((1 + rate) ** nper)

def limited_depreciation(asset_value, additional_costs, dep_years, finance_years):
    total_cost = asset_value + additional_costs
    return min(dep_years, finance_years) * (total_cost / dep_years)

def tax_savings(rate, years, interest, depreciation, tax_rate):
    annual_deductible = (interest + depreciation) / years
    return pv(rate, years, -annual_deductible, 0, 0) * tax_rate

def total_cost(pv_installments, pv_working_cap, extra_costs, tax_benefit):
    return pv_installments + pv_working_cap + extra_costs - tax_benefit

def calculate_loan_or_leasing(option, months, rate_main, rate_wc, when_val, dep_years, years, tax_rate, fv=0):
    pv_inst = pv(rate_main, months, option["monthly_installment"], fv, when_val)
    pv_wc = pv(rate_wc, months, option["working_cap_installment"], 0, when_val)
    depreciation = limited_depreciation(option["value_asset"], option["extra_costs"], dep_years, years)
    capital_financed = option["financing_percent"] * option["value_asset"]
    total_paid = option["monthly_installment"] * months
    interest_total = total_paid - capital_financed
    tax = tax_savings(rate_main * 12, years, interest_total, depreciation, tax_rate)
    total = total_cost(pv_inst, pv_wc, option["extra_costs"], tax)

    return {
        "pv_installments": pv_inst,
        "pv_working_cap": pv_wc,
        "depreciation": depreciation,
        "interest_total": interest_total,
        "tax_savings": tax,
        "total_cost": total
    }
