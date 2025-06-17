from utils import parse_gr_number

def pv(rate, nper, pmt, fv=0, when=1):
    """Υπολογισμός παρούσας αξίας (πάντα θετική τιμή)"""
    if rate == 0:
        return abs(pmt * nper + fv)
    pv_val = pmt * (((1 - (1 + rate) ** -nper) / rate) * (1 + rate) if when else (1 - (1 + rate) ** -nper) / rate)
    pv_val += fv / ((1 + rate) ** nper)
    return abs(pv_val)

def total_depreciation(asset_value, extra_costs, dep_years, total_years):
    """Συνολικές αποσβέσεις: περιορισμένες στην μικρότερη διάρκεια"""
    total_cost = asset_value + extra_costs
    dep_years_effective = min(dep_years, total_years)
    return dep_years_effective * (total_cost / dep_years)

def tax_savings(interest_costs, depreciation, tax_rate):
    """Φορολογικό όφελος από εκπιπτόμενες δαπάνες"""
    deductible_total = interest_costs + depreciation
    return deductible_total * tax_rate

def final_burden(total_payment, tax_savings):
    """Τελική επιβάρυνση = πληρωμές - φορολογικό όφελος"""
    return total_payment - tax_savings
