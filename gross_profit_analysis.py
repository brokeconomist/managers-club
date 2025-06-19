import streamlit as st

def format_gr_number(x):
    """Μορφοποίηση αριθμού με κόμμα ως δεκαδικό και τελεία ως χιλιάδες"""
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def show_gross_profit_template():
    st.header("Ανάλυση Μικτού Κέρδους")

    # Εισαγωγή δεδομένων
    τιμη_μοναδας = st.number_input("Τιμή Μονάδας (€)", value=12.00, min_value=0.0, step=0.01, format="%.2f")
    πωλουμενες_μοναδες = st.number_input("Πωλούμενες Μονάδες", value=22500, min_value=0, step=1)
    επιστροφες = st.number_input("Επιστροφές (€)", value=1000.00, min_value=0.0, step=0.01, format="%.2f")
    εκπτωσεις = st.number_input("Εκπτώσεις (€)", value=2000.00, min_value=0.0, step=0.01, format="%.2f")

    αρχικο_αποθεμα = st.number_input("Αρχικό Απόθεμα (€)", value=40000.00, min_value=0.0, step=0.01, format="%.2f")
    αγορες = st.number_input("Αγορές (€)", value=132000.00, min_value=0.0, step=0.01, format="%.2f")
    τελικο_αποθεμα = st.number_input("Τελικό Απόθεμα (€)", value=42000.00, min_value=0.0, step=0.01, format="%.2f")

    αμεσα_εργατικα = st.number_input("Άμεσα Εργατικά (€)", value=10000.00, min_value=0.0, step=0.01, format="%.2f")
    γεν_βιομηχανικα = st.number_input("Γενικά Βιομηχανικά (€)", value=30000.00, min_value=0.0, step=0.01, format="%.2f")
    αποσβεσεις = st.number_input("Αποσβέσεις (€)", value=20000.00, min_value=0.0, step=0.01, format="%.2f")

    # Υπολογισμοί
    καθαρές_πωλήσεις = τιμη_μοναδας * πωλουμενες_μοναδες - επιστροφες - εκπτωσεις
    κόστος_πωληθέντων = (αρχικο_αποθεμα + αγορες + αμεσα_εργατικα + γεν_βιομηχανικα + αποσβεσεις) - τελικο_αποθεμα
    μικτό_κέρδος = καθαρές_πωλήσεις - κόστος_πωληθέντων
    μικτό_κέρδος_ποσοστό = (μικτό_κέρδος / καθαρές_πωλήσεις * 100) if καθαρές_πωλήσεις != 0 else 0

    st.markdown("---")
    st.write(f"**Καθαρές Πωλήσεις:** € {format_gr_number(καθαρές_πωλήσεις)}")
    st.write(f"**Κόστος Πωληθέντων:** € {format_gr_number(κόστος_πωληθέντων)}")
    st.write(f"**Μικτό Κέρδος:** € {format_gr_number(μικτό_κέρδος)}")
    st.write(f"**Μικτό Κέρδος %:** {μικτό_κέρδος_ποσοστό:.2f}%")
