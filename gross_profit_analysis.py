import streamlit as st

def format_currency(value, decimals=0):
    try:
        formatted = f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{formatted} €"
    except:
        return f"{value} €"

def format_percentage_gr(value, decimals=1):
    try:
        sign = "-" if value < 0 else ""
        abs_val = abs(value * 100)
        formatted = f"{abs_val:,.{decimals}f}".replace(",", "#").replace(".", ",").replace("#", ".")
        return f"{sign}{formatted}%"
    except:
        return "-"

def show_gross_profit_template():
    st.title("📊 Ανάλυση Μικτού Κέρδους")

    st.subheader("🧾 Έσοδα Πωλήσεων")
    unit_price = 12
    units_sold = 22500
    sales = unit_price * units_sold
    returns = 1000
    discounts = 2000
    net_sales = sales - returns - discounts

    with st.container():
        st.write(f"**Τιμή Μονάδας**: {format_currency(unit_price, 0)}")
        st.write(f"**Πωλούμενες μονάδες**: {format_currency(units_sold, 0)}")
        st.write(f"**Πωλήσεις**: {format_currency(sales)}")
        st.write(f"**Επιστροφές**: {format_currency(returns)}")
        st.write(f"**Εκπτώσεις**: {format_currency(discounts)}")
        st.write(f"**Καθαρές Πωλήσεις**: ✅ **{format_currency(net_sales)}**")

    st.markdown("---")
    st.subheader("🏭 Κόστος Πωληθέντων")

    opening_inventory = 40000
    purchases = 132000
    finished_goods = 172000  # opening + purchases
    closing_inventory = 42000
    direct_labor = 10000
    overheads = 30000
    depreciation = 20000

    cost_of_goods_sold = (finished_goods - closing_inventory) + direct_labor + overheads + depreciation

    with st.container():
        st.write(f"**Αρχικό Απόθεμα**: {format_currency(opening_inventory)}")
        st.write(f"**Αγορές**: {format_currency(purchases)}")
        st.write(f"**Έτοιμα Προϊόντα**: {format_currency(finished_goods)}")
        st.write(f"**Τελικό Απόθεμα**: {format_currency(closing_inventory)}")
        st.write(f"**Άμεσα Εργατικά**: {format_currency(direct_labor)}")
        st.write(f"**Γενικά Βιομηχανικά Έξοδα**: {format_currency(overheads)}")
        st.write(f"**Αποσβέσεις**: {format_currency(depreciation)}")
        st.write(f"**Κόστος Πωληθέντων**: ✅ **{format_currency(cost_of_goods_sold)}**")

    st.markdown("---")
    st.subheader("💰 Μικτό Κέρδος")

    gross_profit = net_sales - cost_of_goods_sold
    gross_margin = gross_profit / net_sales if net_sales != 0 else 0

    st.metric("Μικτό Κέρδος", format_currency(gross_profit))
    st.metric("Μικτό Κέρδος %", format_percentage_gr(gross_margin))
