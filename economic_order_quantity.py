import streamlit as st
import math

def format_number_gr(num, decimals=0):
    formatted = f"{num:,.{decimals}f}"
    formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
    return formatted

def format_percentage_gr(num):
    perc = f"{num * 100:.2f}"
    return perc.replace('.', ',') + '%'

def show_economic_order_quantity():
    st.title("Οικονομικότερη Παραγγελία Εμπορευμάτων (EOQ)")

    q = st.number_input("Αρχική τιμή q (τιμή μονάδας)", value=30, step=1)
    M = st.number_input("Ανάγκες μιας περιόδου M", value=10000, step=1)
    kf = st.number_input("Σταθερό κόστος προμηθειών ανά παραγγελία kf", value=600.0, format="%.2f")
    r = st.number_input("Ποσοστιαία έκπτωση % r", value=0.0, format="%.2f") / 100
    insurance_per_month = st.number_input("Ασφάλιστρα ανά μήνα", value=150.0, format="%.2f")
    annual_interest = st.number_input("Ετήσιο επιτόκιο", value=0.05, format="%.4f")
    period_months = st.number_input("Υπολογιζόμενη περίοδος (μήνες)", value=12, step=1)
    monthly_maintenance = st.number_input("Μηνιαία έξοδα συντήρησης", value=600.0, format="%.2f")

    # Υπολογισμοί
    K = kf + insurance_per_month  # ΜΟΝΟ για μια παραγγελία
    KL = (insurance_per_month + monthly_maintenance) * period_months
    i = annual_interest
    j = (monthly_maintenance / period_months) + ((kf * annual_interest) / period_months)

    if r == 0:
        B = math.sqrt((2 * M * kf) / j)
    else:
        B = math.sqrt((2 * M * kf) / (insurance_per_month + (1 - r) * kf))

    num_orders = M / B if B != 0 else_
