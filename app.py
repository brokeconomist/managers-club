import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Managers' Club", layout="centered")

# Sidebar navigation
st.sidebar.title("🔧 Εργαλεία Ανάλυσης")
tool = st.sidebar.radio("Επιλέξτε εργαλείο:", [
    "🏠 Αρχική",
    "📊 Ανάλυση Νεκρού Σημείου",
    "🔁 Μεταβολή Νεκρού Σημείου (Τιμή/Κόστος/Επένδυση)",
    "👥 Ανάλυση CLV",
    "💸 Ανάλυση Μείωσης Τιμής Προϊόντος"
])

st.title("📈 Managers’ Club – Οικονομικά Εργαλεία")

# Tool 1: Αρχική
if tool == "🏠 Αρχική":
    st.markdown("""
    Καλώς ήρθατε στο **Managers’ Club**, την online εργαλειοθήκη για φοιτητές & μικρομεσαίους επιχειρηματίες.  
    Εδώ μπορείτε να αναλύσετε σημεία ισορροπίας, να προβλέψετε την αξία πελατών, να δείτε επιδράσεις μεταβολών τιμής & επενδύσεων, και άλλα πολλά.
    """)

# Tool 2: Βασική Ανάλυση Νεκρού Σημείου
elif tool == "📊 Ανάλυση Νεκρού Σημείου":
    st.subheader("📊 Υπολογισμός Νεκρού Σημείου")
    p = st.number_input("Τιμή Πώλησης ανά μονάδα (€)", min_value=0.01)
    vcu = st.number_input("Μεταβλητό Κόστος ανά μονάδα (€)", min_value=0.00)
    fc = st.number_input("Σταθερά Έξοδα (€)", min_value=0.00)

    if p > vcu:
        q_be = fc / (p - vcu)
        st.success(f"🔹 Νεκρό Σημείο: {q_be:.2f} μονάδες")
    elif p > 0:
        st.error("⚠️ Η τιμή πρέπει να είναι μεγαλύτερη από το μεταβλητό κόστος.")

# Tool 3: Νεκρό Σημείο με Επένδυση/Νέα Τιμή
elif tool == "🔁 Μεταβολή Νεκρού Σημείου (Τιμή/Κόστος/Επένδυση)":
    st.subheader("🔁 Ανάλυση Μεταβολής Νεκρού Σημείου")
    p = st.number_input("Αρχική Τιμή Πώλησης (€)", min_value=0.01)
    vcu = st.number_input("Αρχικό Μεταβλητό Κόστος (€)", min_value=0.00)
    fc = st.number_input("Αρχικά Σταθερά Έξοδα (€)", min_value=0.00)

    delta_fc = st.number_input("Επένδυση/Μεταβολή Σταθερών Εξόδων (€)", value=0.0)
    new_p = st.number_input("Νέα Τιμή Πώλησης (€)", value=p)
    new_vcu = st.number_input("Νέο Μεταβλητό Κόστος (€)", value=vcu)

    if new_p > new_vcu:
        old_be = fc / (p - vcu)
        new_be = (fc + delta_fc) / (new_p - new_vcu)
        diff = new_be - old_be
        st.info(f"🔹 Παλαιό Νεκρό Σημείο: {old_be:.2f}")
        st.success(f"🔹 Νέο Νεκρό Σημείο: {new_be:.2f}")
        st.write(f"🔄 Μεταβολή: {'Αύξηση' if diff > 0 else 'Μείωση'} {abs(diff):.2f} μονάδων")
    elif new_p > 0:
        st.error("⚠️ Η νέα τιμή πρέπει να είναι μεγαλύτερη από το νέο μεταβλητό κόστος.")

# Tool 4: Ανάλυση CLV
elif tool == "👥 Ανάλυση CLV":
    st.subheader("👥 Ανάλυση Customer Lifetime Value (CLV)")

    margin = st.number_input("Μέσο Κέρδος ανά Πελάτη ανά Περίοδο (€)", min_value=0.0)
    retention = st.slider("Πιθανότητα Διατήρησης Πελάτη (%)", min_value=0, max_value=100)
    discount_rate = st.slider("Επιτόκιο Έκπτωσης (%)", min_value=0, max_value=100)

    if retention < 100:
        r = retention / 100
        d = discount_rate / 100
        try:
            clv = margin * r / (1 + d - r)
            st.success(f"📈 Εκτιμώμενο CLV: {clv:.2f} €")
        except ZeroDivisionError:
            st.error("⚠️ Μη έγκυρος συνδυασμός r και d.")
    else:
        st.error("⚠️ Η πιθανότητα διατήρησης πρέπει να είναι < 100%.")

# Tool 5: Ανάλυση Μείωσης Τιμής
elif tool == "💸 Ανάλυση Μείωσης Τιμής Προϊόντος":
    st.subheader("💸 Ανάλυση Μείωσης Τιμής Προϊόντων")

    # Επιλογή προϊόντος
    product = st.selectbox("Επιλέξτε προϊόν:", ["Α", "Β", "Γ", "Δ"])
    
    price = st.number_input("Αρχική Τιμή Πώλησης (€)", min_value=0.01)
    discount_pct = st.slider("Ποσοστό Μείωσης Τιμής (%)", 0, 100, 10)
    new_price = price * (1 - discount_pct / 100)

    vcu = st.number_input("Μεταβλητό Κόστος (€)", min_value=0.00)
    fc = st.number_input("Σταθερά Έξοδα (€)", min_value=0.00)

    st.write(f"🔻 Νέα Τιμή μετά από {discount_pct}% μείωση: **{new_price:.2f} €**")

    if new_price > vcu:
        new_be = fc / (new_price - vcu)
        st.success(f"📍 Νέο Νεκρό Σημείο για το προϊόν {product}: {new_be:.2f} μονάδες")
    elif new_price > 0:
        st.error("⚠️ Η νέα τιμή πρέπει να είναι μεγαλύτερη από το μεταβλητό κόστος.")
