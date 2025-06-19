import streamlit as st
import math

def format_number_gr(num, decimals=0):
    # Με κόμμα δεκαδικό και τελεία χιλιάδες (πχ 26.683,00)
    formatted = f"{num:,.{decimals}f}"
    # Αντικαθιστούμε: κόμμα-> προσωρινό, τελεία-> κόμμα, προσωρινό->τελεία
    formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
    return formatted

def format_percentage_gr(num):
    # num είναι δεκαδικός, πχ 0.05
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
    total_procurement_cost = kf + insurance
    fixed_procurement_cost_per_period = (M / q) * kf if q != 0 else 0
    merchandise_cost_for_period = q * M
    storage_and_interest_cost = (kf + insurance) * period_months
    monthly_interest_rate = annual_interest
    storage_cost_percentage = (monthly_maintenance / period_months) + ((kf * annual_interest) / period_months)
    maintenance_expense_for_period = monthly_maintenance * period_months

    denom = M * (kf + insurance) if r == 0 else M * (insurance + (1 - r) * kf)
    EOQ = math.sqrt((2 * M * kf) / denom) if denom != 0 else 0
    num_orders = M / EOQ if EOQ != 0 else 0

    st.subheader("Αποτελέσματα")
    st.write(f"**ΣΥΝΟΛΙΚΟ ΚΟΣΤΟΣ ΠΡΟΜΕΙΘΕΙΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ Κ:** {format_number_gr(total_procurement_cost,3)}")
    st.write(f"**ΣΤΑΘΕΡΟ ΚΟΣΤΟΣ ΠΡΟΜΕΙΘΕΙΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ ΚF:** {format_number_gr(fixed_procurement_cost_per_period,3)}")
    st.write(f"**ΚΟΣΤΟΣ ΕΜΠΟΡΕΥΜΑΤΟΣ ΓΙΑ ΤΗΝ ΚΑΛΥΨΗ ΑΝΓΚΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ KV:** {format_number_gr(merchandise_cost_for_period,0)}")
    st.write(f"**ΚΟΣΤΟΣ ΑΠΟΘΗΚΕΥΣΗΣ ΚΑΙ ΤΟΚΩΝ KL:** {format_number_gr(storage_and_interest_cost,0)}")
    st.write(f"**ΤΟΚΟΣ ΣΕ % i:** {format_percentage_gr(monthly_interest_rate)}")
    st.write(f"**ΚΟΣΤΟΣ ΑΠΟΘΗΚΕΥΣΗΣ ΣΕ % j:** {format_number_gr(storage_cost_percentage*100,2)}%")
    st.write(f"**ΕΞΟΔΑ ΣΥΝΤΗΡΗΣΗΣ ΑΠΟΘΗΚΕΥΤΙΚΟΥ ΧΩΡΟΥ ΣΤΟ ΣΥΝΟΛΟ ΤΗΣ ΠΕΡΙΟΔΟΥ:** {format_number_gr(maintenance_expense_for_period,0)}")
    st.write(f"**ΒΕΛΤΙΣΤΗ ΠΟΣΟΤΗΤΑ ΠΡΟΜΗΘΕΙΑΣ B:** {format_number_gr(EOQ,0)}")
    st.write(f"**ΑΡΙΘΜΟΣ ΠΑΡΑΓΓΕΛΙΩΝ ΠΕΡΙΟΔΟΥ:** {format_number_gr(num_orders,2)}")
