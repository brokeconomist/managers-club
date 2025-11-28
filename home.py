# home.py
import streamlit as st

def show_home():
    st.title("🎯 Καλωσόρισες στο Managers’ Club!")
    st.subheader("Το έξυπνο εργαλείο για σύγχρονες και τεκμηριωμένες οικονομικές αποφάσεις")

    st.markdown("""
    Το **Managers’ Club** είναι μια διαδικτυακή πλατφόρμα που σου δίνει τη δυνατότητα να κάνεις
    πιο γρήγορα, ξεκάθαρα και τεκμηριωμένα οικονομικές επιλογές για την επιχείρησή σου.

    Δεν χρειάζεσαι πολύπλοκα φύλλα Excel, όλα τα εργαλεία είναι **στη διάθεσή σου με ελληνικό περιβάλλον και απλές ερωτήσεις**.

    ---
    """)

    st.markdown("## 📌 Τι μπορείς να κάνεις εδώ:")

    # Λίστα εργαλείων: (Label for user, page_file_name)
    tools = [
        ("Υπολογισμός Νεκρού Σημείου (Break-Even)", "01_Break-Even"),
        ("Μεταβολή Νεκρού Σημείου (Τιμή / Κόστος / Επένδυση)", "02_Break-Even-Shift"),
        ("Αξία Πελάτη (Customer Lifetime Value)", "03_CLV"),
        ("Ανάλυση Υποκατάστασης Προϊόντων", "04_Substitution"),
        ("Ανάλυση Συμπληρωματικών Προϊόντων", "05_Complementary"),
        ("Όριο Απώλειας Πωλήσεων", "06_LossThreshold"),
        ("Ανάλυση Αύξησης Πίστωσης", "07_CreditExtension"),
        ("Ανάλυση Πολιτικής Πίστωσης", "08_CreditPolicy"),
        ("Ανάλυση Έκπτωσης Πληρωμής Προμηθευτών", "09_SupplierCredit"),
        ("Μέσος Ταμειακός Κύκλος", "10_CashCycle"),
        ("Δάνειο vs Leasing", "11_LoanVsLeasing"),
        ("Υπολογισμός Μικτού Κέρδους", "12_GrossProfit"),
        ("EOQ - Οικονομικότερη Παραγγελία", "13_EOQ"),
        ("Μέσο Κόστος Παραγωγής ανά Μονάδα", "14_UnitCost"),
        ("NPV για έκπτωση τοις μετρητοίς", "15_DiscountNPV"),
        ("Ημέρες Πίστωσης (μεσοσταθμικά)", "16_CreditDays"),
        ("Ταχύτητα Κυκλοφορίας Αποθεμάτων", "17_InventoryTurnover"),
    ]

    for label, page_name in tools:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"**{label}**")
        with c2:
            # Κάθε κουμπί κάνει switch στην αντίστοιχη σελίδα (multipage)
            if st.button("Άνοιγμα", key=f"home_btn_{page_name}"):
                try:
                    # Αυτό δουλεύει μόνο σε multipage deployment
                    st.switch_page(page_name)
                except Exception:
                    # Fallback: εμφανίζουμε μήνυμα αν switch_page δεν υποστηρίζεται
                    st.error("Η πλοήγηση αυτόματα δεν υποστηρίζεται στην τρέχουσα έκδοση. Χρησιμοποίησε το sidebar για να επιλέξεις το εργαλείο.")
