import streamlit as st
from scipy.optimize import bisect

# === Υποστηρικτικές συναρτήσεις μορφοποίησης ===
def format_percentage_gr(value):
    return f"{value * 100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def parse_gr_number(number_str):
    try:
        return float(number_str.replace(".", "").replace(",", "."))
    except:
        return 0.0

# === Λογισμός Dmax ===
def calculate_dmax(
    current_avg_collection,
    days_cash_payment,
    wacc,
    annual_sales,
    percent_accepting_discount
):
    discount_rate_daily = wacc / 365
    delta_days = current_avg_collection - days_cash_payment

    if delta_days <= 0 or percent_accepting_discount == 0:
        return 0.0

    def npv_with_discount(d):
        cash_sales = annual_sales * percent_accepting_discount
        benefit = (cash_sales * (1 - d)) / ((1 + discount_rate_daily) ** delta_days)
        return benefit - cash_sales

    try:
        dmax = bisect(npv_with_discount, 0.0001, 0.5)
        return dmax
    except ValueError:
        return 0.0

# === Streamlit UI ===
st.set_page_config(page_title="Υπολογιστής Μέγιστης Έκπτωσης (Dmax)", page_icon="💸")

st.title("💸 Υπολογιστής Μέγιστης Αποδεκτής Έκπτωσης Τοις Μετρητοίς (Dmax)")

col1, col2 = st.columns(2)

with col1:
    current_avg_collection = st.number_input("Μέσος χρόνος είσπραξης (ημέρες)", min_value=1, value=60)
    days_cash_payment = st.number_input("Ημέρες είσπραξης με μετρητοίς", min_value=0, value=10)
    annual_sales_str = st.text_input("Ετήσιες πωλήσεις (€)", "500.000")

with col2:
    wacc_percent = st.text_input("WACC (% ετησίως)", "12,0")
    percent_accepting_str = st.text_input("Ποσοστό πελατών που αποδέχεται την έκπτωση (%)", "40,0")

# Μετατροπές
annual_sales = parse_gr_number(annual_sales_str)
wacc = parse_gr_number(wacc_percent) / 100
percent_accepting = parse_gr_number(percent_accepting_str) / 100

# Υπολογισμός
dmax = calculate_dmax(
    current_avg_collection,
    days_cash_payment,
    wacc,
    annual_sales,
    percent_accepting
)

# Αποτέλεσμα
st.subheader("📊 Μέγιστο Αποδεκτό Ποσοστό Έκπτωσης")
st.success(f"🔹 {format_percentage_gr(dmax)} τοις εκατό")

st.caption("Υπολογίζεται με βάση το WACC, τις ημέρες είσπραξης, τις πωλήσεις και το ποσοστό αποδοχής.")
