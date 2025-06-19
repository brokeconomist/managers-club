import streamlit as st
import math

def format_number_gr(num, decimals=0):
    formatted = f"{num:,.{decimals}f}"
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted

def format_percentage_gr(num):
    return f"{num * 100:.2f}".replace(".", ",") + "%"

def show_economic_order_quantity():
    st.title("📦 Οικονομικότερη Παραγγελία Εμπορευμάτων (EOQ)")

    # Εισαγωγή δεδομένων
    q = st.number_input("Αρχική Τιμή (q)", value=30.0, format="%.2f")
    M = st.number_input("Ανάγκες μιας Περιόδου (M)", value=10000, step=100)
    kf = st.number_input("Σταθερό Κόστος Προμηθειών ανά Παραγγελία (kf)", value=600.0, format="%.2f")
    r = st.number_input("Ποσοστιαία Έκπτωση (%)", value=0.0, format="%.2f") / 100
    insurance_monthly = st.number_input("Ασφάλιστρα ανά Μήνα", value=150.0, format="%.2f")
    annual_interest = st.number_input("Ετήσιο Επιτόκιο", value=0.05, format="%.4f")
    months = st.number_input("Υπολογιζόμενη Περίοδος (Μήνες)", value=12, step=1)
    maintenance_monthly = st.number_input("Μηνιαία Έξοδα Συντήρησης", value=600.0, format="%.2f")

    # Υπολογισμοί
    KV = M * q
    KL = (insurance_monthly + maintenance_monthly) * months
    i = annual_interest
    j = (KL / KV) + i

    if r == 0:
        B = math.sqrt((2 * M * kf) / (q * j))
    else:
        B = math.sqrt((2 * M * kf) / (maintenance_monthly + (1 - r) * kf))

    orders = M / B if B != 0 else 0
    KF = orders * kf
    K = KF + KL
    maintenance_total = maintenance_monthly * months

    # Εμφάνιση αποτελεσμάτων
    st.subheader("📊 Αποτελέσματα")
    st.write(f"**ΣΥΝΟΛΙΚΟ ΚΟΣΤΟΣ ΠΡΟΜΗΘΕΙΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ (Κ):** {format_number_gr(K, 0)}")
    st.write(f"**ΣΤΑΘΕΡΟ ΚΟΣΤΟΣ ΠΡΟΜΗΘΕΙΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ (ΚF):** {format_number_gr(KF, 0)}")
    st.write(f"**ΚΟΣΤΟΣ ΕΜΠΟΡΕΥΜΑΤΟΣ ΓΙΑ ΤΗΝ ΚΑΛΥΨΗ ΑΝΑΓΚΩΝ (KV):** {format_number_gr(KV, 0)}")
    st.write(f"**ΚΟΣΤΟΣ ΑΠΟΘΗΚΕΥΣΗΣ ΚΑΙ ΤΟΚΩΝ (KL):** {format_number_gr(KL, 0)}")
    st.write(f"**ΤΟΚΟΣ ΣΕ % (i):** {format_percentage_gr(i)}")
    st.write(f"**ΚΟΣΤΟΣ ΑΠΟΘΗΚΕΥΣΗΣ ΣΕ % (j):** {format_percentage_gr(j)}")
    st.write(f"**ΕΞΟΔΑ ΣΥΝΤΗΡΗΣΗΣ ΑΠΟΘΗΚΕΥΤΙΚΟΥ ΧΩΡΟΥ:** {format_number_gr(maintenance_total, 0)}")
    st.write(f"**ΒΕΛΤΙΣΤΗ ΠΟΣΟΤΗΤΑ ΠΡΟΜΗΘΕΙΑΣ (B):** {format_number_gr(B, 0)}")
    st.write(f"**ΑΡΙΘΜΟΣ ΠΑΡΑΓΓΕΛΙΩΝ ΠΕΡΙΟΔΟΥ:** {format_number_gr(orders, 2)}")
