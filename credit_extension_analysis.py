import streamlit as st
from utils import format_number_gr, format_percentage_gr

def calculate_credit_extension_impact(
    current_sales,
    unit_price,
    unit_cost,
    sales_increase_pct,
    bad_debt_pct,
    capital_cost_pct,
    days_extension
):
    try:
        # Υπολογισμός νέων πωλήσεων
        increased_sales = current_sales * (1 + sales_increase_pct / 100)

        # Επιπλέον πωλήσεις
        extra_sales = increased_sales - current_sales

        # Μικτό Κέρδος από τις επιπλέον πωλήσεις
        gross_margin_per_unit = unit_price - unit_cost
        extra_units_sold = extra_sales / unit_price
        gross_profit = extra_units_sold * gross_margin_per_unit

        # Κόστος κεφαλαίου από την αύξηση πίστωσης
        capital_cost = (increased_sales * days_extension / 365) * (capital_cost_pct / 100)

        # Κόστος επισφαλειών
        bad_debt_cost = increased_sales * (bad_debt_pct / 100)

        # Συνολικό Κόστος
        total_cost = capital_cost + bad_debt_cost

        # Καθαρό Κέρδος
        net_profit = gross_profit - total_cost

        return {
            "Gross Profit": gross_profit,
            "Capital Cost": capital_cost,
            "Bad Debt Cost": bad_debt_cost,
            "Total Cost from Increase": total_cost,
            "Net Profit": net_profit,
            "Anticipated Gain": gross_profit - total_cost,
            "Suggestion": "Increase Credit" if net_profit > 0 else "Do Not Increase"
        }
    except Exception as e:
        return {"error": str(e)}

def show_credit_extension_analysis():
    st.title("🕒 Ανάλυση Αύξησης Πίστωσης")

    st.markdown("Αναλύστε αν συμφέρει η επέκταση του χρόνου πίστωσης με βάση τα οικονομικά στοιχεία της επιχείρησης.")

    with st.form("credit_extension_form"):
        col1, col2 = st.columns(2)
        with col1:
            current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=20_000_000, step=100_000)
            unit_price = st.number_input("Τιμή Μονάδας (€)", value=100.0, step=1.0)
            unit_cost = st.number_input("Μεταβλητό Κόστος Μονάδας (€)", value=60.0, step=1.0)
            sales_increase_pct = st.number_input("Εκτιμώμενη Αύξηση Πωλήσεων (%)", value=10.0, step=0.5)

        with col2:
            capital_cost_pct = st.number_input("Κόστος Κεφαλαίου (%)", value=12.0, step=0.5)
            bad_debt_pct = st.number_input("Ποσοστό Επισφαλειών (%)", value=1.0, step=0.1)
            days_extension = st.number_input("Επέκταση Πίστωσης (Ημέρες)", value=30, step=5)

        submitted = st.form_submit_button("📊 Υπολογισμός")

    if submitted:
        results = calculate_credit_extension_impact(
            current_sales,
            unit_price,
            unit_cost,
            sales_increase_pct,
            bad_debt_pct,
            capital_cost_pct,
            days_extension
        )

        if "error" in results:
            st.error(f"❌ Σφάλμα: {results['error']}")
            return

        st.header("📊 Αποτελέσματα")
        st.metric("Καθαρό Κέρδος (€)", format_number_gr(results["Net Profit"]))
        st.metric("Συνολικό Κόστος (€)", format_number_gr(results["Total Cost from Increase"]))
        st.metric("Εκτιμώμενο Κέρδος (€)", format_number_gr(results["Anticipated Gain"]))

        if results["Suggestion"] == "Increase Credit":
            st.success("📌 Πρόταση: ✅ Αύξησε την Πίστωση")
        else:
            st.warning("📌 Πρόταση: ⛔️ Μην Αυξήσεις την Πίστωση")
