import streamlit as st
import math

def format_number_eu(num, decimals=3):
    # Μορφοποίηση: κόμμα ως χιλιάδες, τελεία δεκαδικά (πχ 26,683.123)
    return f"{num:,.{decimals}f}"

def format_percentage_eu(num):
    # num σε δεκαδικό πχ 0.05 -> 5,00%
    perc = f"{num*100:.2f}"
    return perc.replace('.', ',') + '%'

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
    # Σύνολο κόστους προμηθειών περιόδου (Κ) = kf + insurance (αντιλαμβάνομαι ότι είναι προσαρμοσμένο)
    total_procurement_cost = kf + insurance

    # Σταθερό κόστος προμηθειών μίας περιόδου (KF) = (M / q) * kf
    fixed_procurement_cost_per_period = (M / q) * kf if q != 0 else 0

    # Κόστος εμπορεύματος (KV) = q * M
    merchandise_cost_for_period = q * M

    # Κόστος αποθήκευσης και τόκων (KL) = (kf + insurance) * period_months (αναλογικό)
    storage_and_interest_cost = (kf + insurance) * period_months

    # Τόκος σε % i = annual_interest
    monthly_interest_rate = annual_interest

    # Κόστος αποθήκευσης σε % j = (monthly_maintenance / period_months) + ((kf * annual_interest) / period_months)
    storage_cost_percentage = (monthly_maintenance / period_months) + ((kf * annual_interest) / period_months)

    # Έξοδα συντήρησης αποθηκευτικού χώρου στο σύνολο περιόδου
    maintenance_expense_for_period = monthly_maintenance * period_months

    # Βέλτιστη ποσότητα προμήθειας (B)
    denom = M * (kf + insurance) if r == 0 else M * (insurance + (1 - r) * kf)
    EOQ = math.sqrt((2 * M * kf) / denom) if denom != 0 else 0

    # Αριθμός παραγγελιών περιόδου
    num_orders = M / EOQ if EOQ != 0 else 0

    # Εμφάνιση αποτελεσμάτων με σωστό format
    st.subheader("Αποτελέσματα")
    st.write(f"**ΣΥΝΟΛΙΚΟ ΚΟΣΤΟΣ ΠΡΟΜΕΙΘΕΙΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ Κ:** {format_number_eu(total_procurement_cost,3)}")
    st.write(f"**ΣΤΑΘΕΡΟ ΚΟΣΤΟΣ ΠΡΟΜΕΙΘΕΙΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ ΚF:** {format_number_eu(fixed_procurement_cost_per_period,3)}")
    st.write(f"**ΚΟΣΤΟΣ ΕΜΠΟΡΕΥΜΑΤΟΣ ΓΙΑ ΤΗΝ ΚΑΛΥΨΗ ΑΝΓΚΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ KV:** {format_number_eu(merchandise_cost_for_period,0)}")
    st.write(f"**ΚΟΣΤΟΣ ΑΠΟΘΗΚΕΥΣΗΣ ΚΑΙ ΤΟΚΩΝ KL:** {format_number_eu(storage_and_interest_cost,0)}")
    st.write(f"**ΤΟΚΟΣ ΣΕ % i:** {format_percentage_eu(monthly_interest_rate)}")
    st.write(f"**ΚΟΣΤΟΣ ΑΠΟΘΗΚΕΥΣΗΣ ΣΕ % j:** {format_number_eu(storage_cost_percentage*100,2)}%")
    st.write(f"**ΕΞΟΔΑ ΣΥΝΤΗΡΗΣΗΣ ΑΠΟΘΗΚΕΥΤΙΚΟΥ ΧΩΡΟΥ ΣΤΟ ΣΥΝΟΛΟ ΤΗΣ ΠΕΡΙΟΔΟΥ:** {format_number_eu(maintenance_expense_for_period,0)}")
    st.write(f"**ΒΕΛΤΙΣΤΗ ΠΟΣΟΤΗΤΑ ΠΡΟΜΗΘΕΙΑΣ B:** {format_number_eu(EOQ,0)}")
    st.write(f"**ΑΡΙΘΜΟΣ ΠΑΡΑΓΓΕΛΙΩΝ ΠΕΡΙΟΔΟΥ:** {format_number_eu(num_orders,2)}")
