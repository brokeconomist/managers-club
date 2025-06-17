import streamlit as st
from utils import parse_gr_number, format_number_gr
from loan_vs_leasing_logic import calculate_scenario

def loan_vs_leasing_ui():
    st.header("📊 Σύγκριση Τραπεζικού Δανεισμού vs Leasing")

    st.markdown("Συμπλήρωσε τα στοιχεία για κάθε εναλλακτική χρηματοδότησης:")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏦 Τραπεζικός Δανεισμός")
        asset_value1 = parse_gr_number(st.text_input("Εμπορική αξία ακινήτου", "250000"))
        funding_rate1 = st.slider("Ποσοστό χρηματοδότησης (%)", 0, 100, 70) / 100
        monthly_payment1 = parse_gr_number(st.text_input("Μηνιαία δόση", "1469"))
        extra_costs1 = parse_gr_number(st.text_input("Επιπλέον έξοδα", "35000"))
        working_cap1 = parse_gr_number(st.text_input("Δάνειο για κεφάλαιο κίνησης", "110000"))
        wc_payment1 = parse_gr_number(st.text_input("Μηνιαία δόση κεφαλαίου κίνησης", "1044"))

    with col2:
        st.subheader("📄 Leasing")
        asset_value2 = parse_gr_number(st.text_input("Εμπορική αξία ακινήτου ", "250000", key="asset2"))
        funding_rate2 = st.slider("Ποσοστό χρηματοδότησης (%) ", 0, 100, 100, key="funding2") / 100
        monthly_payment2 = parse_gr_number(st.text_input("Μηνιαία δόση ", "2099", key="payment2"))
        extra_costs2 = parse_gr_number(st.text_input("Επιπλέον έξοδα ", "30000", key="costs2"))
        working_cap2 = parse_gr_number(st.text_input("Δάνειο για κεφάλαιο κίνησης ", "30000", key="cap2"))
        wc_payment2 = parse_gr_number(st.text_input("Μηνιαία δόση κεφαλαίου κίνησης ", "285", key="wcp2"))

    st.divider()
    st.subheader("⚙️ Κοινοί Παράμετροι")
    loan_rate = st.number_input("Επιτόκιο Δανείου (%)", value=6.0) / 100
    wc_rate = st.number_input("Επιτόκιο Κεφαλαίου Κίνησης (%)", value=8.0) / 100
    years = st.number_input("Διάρκεια (έτη)", value=15, step=1)
    months = st.number_input("Μήνες ανά έτος", value=12, step=1)
    when = st.radio("Χρόνος πληρωμής", ["Στην αρχή", "Στο τέλος"]) == "Στην αρχή"
    depreciation_years = st.number_input("Συνολικός χρόνος απόσβεσης (έτη)", value=30, step=1)
    residual_value = parse_gr_number(st.text_input("Υπολειμματική αξία leasing", "3530"))
    tax_rate = st.number_input("Φορολογικός συντελεστής (%)", value=35.0) / 100

    if st.button("📈 Υπολογισμός"):
        params1 = {
            "loan_rate": loan_rate,
            "wc_rate": wc_rate,
            "years": years,
            "months": months,
            "when": int(when),
            "asset_value": asset_value1,
            "funding_rate": funding_rate1,
            "monthly_payment": monthly_payment1,
            "extra_costs": extra_costs1,
            "working_capital": working_cap1,
            "working_cap_payment": wc_payment1,
            "residual_value": 0,
            "depreciation_years": depreciation_years,
            "tax_rate": tax_rate
        }

        params2 = {
            **params1,
            "asset_value": asset_value2,
            "funding_rate": funding_rate2,
            "monthly_payment": monthly_payment2,
            "extra_costs": extra_costs2,
            "working_capital": working_cap2,
            "working_cap_payment": wc_payment2,
            "residual_value": residual_value
        }

        result1 = calculate_scenario(params1)
        result2 = calculate_scenario(params2)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🏦 Τραπεζικός Δανεισμός")
            show_results(result1)

        with col2:
            st.subheader("📄 Leasing")
            show_results(result2)

        st.divider()
        better = "Leasing" if result2["total_cost"] < result1["total_cost"] else "Τραπεζικός Δανεισμός"
        diff = abs(result1["total_cost"] - result2["total_cost"])
        st.info(f"Διαφορά υπέρ **{better}**: **{format_number_gr(diff)} €**")

def show_results(result):
    st.write(f"• Παρούσα αξία δόσεων: **{format_number_gr(abs(result['pv_installments']))} €**")
    st.write(f"• Παρούσα αξία κεφαλαίου κίνησης: **{format_number_gr(abs(result['pv_working_cap']))} €**")
    st.write(f"• Αποσβέσεις: **{format_number_gr(abs(result['depreciation']))} €**")
    st.write(f"• Συνολικοί τόκοι: **{format_number_gr(abs(result['interest_total']))} €**")
    st.write(f"• Φορολογικό όφελος: **{format_number_gr(abs(result['tax_savings']))} €**")
    st.success(f"✅ Τελική επιβάρυνση: **{format_number_gr(abs(result['total_cost']))} €**")
