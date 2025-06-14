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

def format_percentage_gr(x):
    try:
        val = x * 100
        if val.is_integer():
            s = f"{int(val):,}".replace(",", "X").replace(".", ",").replace("X", ".")
            return s + " %"
        else:
            return format_number_gr(val) + " %"
    except:
        return str(x)
