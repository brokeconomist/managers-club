from loan_vs_leasing_logic import calculate_final_burden
from utils import format_number_gr

loan_result, leasing_result = calculate_final_burden(
    loan_rate=0.06,
    wc_rate=0.08,
    duration_years=15,
    property_value=250000,
    loan_financing_percent=0.7,
    leasing_financing_percent=1.0,
    add_expenses_loan=35000,
    add_expenses_leasing=30000,
    residual_value_leasing=3530,
    depreciation_years=30,
    tax_rate=0.35,
    pay_when=1
)

col1.metric("📉 Τελική Επιβάρυνση Δανείου", f"{format_number_gr(loan_result)} €")
col2.metric("📉 Τελική Επιβάρυνση Leasing", f"{format_number_gr(leasing_result)} €")
