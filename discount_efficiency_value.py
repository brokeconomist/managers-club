def calculate_cash_discount_metrics(old_sales, new_sales, avg_days, new_avg_days,
                                    discount_rate, cash_percent, wacc):
    # Αποδέσμευση κεφαλαίου
    release = (old_sales * avg_days - new_sales * new_avg_days) / 360

    # Όφελος από την αποδέσμευση (NPV)
    benefit = release * wacc

    # Ζημία λόγω έκπτωσης
    loss = new_sales * discount_rate * cash_percent

    # Καθαρή Παρούσα Αξία
    npv = benefit - loss

    # Μέγιστη και βέλτιστη έκπτωση
    try:
        max_discount = benefit / new_sales if new_sales != 0 else 0
        optimal_discount = benefit / (new_sales * cash_percent) if new_sales * cash_percent != 0 else 0
    except ZeroDivisionError:
        max_discount = 0
        optimal_discount = 0

    return {
        "release": release,
        "benefit": benefit,
        "loss": loss,
        "npv": npv,
        "max_discount": max_discount,
        "optimal_discount": optimal_discount
    }
