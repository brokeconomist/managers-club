import streamlit as st

def format_number_gr(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(x):
    return f"{x * 100:.2f}%".replace(".", ",")

def calculate_max_discount_only_extra_sales(
    current_sales,
    extra_sales,
    variable_cost_pct,
    pct_accept_discount,
    days_cash_payment,
    days_reject_discount,
    current_avg_collection,
    supplier_payment_days,
    wacc
):
    r = wacc / 365
    g = extra_sales / current_sales if current_sales > 0 else 0
    y = variable_cost_pct
    p = pct_accept_discount
    M = days_cash_payment
    Q = days_reject_discount
    N = current_avg_collection
    C = supplier_payment_days

    try:
        numerator = 1 - (1 / p) + (1 + r) ** (Q - N) + y * g * (1 + r) ** (Q - C)
        denominator = p * (1 + g)
        base = (1 + r) ** (M - Q)
        max_discount = 1 - base * (numerator / denominator)
    except ZeroDivisionError:
        max_discount = None

    return max_discount

def show_discount_efficiency_ui():
    st.title("Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς")

    col1, col2 = st.columns(2)

    with col1:
        current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", value=1000.0, step=10.0)
        extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", value=250.0, step=10.0)
        variable_cost_pct = st.number_input("Κόστος πωλήσεων (%)", value=80.0, min_value=0.0, max_value=100.0) / 100
        pct_accept_discount = st.number_input("% πελατών που αποδέχεται την έκπτωση", value=60.0, min_value=0.1, max_value=100.0) / 100
        days_cash_payment = st.number_input("Μέρες πληρωμής με έκπτωση", value=10, step=1)

    with col2:
        days_reject_discount = st.number_input("Μέρες πληρωμής χωρίς έκπτωση", value=120, step=1)
        current_avg_collection = st.number_input("Τρέχουσα μέση περίοδος είσπραξης", value=84.0, step=1.0)
        supplier_payment_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών", value=30, step=1)
        wacc = st.number_input("Κόστος κεφαλαίου (WACC %)", value=20.0, min_value=0.0, max_value=100.0) / 100

    st.markdown("---")

    max_discount = calculate_max_discount_only_extra_sales(
        current_sales,
        extra_sales,
        variable_cost_pct,
        pct_accept_discount,
        days_cash_payment,
        days_reject_discount,
        current_avg_collection,
        supplier_payment_days,
        wacc
    )

    st.subheader("Αποτέλεσμα")
    if max_discount is not None and 0 <= max_discount <= 1:
        st.success(f"Μέγιστη έκπτωση (μόνο επί των επιπλέον πωλήσεων): {format_percentage_gr(max_discount)}")
    else:
        st.error("Δεν μπορεί να υπολογιστεί έγκυρη μέγιστη έκπτωση (ελέγξτε τις τιμές εισόδου)")
