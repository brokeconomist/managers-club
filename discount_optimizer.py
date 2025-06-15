import streamlit as st
from discount_logic import calculate_discount_analysis, optimize_discount

st.set_page_config(page_title="Ανάλυση Έκπτωσης Τοις Μετρητοίς", layout="centered")

st.title("💸 Ανάλυση Έκπτωσης και Πληρωμής Τοις Μετρητοίς")
st.markdown("Υπολογισμός κόστους και οφέλους από πολιτική παροχής έκπτωσης για πληρωμή τοις μετρητοίς.")

with st.form("input_form"):
    sales = st.number_input("Τρέχουσες πωλήσεις", value=1000.0)
    extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης", value=250.0)
    discount_rate = st.number_input("Έκπτωση %", min_value=0.0, max_value=1.0, value=0.02, step=0.01, format="%.4f")
    acceptance_rate = st.number_input("Ποσοστό πελατών που αποδέχεται την έκπτωση", min_value=0.0, max_value=1.0, value=0.60)
    acceptance_days = st.number_input("Μέρες πληρωμής πελατών με έκπτωση", value=10)
    rejection_days = st.number_input("Μέρες πληρωμής πελατών χωρίς έκπτωση", value=120)
    cost_rate = st.number_input("Κόστος πωληθέντων %", min_value=0.0, max_value=1.0, value=0.80)
    wacc = st.number_input("Κόστος κεφαλαίου (WACC) %", min_value=0.0, max_value=1.0, value=0.20)
    current_collection_days = st.number_input("Τρέχουσα μέση περίοδος είσπραξης", value=84)
    supplier_payment_days = st.number_input("Μέρες αποπληρωμής προμηθευτών", value=30)

    submitted = st.form_submit_button("Υπολογισμός")

if submitted:
    results = calculate_discount_analysis(
        sales,
        extra_sales,
        discount_rate,
        acceptance_rate,
        acceptance_days,
        1 - acceptance_rate,
        rejection_days,
        acceptance_days,
        cost_rate,
        wacc,
        current_collection_days,
        supplier_payment_days,
    )

    st.subheader("📊 Αποτελέσματα")
    st.write(f"Κέρδος από επιπλέον πωλήσεις: **{results['profit_extra_sales']:.2f}**")
    st.write(f"Αποδέσμευση κεφαλαίων: **{results['freed_capital']:.2f}**")
    st.write(f"Κόστος έκπτωσης: **{results['discount_cost']:.2f}**")
    st.write(f"Καθαρό όφελος: **{results['total_net_gain']:.2f}**")
    if results["d_max"] is not None:
        st.write(f"Μέγιστη έκπτωση βάσει NPV: **{results['d_max']*100:.2f}%**")
    else:
        st.write("⚠️ Δεν ήταν δυνατός ο υπολογισμός της μέγιστης έκπτωσης (διαίρεση με 0).")

    st.subheader("📈 Βέλτιστη Έκπτωση")
    best_discount, best_gain = optimize_discount(
        sales,
        extra_sales,
        acceptance_rate,
        acceptance_days,
        rejection_days,
        acceptance_days,
        cost_rate,
        wacc,
        current_collection_days,
        supplier_payment_days,
    )

    st.write(f"✅ Βέλτιστη Έκπτωση: **{best_discount*100:.2f}%**")
    st.write(f"Καθαρό Όφελος στη βέλτιστη έκπτωση: **{best_gain:.2f}**")
