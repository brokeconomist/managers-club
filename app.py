import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Managers' Club", page_icon="📊", layout="centered")

# Sidebar για επιλογή σελίδας
page = st.sidebar.selectbox("Μετάβαση σε:", ["🏠 Αρχική", "📊 Break-Even Υπολογιστής"])

if page == "🏠 Αρχική":
    st.title("📊 Managers’ Club")
    st.subheader("Ο οικονομικός βοηθός κάθε μικρομεσαίας επιχείρησης.")

    st.markdown("""
    Καλώς ήρθες!

    Το **Managers’ Club** είναι μια online εφαρμογή που σε βοηθά να παίρνεις οικονομικές αποφάσεις **χωρίς να χρειάζεται να είσαι λογιστής**.

    ### Τι μπορείς να κάνεις:
    - ✅ Υπολογίσεις break-even και ανάλυση κόστους
    - ✅ Πλάνο πληρωμών & εισπράξεων
    - ✅ Υποστήριξη τιμολόγησης και πιστωτικής πολιτικής

    ---
    🧮 Εδώ, τα οικονομικά μιλάνε απλά.  
    Δεν αντικαθιστούμε τους συμβούλους σου – **τους διευκολύνουμε**.
    """)

elif page == "📊 Break-Even Υπολογιστής":
    st.title("📊 Υπολογιστής Νεκρού Σημείου (Break-Even)")
    st.markdown("**Βρες το σημείο στο οποίο η επιχείρησή σου δεν έχει ούτε κέρδος ούτε ζημιά.**")

    # Εισαγωγή δεδομένων από τον χρήστη
    price_per_unit = st.number_input("Τιμή πώλησης ανά μονάδα (€)", value=1000.0, min_value=0.0)
    variable_cost = st.number_input("Μεταβλητό κόστος ανά μονάδα (€)", value=720.0, min_value=0.0)
    fixed_costs = st.number_input("Σταθερά κόστη (€)", value=261000.0, min_value=0.0)

    # Υπολογισμοί
    if price_per_unit > variable_cost:
        contribution_margin = price_per_unit - variable_cost
        break_even_units = fixed_costs / contribution_margin
        break_even_revenue = break_even_units * price_per_unit

        st.success(f"🔹 Νεκρό Σημείο σε Μονάδες: **{break_even_units:.2f}**")
        st.success(f"🔹 Νεκρό Σημείο σε Πωλήσεις (€): **{break_even_revenue:,.2f}**")

        # Διάγραμμα
        st.subheader("📈 Διάγραμμα Εσόδων & Κόστους")
        units = list(range(0, int(break_even_units * 2)))
        revenue = [price_per_unit * u for u in units]
        total_cost = [fixed_costs + variable_cost * u for u in units]

        fig, ax = plt.subplots()
        ax.plot(units, revenue, label="Έσοδα")
        ax.plot(units, total_cost, label="Συνολικό Κόστος")
        ax.axvline(break_even_units, color="red", linestyle="--", label="Νεκρό Σημείο")
        ax.set_xlabel("Μονάδες Πώλησης")
        ax.set_ylabel("€")
        ax.set_title("Break-Even Analysis")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Η τιμή πώλησης πρέπει να είναι μεγαλύτερη από το μεταβλητό κόστος.")

""")
