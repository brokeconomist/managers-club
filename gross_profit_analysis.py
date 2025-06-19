import streamlit as st

def main():
    st.title("Έσοδα Πωλήσεων & Κόστος Πωληθέντων")

    st.header("Έσοδα Πωλήσεων")
    unit_price = st.number_input("Τιμή Μονάδας", value=12, step=1)
    units_sold = st.number_input("Πωλούμενες μονάδες", value=22500, step=100)
    sales = unit_price * units_sold
    returns = st.number_input("Επιστροφές (€)", value=1000)
    discounts = st.number_input("Εκπτώσεις (€)", value=2000)
    net_sales = sales - returns - discounts

    st.write(f"Πωλήσεις: {sales:,.2f} €")
    st.write(f"Καθαρές Πωλήσεις: {net_sales:,.2f} €")

    st.header("Κόστος Πωληθέντων")
    beginning_inventory = st.number_input("Αρχικό Απόθεμα (€)", value=40000)
    purchases = st.number_input("Αγορές (€)", value=132000)
    finished_goods = beginning_inventory + purchases
    ending_inventory = st.number_input("Τελικό Απόθεμα (€)", value=42000)
    direct_labor = st.number_input("Άμμεσα Εργατικά (€)", value=10000)
    factory_overhead = st.number_input("Γεν. Βιομηχανικά (€)", value=30000)
    depreciation = st.number_input("Αποσβέσεις (€)", value=20000)
    cogs = finished_goods - ending_inventory + direct_labor + factory_overhead + depreciation

    st.write(f"Έτοιμα Προϊόντα: {finished_goods:,.2f} €")
    st.write(f"Κόστος Πωληθέντων: {cogs:,.2f} €")

    gross_profit = net_sales - cogs
    gross_profit_percent = (gross_profit / net_sales) * 100 if net_sales else 0

    st.header("Μικτό Κέρδος")
    st.write(f"Μικτό Κέρδος: {gross_profit:,.2f} €")
    st.write(f"Μικτό Κέρδος %: {gross_profit_percent:.1f}%")

if __name__ == "__main__":
    main()
