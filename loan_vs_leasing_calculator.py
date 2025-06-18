import streamlit as st
from loan_vs_leasing_logic import pv, limited_depreciation, tax_savings, total_cost
from utils import format_number_gr, parse_gr_number

def loan_vs_leasing_ui():
    st.header("📊 Σύγκριση Δανείου vs Leasing")

    st.markdown("### Γενικές Παράμετροι")
    rate_loan = st.number_input("Επιτόκιο Δανείου (%)", 0.0, 100.0, 6.0) / 100
    rate_wc = st.number_input("Επιτόκιο Κεφαλαίου Κίνησης (%)", 0.0, 100.0, 8.0) / 100
    years = st.number_input("Διάρκεια (Έτη)", 1, 40, 15)
    months = st.number_input("Μήνες ανά έτος", 1, 12, 12)
    when = st.selectbox("Πληρωμή στην αρχή;", ["Ναι", "Όχι"]) == "Ναι"
    total_periods = years * months

    st.markdown("### Στοιχεία Δανείου")
    asset_value_loan = st.number_input("Αξία Ακινήτου (Δάνειο)", value=250000)
    finance_pct_loan = st.number_input("Ποσοστό Χρηματοδότησης (%)", value=70.0) / 100
    extra_costs_loan = st.number_input("Επιπλέον Έξοδα Δανείου", value=35000.0)
    installment_loan = st.number_input("Μηνιαία Δόση Δανείου", value=1469.40)
    working_cap_loan = st.number_input("Δάνειο Κεφαλαίου Κίνησης", value=110000.0)
    installment_wc_loan = st.number_input("Μηνιαία Δόση Κεφαλαίου Κίνησης", value=1044.26)
    depreciation_loan = st.number_input("Αποσβέσεις (15ετία)", value=142500.0)

    st.markdown("### Στοιχεία Leasing")
    asset_value_leasing = st.number_input("Αξία Ακινήτου (Leasing)", value=250000)
    finance_pct_leasing = st.number_input("Ποσοστό Χρηματοδότησης Leasing (%)", value=100.0) / 100
    extra_costs_leasing = st.number_input("Επιπλέον Έξοδα Leasing", value=30000.0)
    installment_leasing = st.number_input("Μηνιαία Δόση Leasing", value=2099.15)
    working_cap_leasing = st.number_input("Δάνειο Κεφαλαίου Κίνησης Leasing", value=30000.0)
    installment_wc_leasing = st.number_input("Μηνιαία Δόση Κεφαλαίου Κίνησης Leasing", value=284.80)
    residual_value = st.number_input("Υπολειμματική Αξία Leasing", value=3530.0)
    depreciation_leasing = st.number_input("Αποσβέσεις Leasing (15ετία)", value=283530.0)

    st.markdown("### Φορολογικές Παράμετροι")
    tax_rate = st.number_input("Φορολογικός Συντελεστής (%)", 0.0, 100.0, 35.0) / 100

    # --- Υπολογισμοί ---
    # Δάνειο
    pv_inst_loan = pv(rate_loan / months, total_periods, installment_loan, 0, int(when))
    pv_wc_loan = pv(rate_wc / months, total_periods, installment_wc_loan, 0, int(when))
    tax_loan = tax_savings(rate_loan, years, pv_inst_loan - asset_value_loan * finance_pct_loan, depreciation_loan, tax_rate)
    total_loan = total_cost(pv_inst_loan, pv_wc_loan, extra_costs_loan, tax_loan)

    # Leasing
    pv_inst_leasing = pv(rate_loan / months, total_periods, installment_leasing, -residual_value, int(when))
    pv_wc_leasing = pv(rate_wc / months, total_periods, installment_wc_leasing, 0, int(when))
    tax_leasing = tax_savings(rate_loan, years, pv_inst_leasing - asset_value_leasing * finance_pct_leasing, depreciation_leasing, tax_rate)
    total_leasing = total_cost(pv_inst_leasing, pv_wc_leasing, extra_costs_leasing, tax_leasing)

    st.markdown("### 🔎 Αποτελέσματα")
    col1, col2 = st.columns(2)
    col1.metric("Τελική Επιβάρυνση Δανείου", format_number_gr(total_loan, symbol="€"))
    col2.metric("Τελική Επιβάρυνση Leasing", format_number_gr(total_leasing, symbol="€"))

    diff = total_loan - total_leasing
    if diff > 0:
        st.success(f"✅ Το Leasing είναι συμφερότερο κατά {format_number_gr(diff, symbol='€')}")
    elif diff < 0:
        st.warning(f"⚠️ Το Δάνειο είναι συμφερότερο κατά {format_number_gr(abs(diff), symbol='€')}")
    else:
        st.info("⚖️ Δεν υπάρχει διαφορά στο συνολικό κόστος.")
