import streamlit as st

st.set_page_config(page_title="Break-Even Tool", layout="centered")

st.title("🔍 Break-Even Υπολογιστής")

# Εισαγωγή δεδομένων
fixed_costs = st.number_input("Σταθερά Κόστη (€)", min_value=0.0, value=1000.0, step=100.0)
price_per_unit = st.number_input("Τιμή Πώλησης ανά Μονάδα (€)", min_value=0.01, value=10.0, step=0.5)
variable_cost_per_unit = st.number_input("Μεταβλητό Κόστος ανά Μονάδα (€)", min_value=0.0, value=5.0, step=0.5)

# Υπολογισμός
if price_per_unit > variable_cost_per_unit:
    break_even_units = fixed_costs / (price_per_unit - variable_cost_per_unit)
    st.success(f"📈 Break-Even Point: {break_even_units:.0f} μονάδες")
else:
    st.error("Η Τιμή Πώλησης πρέπει να είναι μεγαλύτερη από το Μεταβλητό Κόστος.")

# Γράφημα (προαιρετικά)
import matplotlib.pyplot as plt

units = list(range(0, int(break_even_units * 2) + 10, 10))
revenues = [price_per_unit * x for x in units]
costs = [fixed_costs + variable_cost_per_unit * x for x in units]

fig, ax = plt.subplots()
ax.plot(units, revenues, label="Έσοδα", color="green")
ax.plot(units, costs, label="Κόστη", color="red")
ax.axvline(break_even_units, linestyle="--", color="blue", label="Break-Even")
ax.set_xlabel("Ποσότητα")
ax.set_ylabel("€")
ax.set_title("Break-Even Ανάλυση")
ax.legend()
st.pyplot(fig)
