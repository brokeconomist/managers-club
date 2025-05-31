# utils.py
def format_number_gr(value):
    # π.χ. μετατροπή σε ελληνικό format: κόμμα για δεκαδικά, τελεία για χιλιάδες
    if value is None:
        return ""
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def parse_gr_number(text):
    try:
        # Αντικατάσταση ελληνικού format σε float
        return float(text.replace(".", "").replace(",", "."))
    except Exception:
        return None
        
def format_percentage_gr(value):
    try:
        return f"{value:.2f}".replace('.', ',') + '%'
    except:
        return "-"
