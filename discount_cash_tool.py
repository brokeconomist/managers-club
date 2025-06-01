import streamlit as st
from discount_cash_chart import calculate_discount_cash
from utils import parse_gr_number, format_number_gr, format_percentage_gr

def show_discount_cash_calculator():
    st.header("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    with st.form("discount_cash_form"):
        col1, col2 = st.columns(2)
        with col1:
            current_sales = parse_gr_number(st.text_input("📦 Τρέχουσες πωλήσεις (€)", "1.000"))
            extra_sales = parse_gr_number(st.text_input("➕ Επιπλέον πωλήσεις λόγω πολιτικής (€)", "250"))
            cash_discount_rate = parse_gr_number(st.text_input("🏷️ Ποσοστό έκπτωσης (%)", "2")) / 100
            pct_customers_discount_total = parse_gr_number(
                st.text_input("👥 Ποσοστό όλων των πελατών που πληρώνουν μετρητοίς (%)", "60")
            ) / 100
            cost_of_sales_pct = parse_gr_number(st.text_input("⚙️ Κόστος πωληθέντων (%)", "80")) / 100

        with col2:
            days_accept = parse_gr_number(st.text_input("⏱️ Ημέρες είσπραξης για πληρωμή μετρητοίς", "10"))
            days_reject = parse_gr_number(st.text_input("⏳ Ημέρες είσπραξης χωρίς έκπτωση", "120"))
            cost_of_capital_annual = parse_gr_number(st.text_input("📉 Ετήσιο κόστος κεφαλαίου (%)", "20")) / 100
            avg_supplier_pay_days = parse_gr_number(st.text_input("🧾 Μέρες αποπληρωμής προμηθευτών", "0"))

        submitted = st.form_submit_button("📊 Υπολογισμός")

    if submitted:
        results = calculate_discount_cash(
            current_sales,
            extra_sales,
            cash_discount_rate,
            pct_customers_discount_total,
            days_accept,
            days_reject,
            cost_of_sales_pct,
            cost_of_capital_annual,
            avg_supplier_pay_days
        )

        st.subheader("📈 Αποτελέσματα")
        st.write("💶 **Καθαρή Παρούσα Αξία (NPV)**:", format_number_gr(results["NPV"]), "€")
        st.write("🔝 **Μέγιστο επιτρεπτό ποσοστό έκπτωσης**:", format_percentage_gr(results["Max Discount %"] / 100))
        st.write("✅ **Προτεινόμενο ποσοστό έκπτωσης (25% του max)**:", format_percentage_gr(results["Optimal Discount %"] / 100))

def calculate_discount_cash(
    current_sales,                  # Τρέχουσες πωλήσεις (€)
    extra_sales,                    # Επιπλέον πωλήσεις από την έκπτωση (€)
    cash_discount_rate,             # Ποσοστό έκπτωσης (π.χ. 0.02 για 2%)
    pct_customers_discount_total,   # Ποσοστό όλων των πελατών που δέχονται την έκπτωση (π.χ. 0.6)
    days_accept,                    # Ημέρες είσπραξης για πελάτες με έκπτωση (π.χ. 10)
    days_reject,                    # Ημέρες είσπραξης για πελάτες χωρίς έκπτωση (π.χ. 120)
    cost_of_sales_pct,              # Κόστος πωληθέντων ως ποσοστό (π.χ. 0.8)
    cost_of_capital_annual,         # Ετήσιο κόστος κεφαλαίου (π.χ. 0.2)
    avg_supplier_pay_days           # Μέρες αποπληρωμής προμηθευτών (π.χ. 0)
):
    total_sales = current_sales + extra_sales
    gross_profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)

    def discount_factor(days):
        return 1 / ((1 + cost_of_capital_annual) ** (days / 365))

    pv_discount_customers = total_sales * pct_customers_discount_total * (1 - cash_discount_rate) * discount_factor(days_accept)
    pv_other_customers = total_sales * (1 - pct_customers_discount_total) * discount_factor(days_reject)
    pv_cost_extra_sales = cost_of_sales_pct * extra_sales * discount_factor(avg_supplier_pay_days)

    old_avg_days = (0.5 * days_accept) + (0.5 * days_reject)
    pv_current_sales = current_sales * discount_factor(old_avg_days)

    npv = pv_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales

    max_discount = gross_profit_extra_sales / total_sales
    optimal_discount = max_discount * 0.25

    return {
        "NPV": round(npv, 2),
        "Max Discount %": round(max_discount * 100, 2),
        "Optimal Discount %": round(optimal_discount * 100, 2)
    }


