import streamlit as st

def turnover_quantity_based(avg_qty, sold_qty):
    if sold_qty == 0:
        return 0
    return round((avg_qty * 365) / sold_qty, 2)

def turnover_value_based(avg_value, cost_of_goods_sold):
    if cost_of_goods_sold == 0:
        return 0
    return round((avg_value * 365) / cost_of_goods_sold, 2)

def show_inventory_turnover_calculator():
    st.title("📦 Ταχύτητα Κυκλοφορίας Αποθεμάτων")
    st.write("Επίλεξε τρόπο υπολογισμού:")

    method = st.radio("Μέθοδος Υπολογισμού", ["📊 Με βάση ποσότητες", "💶 Με βάση αξίες"])

    num_items = st.number_input("Αριθμός ειδών εμπορευμάτων", min_value=1, max_value=10, value=4)

    product_names = []
    inputs1 = []
    inputs2 = []

    st.markdown("### Εισαγωγή Δεδομένων")
    for i in range(num_items):
        st.markdown(f"#### Εμπόρευμα {i+1}")
        name = st.text_input(f"Όνομα Εμπορεύματος {i+1}", key=f"name_{i}")

        if method == "📊 Με βάση ποσότητες":
            avg_inventory = st.number_input("Μ.Ο. Ποσότητα Αποθέματος", min_value=0.0, key=f"inv_qty_{i}")
            sold_quantity = st.number_input("Πωληθείσα Ποσότητα", min_value=0.0, key=f"sold_qty_{i}")
            inputs1.append((avg_inventory, sold_quantity))
        else:
            avg_inventory_value = st.number_input("Μ.Ο. Αξία Αποθέματος (€)", min_value=0.0, key=f"inv_val_{i}")
            cogs = st.number_input("Κόστος Πωληθέντων (€)", min_value=0.0, key=f"cogs_{i}")
            inputs2.append((avg_inventory_value, cogs))

        product_names.append(name)

    if st.button("📈 Υπολογισμός"):
        st.subheader("Αποτελέσματα")
        for i, name in enumerate(product_names):
            if method == "📊 Με βάση ποσότητες":
                avg_inv, sold = inputs1[i]
                result = turnover_quantity_based(avg_inv, sold)
                st.write(f"🛒 **{name}**: {result} ημέρες κυκλοφορίας (ποσότητες)")
            else:
                avg_val, cogs = inputs2[i]
                result = turnover_value_based(avg_val, cogs)
                st.write(f"💰 **{name}**: {result} ημέρες κυκλοφορίας (αξίες)")
