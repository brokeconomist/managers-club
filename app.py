import streamlit as st

# --- Sidebar μενού για επιλογή εργαλείου ---
st.sidebar.title("Εργαλεία Managers’ Club")
selected_tool = st.sidebar.radio("📌 Επιλέξτε εργαλείο:", [
    "Υπολογιστής Νεκρού Σημείου",
    "Ανάλυση Αλλαγής Νεκρού Σημείου",
    "Υπολογιστής Αξίας Πελάτη (CLV)",
    "Ανάλυση Υποκατάστασης Προϊόντων",
    "Ανάλυση Συμπληρωματικών Προϊόντων",
    "Όριο Απώλειας Πωλήσεων πριν Μείωση Τιμής"
])

# --- Εδώ πάει ο κώδικας κάθε εργαλείου ξεχωριστά ---
# Για το εργαλείο Νεκρού Σημείου:
if selected_tool == "Υπολογιστής Νεκρού Σημείου":
    st.title("Πόσο πρέπει να πουλήσω για να μη μπαίνω μέσα;")
    st.markdown("""
    Θέλετε να μάθετε **πόσα τεμάχια** ή **ποιο τζίρο** πρέπει να κάνετε για να καλύψετε τα έξοδά σας;

    👉 Αυτό το εργαλείο σάς δείχνει το **νεκρό σημείο** – δηλαδή εκεί που δεν έχετε ούτε κέρδος ούτε ζημιά.

    Ιδανικό για: νέες επιχειρήσεις, νέες τιμολογήσεις, ή όταν ζυγίζετε αν «σας βγαίνει» μια προσπάθεια.
    """)

    col1, col2 = st.columns(2)
    with col1:
        fixed_costs = st.number_input("Σταθερά κόστη (€)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
        price_per_unit = st.number_input("Τιμή πώλησης ανά τεμάχιο (€)", min_value=0.01, value=20.0, step=1.0, format="%.2f")
    with col2:
        variable_cost_per_unit = st.number_input("Μεταβλητό κόστος ανά τεμάχιο (€)", min_value=0.0, value=10.0, step=1.0, format="%.2f")

    if price_per_unit > variable_cost_per_unit:
        break_even_units = fixed_costs / (price_per_unit - variable_cost_per_unit)
        break_even_revenue = break_even_units * price_per_unit

        st.success("📊 Αποτελέσματα Νεκρού Σημείου")
        st.metric("🔢 Τεμάχια για κάλυψη κόστους", f"{break_even_units:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.metric("💶 Τζίρος για κάλυψη κόστους", f"{break_even_revenue:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
    else:
        st.error("❗ Η τιμή πώλησης πρέπει να είναι μεγαλύτερη από το μεταβλητό κόστος.")

# --- Εδώ θα συνεχίσεις και με τα υπόλοιπα εργαλεία όπως το CLV, Υποκατάσταση, κλπ ---
