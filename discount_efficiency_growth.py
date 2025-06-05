def calculate_discount_efficiency_growth(
    current_sales,
    extra_sales,
    discount_rate,
    discount_acceptance,
    discount_days,
    non_acceptance,
    non_discount_days,
    cash_days,
    cost_percent,
    wacc,
    suppliers_days,
    current_collection_days
):
    # Συντελεστής προεξόφλησης ανά ημέρα
    daily_discount_factor = 1 + (wacc / 100) / 365

    # Ποσοστά πελατών βάσει νέας πολιτικής
    total_sales = current_sales + extra_sales
    share_new_policy = current_sales / total_sales
    share_old_policy = 1 - share_new_policy

    # Νέα μέση περίοδος είσπραξης για τους πελάτες που αποδέχονται και δεν αποδέχονται την έκπτωση
    discounted_collection_days = (
        (discount_acceptance * discount_days + non_acceptance * non_discount_days) / 100
    )

    # Προεξοφλημένες ταμειακές ροές:
    present_value_discounted = (
        total_sales * share_new_policy * (1 - discount_rate / 100)
        / (daily_discount_factor ** cash_days)
    )

    present_value_non_discounted = (
        total_sales * share_old_policy
        / (daily_discount_factor ** non_discount_days)
    )

    present_value_supplier_shift = (
        cost_percent / 100
        * (extra_sales / current_sales)
        * current_sales
        / (daily_discount_factor ** suppliers_days)
    )

    present_value_current_receivables = (
        current_sales
        / (daily_discount_factor ** current_collection_days)
    )

    # NPV καθαρής απόδοσης της πολιτικής έκπτωσης
    npv = (
        present_value_discounted
        + present_value_non_discounted
        - present_value_supplier_shift
        - present_value_current_receivables
    )

    # Μέγιστη αποδεκτή έκπτωση (NPV Break Even)
    try:
        max_discount_numerator = (
            1
            - (1 / (share_new_policy))
            + (daily_discount_factor ** (non_discount_days - current_collection_days))
            + ((cost_percent / 100) * (extra_sales / current_sales) *
               (daily_discount_factor ** (non_discount_days - suppliers_days)))
        )

        max_discount_denominator = (
            share_new_policy * (1 + (extra_sales / current_sales))
        )

        max_discount = 1 - (
            (daily_discount_factor ** (cash_days - non_discount_days)) *
            (max_discount_numerator / max_discount_denominator)
        )
    except ZeroDivisionError:
        max_discount = None  # ή 0

    # Βέλτιστη έκπτωση ως μέσος όρος
    optimal_discount = (
        1 - (daily_discount_factor ** (cash_days - current_collection_days))
    ) / 2

    return {
        "npv": npv,
        "max_discount": max_discount,
        "optimal_discount": optimal_discount,
        "daily_discount_factor": daily_discount_factor
    }
