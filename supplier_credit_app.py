import streamlit as st

def format_currency(value):
    return f"{value:,.0f} €".replace(",", ".").replace(".", ",", 1)

def show_supplier_credit_analysis():
    st.title("💰 Ανάλυση Έκπτωσης Προμηθευτή (Προπληρωμή)")

    with st.form("supplier_credit_form"):
        st.subheader("📋 Εισαγωγή Δεδομένων")

        supplier_credit_days = st.number_input("Ημέρες Πίστωσης από Προμηθευτή", min_value=0, value=60)
        discount = st.number_input("Έκπτωση για Προπληρωμή (%)", min_value=0.0, max_value=100.0, value=3.0) / 100
        clients_accept_discount = st.number_input("Ποσοστό Προμηθευτών που Δέχονται (%)", min_value=0.0, max_value=100.0, value=80.0) / 100

        current_sales = st.number_input("Ετήσιες Αγορές (€)", min_value=0.0, value=5_000_000.0)
        unit_price = st.number_input("Τιμή Μονάδας (€)", min_value=0.01, value=10.0)
        total_unit_cost = st.number_input("Συνολικό Κόστος Μονάδας (€)", min_value=0.01, value=8.0)

        interest_rate = st.number_input("Κόστος Κεφαλαίου (% ετησίως)", min_value=0.0, max_value=100.0, value=10.0) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        base_discount_gain = current_sales * discount * clients_accept_discount

        financing_savings = (
            (current_sales / (360 / supplier_credit_days)) * (total_unit_cost / unit_price)
            - ((current_sales * (1 - clients_accept_discount)) / (360 / supplier_credit_days)) * (total_unit_cost / unit_price)
        ) * interest_rate

        total_gain = base_discount_gain - financing_savings

        st.subheader("📊 Αποτελέσματα")
        st.metric("Κέρδος από Έκπτωση Προπληρωμής", format_currency(base_discount_gain))
        st.metric("Εξοικονόμηση από Χρηματοοικονομικό Κόστος", format_currency(financing_savings))
        st.metric("Καθαρό Όφελος από Πολιτική", format_currency(total_gain))

        if total_gain > 0:
            st.success("✅ Συμφέρει η προπληρωμή στους προμηθευτές με έκπτωση.")
        else:
            st.error("❌ Δεν συμφέρει η πολιτική προπληρωμής με βάση τα δεδομένα.")
