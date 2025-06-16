def calculate_max_cash_discount(days_saved: float, annual_rate: float) -> float:
    """
    Υπολογίζει τη μέγιστη αποδεκτή έκπτωση που μπορεί να δοθεί,
    βάσει ημερών πρόωρης πληρωμής και ετήσιου κόστους κεφαλαίου (WACC).

    Parameters:
    - days_saved: αριθμός ημερών που κερδίζονται με πρόωρη πληρωμή
    - annual_rate: ετήσιο κόστος κεφαλαίου (π.χ. 0.12 για 12%)

    Returns:
    - max_discount: μέγιστο ποσοστό έκπτωσης (π.χ. 0.025 για 2.5%)
    """
    daily_rate = (1 + annual_rate) ** (1 / 365) - 1
    max_discount = (1 + daily_rate) ** days_saved - 1
    return max_discount
