def calculate_required_sales_increase_excel_style(
    price_A,
    profit_A,
    profit_B,
    profit_C,
    profit_D,
    percent_B,
    percent_C,
    percent_D,
    percent_D_extra,
    price_reduction  # π.χ. -0.10 για -10%
):
    # Αθροιστικά κέρδη συμπληρωματικών προϊόντων
    supplementary_profit = (
        (percent_B * profit_B) +
        (percent_C * profit_C) +
        (percent_D * profit_D) +
        (price_A * percent_D_extra)  # Υποθέτοντας πως D6*D12 αντιστοιχεί σε αυτό
    )

    denominator = ((profit_A + supplementary_profit) / price_A) + price_reduction

    if denominator == 0:
        return None

    required_increase = -price_reduction / denominator

    return required_increase * 100  # ποσοστό %

# Παράδειγμα χρήσης (τα ποσοστά σε δεκαδική μορφή, όχι %):
price_A = 200.0
profit_A = 60.0
profit_B = 18.0
profit_C = 11.0
profit_D = 14.0
percent_B = 0.9     # 90%
percent_C = 0.7     # 70%
percent_D = 0.1     # 10%
percent_D_extra = 0.05  # πχ 5% επιπλέον (αντί για D12)
price_reduction = -0.1  # -10% μείωση τιμής

result = calculate_required_sales_increase_excel_style(
    price_A,
    profit_A,
    profit_B,
    profit_C,
    profit_D,
    percent_B,
    percent_C,
    percent_D,
    percent_D_extra,
    price_reduction
)

print(f"Απαιτούμενη αύξηση πωλήσεων: {result:.2f}%")
