
import streamlit as st
from utils import parse_gr_number, format_number_gr, format_percentage_gr
import math

def calculate_discount_cashflow(
    current_sales,
    extra_sales,
    cash_discount_pct,
    discount_rate_annual,
    days_cash_payment,
    supplier_payment_days,
    cost_of_sales_pct
):
    discount_rate_daily = (1 + discount_rate_annual) ** (1 / 365) - 1

    total_sales = current_sales + extra_sales
    discounted_revenue = total_sales * (1 - cash_discount_pct)
    discounted_revenue_npv = discounted_revenue / ((1 + discount_rate_daily) ** days_cash_payment)
    cost_of_goods_npv = (cost_of_sales_pct * total_sales) / ((1 + discount_rate_daily) ** supplier_payment_days)

    npv = discounted_revenue_npv - cost_of_goods_npv
    discount_cost = extra_sales * cash_discount_pct

    return npv, discount_cost

def app():
    st.markdown("### Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")
    st.markdown(
        "Υπολογισμός της καθαρής παρούσας αξίας (NPV) από την εφαρμογή πολιτικής έκπτωσης τοις μετρητοίς "
        "σε όλες τις πωλήσεις από εδώ και στο εξής, και το κόστος της έκπτωσης που εφαρμόζεται μόνο στις νέες επιπλέον πωλήσεις."
    )

    col1, col2 = st.columns(2)
    with col1:
        current_sales = parse_gr_number(st.text_input("Τρέχουσες Πωλήσεις (€)", "100.000"))
        extra_sales = parse_gr_number(st.text_input("Πρόσθετες Πωλήσεις λόγω Έκπτωσης (€)", "20.000"))
        cash_discount_pct = parse_gr_number(st.text_input("Ποσοστό Έκπτωσης (%)", "2")) / 100
        cost_of_sales_pct = parse_gr_number(st.text_input("Κόστος Πωληθέντων (% επί των πωλήσεων)", "60")) / 100

    with col2:
        discount_rate_annual = parse_gr_number(st.text_input("Ετήσιο Επιτόκιο Προεξόφλησης (%)", "10")) / 100
        days_cash_payment = parse_gr_number(st.text_input("Ημέρες Είσπραξης με Έκπτωση", "10"))
        supplier_payment_days = parse_gr_number(st.text_input("Ημέρες Πληρωμής Προμηθευτών", "30"))

    if st.button("Υπολογισμός"):
        npv, discount_cost = calculate_discount_cashflow(
            current_sales,
            extra_sales,
            cash_discount_pct,
            discount_rate_annual,
            days_cash_payment,
            supplier_payment_days,
            cost_of_sales_pct
        )

        st.success("Αποτελέσματα")
        st.markdown(f"**Καθαρή Παρούσα Αξία (NPV):** {format_number_gr(npv)} €")
        st.markdown(f"**Κόστος Έκπτωσης (μόνο για τις επιπλέον πωλήσεις):** {format_number_gr(discount_cost)} €")

        if npv > discount_cost:
            st.markdown("✅ Η πολιτική έκπτωσης αποδίδει θετικά.")
        elif math.isclose(npv, discount_cost, rel_tol=1e-3):
            st.markdown("➖ Η πολιτική έκπτωσης βρίσκεται περίπου στο σημείο ισορροπίας (break-even).")
        else:
            st.markdown("⚠️ Η πολιτική έκπτωσης δεν είναι αποδοτική με τα παρόντα δεδομένα.")

if __name__ == "__main__":
    app()
