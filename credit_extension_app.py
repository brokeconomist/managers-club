import streamlit as st

def calculate_credit_extension(
    current_credit_days,
    new_credit_days,
    sales,
    price_per_unit,
    total_cost_per_unit,
    variable_cost_per_unit,
    sales_increase_pct,
    bad_debt_pct,
    capital_cost_pct
):
    # Υπολογισμός βασικών μεγεθών
    units = sales / price_per_unit
    new_sales = sales * (1 + sales_increase_pct / 100)
    new_units = new_sales / price_per_unit
    additional_units = new_units - units

    gross_profit_extra_sales = additional_units * (price_per_unit - variable_cost_per_unit)

    # Κόστος ανά μονάδα μετά την αύξηση (νέος σταθμισμένος μέσος όρος)
    total_cost_initial = units * total_cost_per_unit
    total_cost_extra = additional_units * variable_cost_per_unit
    total_cost_all = total_cost_initial + total_cost_extra
    cost_per_unit_new = total_cost_all / new_units

    # Δέσμευση κεφαλαίου = (Πωλήσεις x Κόστος ανά μονάδα) x (Μέρες / 365)
    old_capital = sales * total_cost_per_unit * (current_credit_days / 365)
    new_capital = new_sales * cost_per_unit_new * (new_credit_days / 365)
    extra_capital = new_capital - old_capital

    # Κόστη
    cost_of_extra_capital = extra_capital * (capital_cost_pct / 100)
    bad_debt_cost = (new_sales - sales) * (bad_debt_pct / 100)
    total_cost = cost_of_extra_capital + bad_debt_cost

    # Συνολικό εκτιμώμενο όφελος
    net_benefit = gross_profit_extra_sales - total_cost

    return {
        "Νέες Πωλήσεις (€)": new_sales,
        "Νέο Κόστος ανα μονάδα (€)": round(cost_per_unit_new, 2),
        "Παρούσα Δέσμευση Κεφαλαίων (€)": round(old_capital, 0),
        "Νέα Δέσμευση Κεφαλαίων (€)": round(new_capital, 0),
        "Επιπλέον Δέσμευση Κεφαλαίων (€)": round(extra_capital, 0),
        "Κόστος Επιπλέον Δέσμευσης Κεφαλαίων (€)": round(cost_of_extra_capital, 0),
        "Κόστος Επισφαλειών (€)": round(bad_debt_cost, 0),
        "Συνολικό Κόστος (€)": round(total_cost, 0),
        "Καθαρό Όφελος (€)": round(net_benefit, 0)
    }

st.set_page_config(page_title="Αύξηση Πίστωσης - Υπολογισμός", layout="centered")
st.title("📈 Υπολογισμός Επίπτωσης Αύξησης Πίστωσης")

st.markdown("Εισάγετε τα στοιχεία για να υπολογίσετε την επίπτωση από την επέκταση της περιόδου πίστωσης.")

with st.form("credit_form"):
    col1, col2 = st.columns(2)
    with col1:
        current_credit_days = st.number_input("Τρέχουσες Μέρες Πίστωσης", value=60)
        price_per_unit = st.number_input("Τιμή Προϊόντος (€)", value=20.0)
        total_cost_per_unit = st.number_input("Συνολικό Κόστος ανά Μονάδα (€)", value=18.0)
        capital_cost_pct = st.number_input("Κόστος Κεφαλαίου (%)", value=10.0)
    with col2:
        new_credit_days = st.number_input("Νέες Μέρες Πίστωσης", value=90)
        variable_cost_per_unit = st.number_input("Μεταβλητό Κόστος ανά Μονάδα (€)", value=14.0)
        sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=200000.0)
        bad_debt_pct = st.number_input("Ποσοστό Επισφαλειών (%)", value=2.0)

    sales_increase_pct = st.slider("Ποσοστό Αύξησης Πωλήσεων (%)", 0.0, 100.0, 20.0)

    submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        results = calculate_credit_extension(
            current_credit_days,
            new_credit_days,
            sales,
            price_per_unit,
            total_cost_per_unit,
            variable_cost_per_unit,
            sales_increase_pct,
            bad_debt_pct,
            capital_cost_pct
        )

        st.subheader("📊 Αποτελέσματα")
        for key, value in results.items():
            st.metric(label=key, value=f"€ {value:,.0f}")
