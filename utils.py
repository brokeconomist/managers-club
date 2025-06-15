def format_number_gr(x):
    try:
        s = f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return s
    except:
        return str(x)

def parse_gr_number(x):
    try:
        # Αν είναι ήδη float ή int το επιστρέφει
        if isinstance(x, (float, int)):
            return x
        return float(x.replace(".", "").replace(",", "."))
    except:
        return 0.0

def format_percentage_gr(value, decimals=2):
    if value is None:
        return "-"
    return f"{value * 100:,.{decimals}f}%".replace(",", "#").replace(".", ",").replace("#", ".")
