def format_number_gr(x, decimals=2):
    return f"{x:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(x, decimals=1):
    return f"{x * 100:.{decimals}f}%".replace(".", ",")

def parse_gr_number(x):
    try:
        # Αν είναι ήδη float ή int το επιστρέφει
        if isinstance(x, (float, int)):
            return x
        return float(x.replace(".", "").replace(",", "."))
    except:
        return 0.0
