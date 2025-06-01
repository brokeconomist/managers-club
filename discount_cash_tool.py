def cash_discount_analysis(
    current_sales, extra_sales, discount_rate,
    accept_rate, days_accept, days_non_accept,
    current_collection_days, gross_margin, wacc
):
    """
    Υπολογίζει την επίδραση έκπτωσης τοις μετρητοίς σε δύο στάδια:
    1. Μόνο με την έκπτωση χωρίς επιπλέον πωλήσεις
    2. Με την έκπτωση και την αύξηση πωλήσεων
    Επιστρέφει λεξικό με όλα τα ενδιάμεσα και τελικά μεγέθη.
    """

    days_per_year = 365

    # --- Στάδιο 1: Μόνο έκπτωση, χωρίς επιπλέον πωλήσεις ---

    # Νέες πωλήσεις = τρέχουσες (χωρίς αύξηση)
    new_sales_stage1 = current_sales

    # Ποσοστό πελατών με νέα πολιτική (αποδέκτες έκπτωσης)
    pct_new_policy_stage1 = accept_rate

    # Ποσοστό πελατών παλαιά πολιτική
    pct_old_policy_stage1 = 1 - pct_new_policy_stage1

    # Νέα μέση μέρα είσπραξης
    new_avg_days_stage1 = pct_new_policy_stage1 * days_accept + pct_old_policy_stage1 * days_non_accept

    # Τρέχουσες απαιτήσεις (σε €)
    old_receivables = (current_sales * current_collection_days) / days_per_year

    # Νέες απαιτήσεις μετά την έκπτωση (χωρίς αύξηση πωλήσεων)
    new_receivables_stage1 = (new_sales_stage1 * new_avg_days_stage1) / days_per_year

    # Αποδέσμευση κεφαλαίων (θετικό αν μειώνονται οι απαιτήσεις)
    capital_released_stage1 = old_receivables - new_receivables_stage1

    # Κέρδος από αποδέσμευση κεφαλαίων
    profit_release_stage1 = capital_released_stage1 * wacc

    # Κόστος έκπτωσης (επί τω υπάρχοντος όγκου πωλήσεων)
    discount_cost_stage1 = new_sales_stage1 * pct_new_policy_stage1 * discount_rate

    # Κέρδος από επιπλέον πωλήσεις = 0 (δεν υπάρχουν ακόμα)
    profit_extra_stage1 = 0

    # Συνολικό κέρδος στάδιο 1
    total_profit_stage1 = profit_extra_stage1 + profit_release_stage1 - discount_cost_stage1

    # NPV στάδιο 1
    npv_stage1 = total_profit_stage1 / (1 + wacc)


    # --- Στάδιο 2: Προσθέτουμε την αύξηση πωλήσεων λόγω έκπτωσης ---

    new_sales_stage2 = current_sales + extra_sales

    # Ποσοστό πελατών με νέα πολιτική επί του νέου συνόλου
    pct_new_policy_stage2 = (current_sales * accept_rate + extra_sales) / new_sales_stage2

    pct_old_policy_stage2 = 1 - pct_new_policy_stage2

    new_avg_days_stage2 = pct_new_policy_stage2 * days_accept + pct_old_policy_stage2 * days_non_accept

    new_receivables_stage2 = (new_sales_stage2 * new_avg_days_stage2) / days_per_year

    capital_released_stage2 = old_receivables - new_receivables_stage2

    profit_release_stage2 = capital_released_stage2 * wacc

    profit_extra_stage2 = extra_sales * gross_margin

    discount_cost_stage2 = new_sales_stage2 * pct_new_policy_stage2 * discount_rate

    total_profit_stage2 = profit_extra_stage2 + profit_release_stage2 - discount_cost_stage2

    npv_stage2 = total_profit_stage2 / (1 + wacc)


    return {
        # Στάδιο 1 (μόνο έκπτωση)
        "stage1": {
            "new_sales": new_sales_stage1,
            "pct_new_policy": pct_new_policy_stage1,
            "pct_old_policy": pct_old_policy_stage1,
            "new_avg_days": new_avg_days_stage1,
            "old_receivables": old_receivables,
            "new_receivables": new_receivables_stage1,
            "capital_released": capital_released_stage1,
            "profit_release": profit_release_stage1,
            "discount_cost": discount_cost_stage1,
            "profit_extra": profit_extra_stage1,
            "total_profit": total_profit_stage1,
            "npv": npv_stage1,
        },

        # Στάδιο 2 (με αύξηση πωλήσεων)
        "stage2": {
            "new_sales": new_sales_stage2,
            "pct_new_policy": pct_new_policy_stage2,
            "pct_old_policy": pct_old_policy_stage2,
            "new_avg_days": new_avg_days_stage2,
            "old_receivables": old_receivables,
            "new_receivables": new_receivables_stage2,
            "capital_released": capital_released_stage2,
            "profit_release": profit_release_stage2,
            "discount_cost": discount_cost_stage2,
            "profit_extra": profit_extra_stage2,
            "total_profit": total_profit_stage2,
            "npv": npv_stage2,
        }
    }
