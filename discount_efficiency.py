def calculate_discount_efficiency(
    current_sales, extra_sales, discount_rate, pct_accepting, days_accepting,
    pct_rejecting, days_rejecting, cash_days, cost_pct, wacc, supplier_days,
    current_collection_days=None
):
    """
    Υπολογίζει την αποδοτικότητα πολιτικής έκπτωσης τοις μετρητοίς με ανάπτυξη πωλήσεων.
    
    Παράμετροι:
    - current_sales (float): Τρέχουσες πωλήσεις (€)
    - extra_sales (float): Επιπλέον πωλήσεις λόγω έκπτωσης (€)
    - discount_rate (float): Ποσοστό έκπτωσης (%)
    - pct_accepting (float): % πελατών που αποδέχονται την έκπτωση (%)
    - days_accepting (int): Μέρες πληρωμής πελατών που αποδέχονται την έκπτωση
    - pct_rejecting (float): % πελατών που δεν αποδέχονται την έκπτωση (%)
    - days_rejecting (int): Μέρες πληρωμής πελατών που δεν αποδέχονται
    - cash_days (int): Μέρες πληρωμής τοις μετρητοίς
    - cost_pct (float): Κόστος πωλήσεων (% επί πωλήσεων)
    - wacc (float): Κόστος κεφαλαίου (WACC %)
    - supplier_days (int): Μέση περίοδος αποπληρωμής προμηθευτών (μέρες)
    - current_collection_days (int ή None): Τρέχουσα μέση περίοδος είσπραξης (μέρες), αν None υπολογίζεται
    
    Επιστρέφει:
    dict με υπολογισμένα αποτελέσματα, όπως NPV, αποδέσμευση κεφαλαίων, break-even έκπτωση κλπ.
    """

    # Μετατροπή ποσοστών σε δεκαδικά
    pct_accepting /= 100
    pct_rejecting /= 100
    discount_rate /= 100
    cost_pct /= 100
    wacc /= 100

    # Υπολογισμός μέσης περιόδου είσπραξης αν δεν δοθεί
    if current_collection_days is None:
        current_avg_collection = days_accepting * pct_accepting + days_rejecting * pct_rejecting
    else:
        current_avg_collection = current_collection_days
    current_receivables = current_sales * current_avg_collection / 365

    # Νέα πολιτική χωρίς αύξηση πωλήσεων (οι αποδέκτες πληρώνουν τοις μετρητοίς)
    new_avg_collection = cash_days * pct_accepting + days_rejecting * pct_rejecting
    new_receivables = current_sales * new_avg_collection / 365
    release1 = current_receivables - new_receivables

    # Νέα πολιτική με αύξηση πωλήσεων
    total_sales = current_sales + extra_sales
    pct_new_policy = ((current_sales * pct_accepting) + extra_sales) / total_sales if total_sales != 0 else 0
    pct_old_policy = 1 - pct_new_policy

    avg_collection_after_growth = pct_new_policy * cash_days + pct_old_policy * days_rejecting
    receivables_after_growth = total_sales * avg_collection_after_growth / 365
    release2 = current_receivables - receivables_after_growth

    # Κέρδη από επιπλέον πωλήσεις και αποδέσμευση κεφαλαίων
    profit_extra_sales = extra_sales * (1 - cost_pct)
    release_profit = release2 * wacc
    discount_cost = total_sales * pct_new_policy * discount_rate
    total_profit = profit_extra_sales + release_profit - discount_cost

    # Παράγοντες προεξόφλησης (για NPV)
    factor_accepting = 1 / ((1 + (wacc / 365)) ** cash_days)
    factor_rejecting = 1 / ((1 + (wacc / 365)) ** days_rejecting)
    factor_suppliers = 1 / ((1 + (wacc / 365)) ** supplier_days)
    factor_old = 1 / ((1 + (wacc / 365)) ** current_avg_collection)

    # Καθαρή παρούσα αξία (NPV)
    npv = (
        total_sales * pct_new_policy * (1 - discount_rate) * factor_accepting +
        total_sales * (1 - pct_new_policy) * factor_rejecting -
        cost_pct * extra_sales * factor_suppliers -
        current_sales * factor_old
    )

    # Break-even έκπτωση (προσοχή σε διαίρεση με μηδέν)
    try:
        break_even_discount = 1 - (
            (1 + (wacc / 365)) ** (cash_days - days_rejecting) *
            (
                (1 - (1 / pct_new_policy)) +
                ((1 + (wacc / 365)) ** (days_rejecting - current_avg_collection) +
                 cost_pct * (extra_sales / current_sales) * ((1 + (wacc / 365)) ** (days_rejecting - supplier_days)))
                / (pct_new_policy * (1 + (extra_sales / current_sales)))
            )
        )
        if break_even_discount < 0 or break_even_discount > 1:
            break_even_discount = None
    except (ZeroDivisionError, OverflowError):
        break_even_discount = None

    # Βέλτιστη έκπτωση (προσέγγιση)
    optimal_discount = (1 - ((1 + (wacc / 365)) ** (cash_days - current_avg_collection))) / 2

    return {
        "current_avg_collection": current_avg_collection,
        "current_receivables": current_receivables,
        "new_avg_collection": new_avg_collection,
        "new_receivables": new_receivables,
        "release1": release1,
        "pct_new_policy": pct_new_policy,
        "pct_old_policy": pct_old_policy,
        "avg_collection_after_growth": avg_collection_after_growth,
        "receivables_after_growth": receivables_after_growth,
        "release2": release2,
        "profit_extra_sales": profit_extra_sales,
        "release_profit": release_profit,
        "discount_cost": discount_cost,
        "total_profit": total_profit,
        "npv": npv,
        "break_even_discount": break_even_discount,
        "optimal_discount": optimal_discount
    }
