import streamlit as st
import math

def show_economic_order_quantity():
    st.title("Οικονομικότερη Παραγγελία Εμπορευμάτων (EOQ)")

    q = st.number_input("Αρχική τιμή Q (ποσότητα παραγγελίας)", value=30, step=1)
    M = st.number_input("Ανάγκες μιας περιόδου M (συνολική ζήτηση)", value=10000, step=1)
    kf = st.number_input("Σταθερό κόστος προμηθειών ανά παραγγελία kf", value=600.0, step=10.0, format="%.2f")
    r = st.number_input("Ποσοστιαία έκπτωση % r", value=0.0, step=0.01, format="%.4f") / 100
    insurance = st.number_input("Ασφάλιστρα για την περίοδο ανά μήνα", value=150.0, step=10.0, format="%.2f")
    annual_interest = st.number_input("Ετήσιο επιτόκιο", value=0.05, step=0.001, format="%.4f")
    period_months = st.number_input("Υπολογιζόμενη περίοδος (μήνες)", value=12, step=1)
    monthly_maintenance = st.number_input("Μηνιαία έξοδα συντήρησης (π.χ. ενοίκιο, βάψιμο κλπ)", value=600.0, step=10.0, format="%.2f")

    # Υπολογισμοί
    total_procurement_cost = kf + insurance
    fixed_procurement_cost_per_period = (M / q) * kf if q != 0 else 0
    merchandise_cost_for_period = q * M
    storage_and_interest_cost = (kf + insurance) * period_months
    monthly_interest_rate = annual_interest / 12
    storage_cost_percentage = (monthly_maintenance / period_months) + ((kf * annual_interest) / period_months)
    maintenance_expense_for_period = monthly_maintenance * period_months

    if r == 0:
        EOQ = math.sqrt((2 * M * kf) / (M * (kf + insurance))) if M * (kf + insurance) != 0 else 0
    else:
        EOQ = math.sqrt((2 * M * kf) / (M * (insurance + (1 - r) * kf))) if M * (insurance + (1 - r) * kf) != 0 else 0

    num_orders = M / EOQ if EOQ != 0 else 0

    st.subheader("Αποτελέσματα")
    st.write(f"Συνολικό κόστος προμηθειών μίας περιόδου (Κ): {total_procurement_cost:.2f}")
    st.write(f"Σταθερό κόστος προμηθειών μίας περιόδου (KF): {fixed_procurement_cost_per_period:.2f}")
    st.write(f"Κόστος εμπορεύματος για την κάλυψη αναγκών μίας περιόδου (KV): {merchandise_cost_for_period:.2f}")
    st.write(f"Κόστος αποθήκευσης και τόκων (KL): {storage_and_interest_cost:.2f}")
    st.write(f"Τόκος σε % (i): {monthly_interest_rate:.4f}")
    st.write(f"Κόστος αποθήκευσης σε % (j): {storage_cost_percentage:.4f}")
    st.write(f"Έξοδα συντήρησης αποθηκευτικού χώρου στο σύνολο της περιόδου: {maintenance_expense_for_period:.2f}")
    st.write(f"Βέλτιστη ποσότητα προμήθειας (B): {EOQ:.2f}")
    st.write(f"Αριθμός παραγγελιών περιόδου: {num_orders:.2f}")
