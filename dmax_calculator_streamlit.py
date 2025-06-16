import streamlit as st

# === Υποστηρικτικές συναρτήσεις ===
def parse_gr_number(number_str):
    try:
        return float(number_str.replace(".", "").replace(",", "."))
    except:
        return 0.0

def format_percentage_gr(value):
    return f"{value * 100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# === Συνάρτηση υπολογισμού Dmax ===
def calculate_dmax_excel_compatible(
    current_sales,
    extra_sales,
    prc_clients_take_disc,
    days_clients_take_discount,
    days_clients_not_take_discount,
    new_days_payment_clients_take_discount,
    COGS,
    WACC,
    avg_days_pay_suppliers,
    avg_current_collection_days
):
    WACC_daily = WACC / 365
    Δsales_over_sales = extra_sales / current_sales
    p = prc_clients_take_disc

    try:
        power1 = (1 + WACC_daily) ** (new_days_payment_clients_take_discount - days_clients_not_take_discount)
        power2 = (1 + WACC_daily) ** (days_clients_not_take_discount - avg_current_collection_days)
        power3 = (1 + WACC_daily) ** (days_clients_not_take_discount - avg_days_pay_suppliers)

        numerator = (
            1 - (1 / p) +
            power2 +
            COGS * Δsales_over_sales * power3
        )

        denominator = p * (1 + Δsales_over_sales)

        dmax = 1 - (power1 * (numerator / denominator))
        return dmax
    except Exception:
        return 0.0

# === Streamlit UI ===
st.set_page_config(page_title="Μέγιστο Ποσοστό Έκπτωσης (Dmax)", page_icon="💸")

st.title("💸 Υπολογιστής Μέγιστης Αποδεκτής Έκπτωσης (Dmax)")

st.markdown("Υπολογισμός βασισμένος σε αύξηση πωλήσεων, WACC και κόστος.")

col1, col2 = st.columns(2)

with col1:
    current_sales_str = st.text_input("Τρέχουσες πωλήσεις (€)", "1.000")
    extra_sales_str = st.text_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", "250")
    prc_clients_take_disc_str = st.text_input("Ποσοστό πελατών που αποδέχονται την έκπτωση (%)", "40,0")
    COGS_str = st.text_input("Κόστος Πωληθέντων (COGS %)", "80,0")
    WACC_str = st.text_input("WACC (% ετησίως)", "20,0")

with col2:
    days_clients_take_discount = st.number_input("Ημέρες πληρωμής πελατών που αποδέχονται την έκπτωση", min_value=0, value=60)
    days_clients_not_take_discount = st.number_input("Ημέρες πληρωμής πελατών που **δεν** αποδέχονται την έκπτωση", min_value=1, value=120)
    new_days_payment_clients_take_discount = st.number_input("Νέες ημέρες πληρωμής με μετρητοίς", min_value=0, value=10)
    avg_days_pay_suppliers = st.number_input("Μέσος χρόνος πληρωμής προμηθευτών", min_value=0, value=30)
    avg_current_collection_days = st.number_input("Μέσος τρέχων χρόνος είσπραξης (ημέρες)", min_value=1, value=96)

# === Μετατροπές ===
current_sales = parse_gr_number(current_sales_str)
extra_sales = parse_gr_number(extra_sales_str)
prc_clients_take_disc = parse_gr_number(prc_clients_take_disc_str) / 100
COGS = parse_gr_number(COGS_str) / 100
WACC = parse_gr_number(WACC_str) / 100

# === Υπολογισμός ===
dmax = calculate_dmax_excel_compatible(
    current_sales,
    extra_sales,
    prc_clients_take_disc,
    days_clients_take_discount,
    days_clients_not_take_discount,
    new_days_payment_clients_take_discount,
    COGS,
    WACC,
    avg_days_pay_suppliers,
    avg_current_collection_days
)

# === Αποτέλεσμα ===
st.subheader("📊 Μέγιστο Αποδεκτό Ποσοστό Έκπτωσης")
st.success(f"🔹 {format_percentage_gr(dmax)} τοις εκατό")

st.caption("Η έκπτωση αυτή δεν δημιουργεί οικονομική ζημία με βάση τις παραδοχές για WACC, COGS και εισπρακτικό κύκλο.")
