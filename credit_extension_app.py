import streamlit as st
from credit_extension_analysis import calculate_credit_extension_simple

st.set_page_config(page_title="Ανάλυση Επέκτασης Πίστωσης", layout="centered")

st.title("📊 Ανάλυση Επέκτασης Χρόνου Πίστωσης")

# 🔸 Συνάρτηση μετατροπής ελληνικού αριθμού σε float
def parse_greek_number(text):
    try:
        return float(text.replace('.', '').replace(',', '.'))
    except:
        return 0.0

st.header("📌 Τρέχουσα Κατάσταση")
current_credit_days = int(st.text_input("Μέρες Πίστωσης", value="60"))

st.header("📈 Νέα Πρόταση")
new_credit_days = int(st.text_input("Νέες Μέρες Πίστωσης", value="90"))
sales_increase_pct = parse_greek_number(st.text_input("Ποσοστό Αύξησης Πωλήσεων (%)", value="20,0")) / 100

st.header("💼 Οικονομικά Δεδομένα")
current_sales = parse_greek_number(st.text_input("Τρέχουσες Πωλήσεις (€)", value="20.000.000"))
unit_price = parse_greek_number(st.text_input("Τιμή Μονάδας (€)", value="20,0"))
total_unit_cost = parse_greek_number(st.text_input("Συνολικό Κόστος ανά Μονάδα (€)", value="18,0"))
variable_unit_cost = parse_greek_number(st.text_input("Μεταβλητό Κόστος ανά Μονάδα (€)", value="14,0"))
bad_debt_pct = parse_greek_number(st.text_input("Ποσοστό Επισφαλειών (%)", value="2,0")) / 100
capital_cost_pct = parse_greek_number(st.text_input("Κόστος Κεφαλαίου (%)", value="10,0")) / 100

# 🔸 Συνάρτηση μορφοποίησης ελληνικού ποσού
def format_currency(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

if st.button("Υπολογισμός"):
    results = calculate_credit_extension_simple(
        current_credit_days,
        new_credit_days,
        sales_increase_pct,
        current_sales,
        unit_price,
        total_unit_cost,
        variable_unit_cost,
        bad_debt_pct,
        capital_cost_pct,
    )

    st.header("📊 Αποτελέσματα")
    st.metric("Καθαρό Κέρδος (€)", format_currency(results['Net Profit']))
    st.metric("Συνολικό Κόστος (€)", format_currency(results['Total Cost from Increase']))
    st.metric("Εκτιμώμενο Κέρδος (€)", format_currency(results['Anticipated Gain']))
    st.success(f"Πρόταση: {results['Suggestion']}")
