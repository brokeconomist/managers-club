import streamlit as st

def format_currency(value, decimals=2):
    try:
        formatted = f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{formatted} €"
    except Exception:
        return f"{value} €"

def show_credit_policy_analysis():
    st.title("🕵️‍♂️ Αξιολόγηση Πολιτικής Πίστωσης")

    with st.form("credit_policy_form"):
        st.subheader("📌 Παρούσα Κατάσταση")
        current_cash = st.number_input("Ποσοστό Πωλήσεων Μετρητοίς (%)", min_value=0.0, max_value=100.0, value=50.0) / 100
        current_credit_pct = st.number_input("Ποσοστό Πωλήσεων με Πίστωση (%)", min_value=0.0, max_value=100.0, value=50.0) / 100
        current_credit_days = st.number_input("Ημέρες Πίστωσης (Παρούσα)", min_value=0, value=60)

        st.subheader("📌 Νέα Κατάσταση")
        new_cash = st.number_input("Νέο Ποσοστό Πωλήσεων Μετρητοίς (%)", min_value=0.0, max_value=100.0, value=20.0) / 100
        new_credit_pct = st.number_input("Νέο Ποσοστό Πωλήσεων με Πίστωση (%)", min_value=0.0, max_value=100.0, value=80.0) / 100
        new_credit_days = st.number_input("Ημέρες Πίστωσης (Νέα)", min_value=0, value=90)

        st.subheader("📈 Στοιχεία Πωλήσεων")
        sales_increase = st.number_input("Αναμενόμενη Αύξηση Πωλήσεων (%)", min_value=0.0, value=20.0) / 100
        current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", min_value=0.0, value=20_000_000.0)
        unit_price = st.number_input("Τιμή Μονάδας (€)", min_value=0.01, value=20.0)
        total_unit_cost = st.number_input("Συνολικό Κόστος Μονάδας (€)", min_value=0.01, value=18.0)
        variable_unit_cost = st.number_input("Μεταβλητό Κόστος Μονάδας (€)", min_value=0.01, value=14.0)
        expected_bad_debts = st.number_input("Ποσοστό Επισφαλών Απαιτήσεων (%)", min_value=0.0, max_value=100.0, value=2.0) / 100
        interest_rate = st.number_input("Κόστος Κεφαλαίου (% ετησίως)", min_value=0.0, max_value=100.0, value=10.0) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        # Μονάδες και κέρδος από αύξηση
        base_units = current_sales / unit_price
        increased_units = base_units * sales_increase
        profit_increase = increased_units * (unit_price - variable_unit_cost)

        # Κόστος αύξησης κεφαλαίου (διορθωμένος τύπος)
        avg_cost_per_unit = (
            ((base_units * total_unit_cost) + (increased_units * variable_unit_cost)) /
            (base_units + increased_units)
        )
        new_credit_sales = (current_sales * (1 + new_cash)) * new_credit_pct
        current_credit_sales = current_sales * current_cash

        capital_cost_new = (new_credit_sales / (360 / new_credit_days)) * (avg_cost_per_unit / unit_price)
        capital_cost_current = (current_credit_sales / (360 / current_credit_days)) * (total_unit_cost / unit_price)
        capital_cost_difference = capital_cost_new - capital_cost_current
        financial_cost = capital_cost_difference * interest_rate

        # Επισφάλειες
        bad_debts_cost = current_sales * expected_bad_debts + current_sales * expected_bad_debts * sales_increase

        # Σύνολο κόστους
        total_cost = financial_cost + bad_debts_cost

        # Τελική αξιολόγηση
        anticipated_gain = profit_increase - total_cost
        suggestion = "✅ Αύξηση Πίστωσης" if anticipated_gain > 0 else "❌ ΜΗ Αύξηση Πίστωσης"

        # Αποτελέσματα
        st.subheader("📊 Αποτελέσματα")
        st.metric("Καθαρό Κέρδος από Επιπλέον Πωλήσεις", format_currency(profit_increase))
        st.metric("Συνολικό Κόστος από την Αύξηση", format_currency(total_cost))
        st.metric("Καθαρό Όφελος", format_currency(anticipated_gain))
        st.success(f"Πρόταση: {suggestion}")
