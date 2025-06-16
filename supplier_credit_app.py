import streamlit as st

def calculate_supplier_credit_gain(SupplierCreditDays, Discount, Clients, CurrentSales, UnitPrice, TotalUnitCost, InterestRateOnDebt):
    # Μετατροπή ποσοστών σε δεκαδικούς
    Discount = Discount / 100
    Clients = Clients / 100
    InterestRateOnDebt = InterestRateOnDebt / 100

    # Κέρδος από την έκπτωση επί των πωλήσεων σε πελάτες που πληρώνουν άμεσα
    discount_gain = CurrentSales * Discount * Clients

    # Κόστος ευκαιρίας από απώλεια πίστωσης
    average_cost = TotalUnitCost / UnitPrice
    credit_benefit = ((CurrentSales / (360 / SupplierCreditDays)) * average_cost
                     - ((CurrentSales * (1 - Clients)) / (360 / SupplierCreditDays)) * average_cost) * InterestRateOnDebt

    net_gain = discount_gain - credit_benefit
    return discount_gain, credit_benefit, net_gain

def format_currency(amount):
    return f"{amount:,.0f} €".replace(",", ".")

def show_supplier_credit_analysis():
    st.title("🏦 Ανάλυση Πίστωσης Προμηθευτών (Έκπτωση)")
    st.markdown("Αξιολόγηση απόδοσης από την **πληρωμή μετρητοίς με έκπτωση** σε σχέση με πίστωση από τον προμηθευτή.")

    with st.form("supplier_credit_form"):
        col1, col2 = st.columns(2)
        with col1:
            SupplierCreditDays = st.number_input("📆 Ημέρες Πίστωσης από Προμηθευτή", min_value=0, value=60)
            Discount = st.number_input("💸 Ποσοστό Έκπτωσης για Πληρωμή Μετρητοίς (%)", min_value=0.0, value=2.0)
            Clients = st.number_input("👥 Ποσοστό Πωλήσεων που Πληρώνοναι Μετρητοίς (%)", min_value=0.0, max_value=100.0, value=50.0)

        with col2:
            CurrentSales = st.number_input("💰 Τρέχουσες Πωλήσεις (€)", min_value=0, value=2_000_000)
            UnitPrice = st.number_input("📦 Τιμή Μονάδας (€)", min_value=0.01, value=20.0)
            TotalUnitCost = st.number_input("🧾 Συνολικό Κόστος Μονάδας (€)", min_value=0.01, value=18.0)
            InterestRateOnDebt = st.number_input("🏦 Κόστος Κεφαλαίου (%)", min_value=0.0, value=10.0)

        submitted = st.form_submit_button("🔍 Υπολογισμός")

    if submitted:
        discount_gain, credit_cost, net_gain = calculate_supplier_credit_gain(
            SupplierCreditDays, Discount, Clients,
            CurrentSales, UnitPrice, TotalUnitCost, InterestRateOnDebt
        )

        st.subheader("📊 Αποτελέσματα")
        st.metric("✅ Κέρδος από Έκπτωση", format_currency(discount_gain))
        st.metric("💸 Κόστος Απώλειας Πίστωσης", format_currency(credit_cost))
        st.metric("🏁 Καθαρό Όφελος", format_currency(net_gain), delta_color="normal" if net_gain >= 0 else "inverse")

        if net_gain > 0:
            st.success("👉 Συμφέρει να πληρώνετε με μετρητά με την προτεινόμενη έκπτωση.")
        else:
            st.error("⚠️ Δεν συμφέρει η πληρωμή με μετρητά με την έκπτωση αυτή.")
