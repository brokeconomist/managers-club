import streamlit as st

def show_gross_profit_template():
    st.title("📈 Ανάλυση Μικτού Κέρδους")

    st.subheader("🧾 Έσοδα Πωλήσεων")
    unit_price = st.number_input("Τιμή Μονάδας (€)", min_value=0.01, value=12.0)
    units_sold = st.number_input("Πωλούμενες Μονάδες", min_value=0.0, value=22500.0)
    returns = st.number_input("Επιστροφές (€)", min_value=0.0, value=1000.0)
    discounts = st.number_input("Εκπτώσεις (€)", min_value=0.0, value=2000.0)

    st.subheader("🏭 Κόστος Πωληθέντων")
    opening_inventory = st.number_input("Αρχικό Απόθεμα (€)", min_value=0.0, value=40000.0)
    purchases = st.number_input("Αγορές (€)", min_value=0.0, value=132000.0)
    closing_inventory = st.number_input("Τελικό Απόθεμα (€)", min_value=0.0, value=42000.0)
    direct_labor = st.number_input("Άμεσα Εργατικά (€)", min_value=0.0, value=10000.0)
    overheads = st.number_input("Γενικά Βιομηχανικά Έξοδα (€)", min_value=0.0, value=30000.0)
    depreciation = st.number_input("Αποσβέσεις (€)", min_value=0.0, value=20000.0)

    sales = unit_price * units_sold
    net_sales = sales - returns - discounts
    finished_goods = opening_inventory + purchases
    cost_of_goods_sold = (finished_goods - closing_inventory) + direct_labor + overheads + depreciation
    gross_profit = net_sales - cost_of_goods_sold
    gross_margin = gross_profit / net_sales if net_sales else 0

    st.markdown("---")
    st.subheader("📊 Αποτελέσματα")
    st.metric("Καθαρές Πωλήσεις", f"{net_sales:,.2f} €")
    st.metric("Κόστος Πωληθέντων", f"{cost_of_goods_sold:,.2f} €")
    st.metric("Μικτό Κέρδος", f"{gross_profit:,.2f} €")
    st.metric("Μικτό Κέρδος %", f"{gross_margin*100:.2f} %")

if __name__ == "__main__":
    show_gross_profit_template()
