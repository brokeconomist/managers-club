import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# ΥΠΟΛΟΓΙΣΤΙΚΗ ΣΥΝΑΡΤΗΣΗ
# -----------------------------
def calculate_cash_discount(
    current_sales,
    extra_sales,
    gross_margin,
    discount_rate,
    accept_rate,
    days_accept,
    days_non_accept,
    current_collection_days,
    wacc
):
    new_sales = current_sales + extra_sales
    decline_rate = 1 - accept_rate

    # Νέα μέση περίοδος είσπραξης
    new_collection_days = accept_rate * days_accept + decline_rate * days_non_accept

    # Υπολογισμός απαιτήσεων
    old_receivables = (current_collection_days / 365) * current_sales
    new_receivables = (new_collection_days / 365) * new_sales
    capital_release = old_receivables - new_receivables

    # Κέρδος από νέες πωλήσεις
    profit_from_sales = extra_sales * gross_margin

    # Κόστος έκπτωσης
    discount_cost = new_sales * discount_rate * accept_rate

    # Κέρδος αποδέσμευσης κεφαλαίου (τοκισμένο)
    capital_benefit = capital_release * wacc

    # Συνολικό κέρδος
    total_profit = profit_from_sales + capital_benefit - discount_cost

    return {
        "new_collection_days": new_collection_days,
        "old_receivables": old_receivables,
        "new_receivables": new_receivables,
        "capital_release": capital_release,
        "profit_from_sales": profit_from_sales,
        "discount_cost": discount_cost,
        "capital_benefit": capital_benefit,
        "total_profit": total_profit,
        "npv": total_profit
    }

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς", layout="centered")

st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

# Εισαγωγή παραμέτρων
st.subheader("Παράμετροι")

col1, col2 = st.columns(2)

with col1:
    current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", value=1000.0, step=100.0)
    extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", value=250.0, step=50.0)
    gross_margin = st.slider("Μικτό περιθώριο κέρδους (%)", 0.0, 100.0, value=20.0) / 100
    wacc = st.slider("Κόστος κεφαλαίου (WACC) (%)", 0.0, 50.0, value=20.0) / 100

with col2:
    accept_rate = st.slider("% πελατών που αποδέχεται την έκπτωση", 0.0, 100.0, value=60.0) / 100
    days_accept = st.number_input("Μέρες πληρωμής (με έκπτωση)", value=10)
    days_non_accept = st.number_input("Μέρες πληρωμής (χωρίς έκπτωση)", value=120)
    current_collection_days = st.number_input("Τρέχουσα μέση περίοδος είσπραξης (μέρες)", value=84)

# Υπολογισμοί για εύρος εκπτώσεων
discounts = np.linspace(0.0, 0.30, 301)
npvs = []
for d in discounts:
    res = calculate_cash_discount(
        current_sales=current_sales,
        extra_sales=extra_sales,
        gross_margin=gross_margin,
        discount_rate=d,
        accept_rate=accept_rate,
        days_accept=days_accept,
        days_non_accept=days_non_accept,
        current_collection_days=current_collection_days,
        wacc=wacc
    )
    npvs.append(res["npv"])

npvs = np.array(npvs)
optimal_idx = npvs.argmax()
optimal_discount = discounts[optimal_idx]
breakeven_idx = np.abs(npvs).argmin()
breakeven_discount = discounts[breakeven_idx]

# Αποτελέσματα
st.subheader("Αποτελέσματα")

st.markdown(f"✅ **Βέλτιστη έκπτωση**: **{optimal_discount:.2%}**")
st.markdown(f"🟡 **Έκπτωση break-even (NPV = 0)**: **{breakeven_discount:.2%}**")
st.markdown(f"📈 **Μέγιστο NPV**: **{npvs[optimal_idx]:.2f} €**")

# Γράφημα
st.subheader("Γράφημα NPV σε σχέση με την έκπτωση")

fig, ax = plt.subplots()
ax.plot(discounts * 100, npvs, label="NPV")
ax.axhline(0, color="gray", linestyle="--")
ax.axvline(optimal_discount * 100, color="green", linestyle="--", label="Βέλτιστη έκπτωση")
ax.axvline(breakeven_discount * 100, color="orange", linestyle="--", label="Break-even έκπτωση")
ax.set_xlabel("Έκπτωση (%)")
ax.set_ylabel("NPV (€)")
ax.set_title("NPV σε σχέση με την Έκπτωση Τοις Μετρητοίς")
ax.legend()
ax.grid(True)

st.pyplot(fig)
