import streamlit as st

def format_currency(value, decimals=0):
    formatted = f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{formatted} €"

def format_percentage_gr(value, decimals=1):
    sign = "-" if value < 0 else ""
    abs_val = abs(value * 100)
    formatted = f"{abs_val:,.{decimals}f}".replace(",", "#").replace(".", ",").replace("#", ".")
    return f"{sign}{formatted}%"

def show_gross_profit_template():
    st.title("📈 Ανάλυση Μικτού Κέρδους")

    with st.form("gross_profit_form"):
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

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        sales = unit_price * units_sold
        net_sales = sales - returns - discounts
        finished_goods = opening_inventory + purchases
        cost_of_goods_sold = (finished_goods - closing_inventory) + direct_labor + overheads + depreciation
        gross_profit = net_sales - cost_of_goods_sold
        gross_margin = gross_profit / net_sales if net_sales else 0

        st.markdown("---")
        st.subheader("📊 Αποτελέσματα")
        st.metric("Καθαρές Πωλήσεις", format_currency(net_sales))
        st.metric("Κόστος Πωληθέντων", format_currency(cost_of_goods_sold))
        st.metric("Μικτό Κέρδος", format_currency(gross_profit))
        st.metric("Μικτό Κέρδος %", format_percentage_gr(gross_margin))

if __name__ == "__main__":
    show_gross_profit_template()
