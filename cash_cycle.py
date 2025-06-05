import streamlit as st

def run_cash_cycle_app():
    st.title("📊 Υπολογιστής Ταμειακού Κύκλου")

    st.markdown("Συμπλήρωσε τις παρακάτω τιμές για να υπολογίσεις τον **συνολικό ταμειακό κύκλο** της επιχείρησης σου.")

    # Είσοδοι χρήστη
    col1, col2 = st.columns(2)

    with col1:
        raw_materials_days = st.number_input("📦 Ημέρες Αποθέματος Α’ Υλών", min_value=0, value=76, step=1)
        processing_days = st.number_input("🏭 Ημέρες Βιομηχανοποίησης", min_value=0, value=37, step=1)
        finished_goods_days = st.number_input("📦 Ημέρες Αποθέματος Ετοίμων", min_value=0, value=42, step=1)

    with col2:
        receivables_days = st.number_input("💰 Ημέρες Πίστωσης προς Πελάτες", min_value=0, value=73, step=1)
        payables_days = st.number_input("🧾 Ημέρες Πίστωσης από Προμηθευτές", min_value=0, value=61, step=1)

    # Υπολογισμός Ταμειακού Κύκλου
    cash_conversion_cycle = (
        raw_materials_days +
        processing_days +
        finished_goods_days +
        receivables_days -
        payables_days
    )

    # Αποτελέσματα
    st.markdown("---")
    st.subheader("🧮 Αποτελέσματα Υπολογισμού")

    st.metric(label="📆 Συνολικός Ταμειακός Κύκλος (ημέρες)", value=f"{cash_conversion_cycle} ημέρες")

    # Αξιολόγηση
    if cash_conversion_cycle > 150:
        st.warning("⚠️ Ο ταμειακός κύκλος είναι πολύ μεγάλος. Εξετάστε μείωση αποθεμάτων ή βελτίωση των όρων πίστωσης.")
    elif cash_conversion_cycle < 60:
        st.success("✅ Ο ταμειακός κύκλος είναι σύντομος και αποδοτικός.")
    else:
        st.info("ℹ️ Ο ταμειακός κύκλος βρίσκεται σε φυσιολογικά επίπεδα.")

    st.markdown("---")
    st.caption("🔧 Το εργαλείο βασίζεται σε κλασική ανάλυση χρηματοοικονομικής διοίκησης και ελέγχει το καθαρό διάστημα δεσμευμένων πόρων.")

