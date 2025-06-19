import streamlit as st
import math

def format_number_gr(num, decimals=0):
    formatted = f"{num:,.{decimals}f}"
    formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
    return formatted

def format_percentage_gr(num):
    perc = f"{num*100:.2f}"
    return perc.replace('.', ',') + '%'

def show_economic_order_quantity():
    st.title("Οικονομικότερη Παραγγελία Εμπορευμάτων (EOQ)")

    M = st.number_input("Ανάγκες μιας περιόδου M (συνολική ζήτηση)", value=10000, step=1)
    kf = st.number_input("Σταθερό κόστος προμηθειών ανά παραγγελία kf", value=600.0, step=10.0, format="%.2f")
    insurance = st.number_input("Ασφάλιστρα για την περίοδο ανά μήνα", value=150.0, step=10.0, format="%.2f")
    annual_interest = st.number_input("Ετήσιο επιτόκιο", value=0.05, step=0.001, format="%.4f")
    period_months = st.number_input("Υπολογιζόμενη περίοδος (μήνες)", value=12, step=1)
    monthly_maintenance = st.number_input("Μηνιαία έξοδα συντήρησης (π.χ. ενοίκιο, βάψιμο κλπ)", value=600.0, step=10.0, format="%.2f")

    # Υπολογισμός συνολικού κόστους προμηθειών (Κ)
    total_procurement_cost = kf + insurance * period_months  # ασφάλιστρα * μήνες

    # Υπολογισμός κόστους αποθήκευσης σε %
    j = (monthly_maintenance / period_months) + ((kf * annual_interest) / period_months)

    # Βέλτιστη ποσότητα προμήθειας (B)
    EOQ = math.sqrt((2 * M * kf) / j)

    # Αριθμός παραγγελιών
    num_orders = M / EOQ

    # Άλλα κόστη που θες να εμφανίσεις:
    fixed_procurement_cost_per_period = (M / EOQ) * kf
    merchandise_cost_for_period = M * 30  # Υποθέτω τιμή μονάδας=30
    storage_and_interest_cost = (kf + insurance) * period_months
    maintenance_expense_for_period = monthly_maintenance * period_months

    st.subheader("Αποτελέσματα")
    st.write(f"**ΣΥΝΟΛΙΚΟ ΚΟΣΤΟΣ ΠΡΟΜΕΙΘΕΙΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ Κ:** {format_number_gr(total_procurement_cost,3)}")
    st.write(f"**ΣΤΑΘΕΡΟ ΚΟΣΤΟΣ ΠΡΟΜΕΙΘΕΙΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ ΚF:** {format_number_gr(fixed_procurement_cost_per_period,3)}")
    st.write(f"**ΚΟΣΤΟΣ ΕΜΠΟΡΕΥΜΑΤΟΣ ΓΙΑ ΤΗΝ ΚΑΛΥΨΗ ΑΝΓΚΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ KV:** {format_number_gr(merchandise_cost_for_period,0)}")
    st.write(f"**ΚΟΣΤΟΣ ΑΠΟΘΗΚΕΥΣΗΣ ΚΑΙ ΤΟΚΩΝ KL:** {format_number_gr(storage_and_interest_cost,0)}")
    st.write(f"**ΤΟΚΟΣ ΣΕ % i:** {format_percentage_gr(annual_interest)}")
    st.write(f"**ΚΟΣΤΟΣ ΑΠΟΘΗΚΕΥΣΗΣ ΣΕ % j:** {format_number_gr(j*100,2)}%")
    st.write(f"**ΕΞΟΔΑ ΣΥΝΤΗΡΗΣΗΣ ΑΠΟΘΗΚΕΥΤΙΚΟΥ ΧΩΡΟΥ ΣΤΟ ΣΥΝΟΛΟ ΤΗΣ ΠΕΡΙΟΔΟΥ:** {format_number_gr(maintenance_expense_for_period,0)}")
    st.write(f"**ΒΕΛΤΙΣΤΗ ΠΟΣΟΤΗΤΑ ΠΡΟΜΗΘΕΙΑΣ B:** {format_number_gr(EOQ,0)}")
    st.write(f"**ΑΡΙΘΜΟΣ ΠΑΡΑΓΓΕΛΙΩΝ ΠΕΡΙΟΔΟΥ:** {format_number_gr(num_orders,2)}")
