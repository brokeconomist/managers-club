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
    annual_interest = st.number_input("Ετήσιο Επιτόκιο", value=0.05, format="%.4f")
    storage_cost_rate = st.number_input("Ποσοστό Κόστους Αποθήκευσης (%)", value=3.0, format="%.2f") / 100

    # Υπολογισμοί
    KV = M * q                              # Κόστος εμπορεύματος
    i = annual_interest                     # Τόκος
    j = i + storage_cost_rate               # Συνολικό ποσοστό κόστους αποθήκευσης
    KL = j * KV                             # Κόστος αποθήκευσης και τόκων

    if r == 0:
        B = math.sqrt((2 * M * kf) / (q * j)) if j != 0 else 0
    else:
        B = math.sqrt((2 * M * kf) / (storage_cost_rate + (1 - r) * kf))  # προσαρμοσμένο για έκπτωση

    orders = M / B if B != 0 else 0
    KF = orders * kf
    K = KF + KL

    # Εμφάνιση αποτελεσμάτων
    st.subheader("📊 Αποτελέσματα")
    st.write(f"**ΣΥΝΟΛΙΚΟ ΚΟΣΤΟΣ ΠΡΟΜΗΘΕΙΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ (Κ):** {format_number_gr(K, 0)}")
    st.write(f"**ΣΤΑΘΕΡΟ ΚΟΣΤΟΣ ΠΡΟΜΗΘΕΙΩΝ ΜΙΑΣ ΠΕΡΙΟΔΟΥ (ΚF):** {format_number_gr(KF, 0)}")
    st.write(f"**ΚΟΣΤΟΣ ΕΜΠΟΡΕΥΜΑΤΟΣ ΓΙΑ ΤΗΝ ΚΑΛΥΨΗ ΑΝΑΓΚΩΝ (KV):** {format_number_gr(KV, 0)}")
    st.write(f"**ΚΟΣΤΟΣ ΑΠΟΘΗΚΕΥΣΗΣ ΚΑΙ ΤΟΚΩΝ (KL):** {format_number_gr(KL, 0)}")
    st.write(f"**ΤΟΚΟΣ ΣΕ % (i):** {format_percentage_gr(i)}")
    st.write(f"**ΚΟΣΤΟΣ ΑΠΟΘΗΚΕΥΣΗΣ ΣΕ % (j):** {format_percentage_gr(j)}")
    st.write(f"**ΒΕΛΤΙΣΤΗ ΠΟΣΟΤΗΤΑ ΠΡΟΜΗΘΕΙΑΣ (B):** {format_number_gr(B, 0)}")
    st.write(f"**ΑΡΙΘΜΟΣ ΠΑΡΑΓΓΕΛΙΩΝ ΠΕΡΙΟΔΟΥ:** {format_number_gr(orders, 2)}")
