import streamlit as st

def calculate_discount_cash(
    current_sales,              
    extra_sales,                
    cash_discount_rate,         
    pct_customers_accept,       
    days_accept,                
    pct_customers_reject,       
    days_reject,                
    cash_payment_days,          
    cost_of_sales_pct,          
    cost_of_capital_annual,     
    avg_supplier_pay_days       
):
    current_avg_receivable_days = (pct_customers_accept * days_accept) + (pct_customers_reject * days_reject)
    pct_customers_new_policy = 0.6
    new_avg_receivable_days = (pct_customers_accept * days_accept) + (pct_customers_reject * days_reject)
    gross_profit_extra_sales = extra_sales * (1 - cost_of_sales_pct)
    def discount_factor(days):
        return 1 / ((1 + cost_of_capital_annual) ** (days / 365))
    pv_cash_discount_customers = (current_sales + extra_sales) * pct_customers_new_policy * (1 - cash_discount_rate) * discount_factor(cash_payment_days)
    pv_other_customers = (current_sales + extra_sales) * (1 - pct_customers_new_policy) * discount_factor(days_reject)
    pv_cost_extra_sales = cost_of_sales_pct * extra_sales * discount_factor(avg_supplier_pay_days)
    pv_current_sales = current_sales * discount_factor(current_avg_receivable_days)
    npv = pv_cash_discount_customers + pv_other_customers - pv_cost_extra_sales - pv_current_sales
    max_discount = gross_profit_extra_sales / (current_sales + extra_sales)
    optimal_discount = max_discount * 0.25
    npv_rounded = round(npv, 2)
    max_discount_pct = round(max_discount * 100, 2)
    optimal_discount_pct = round(optimal_discount * 100, 2)
    return {
        "NPV": npv_rounded,
        "Max Discount %": max_discount_pct,
        "Optimal Discount %": optimal_discount_pct
    }


def show_discount_cash_tool():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς 💰")

    # Inputs
    current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=1000.0, min_value=0.0, step=100.0)
    extra_sales = st.number_input("Επιπλέον Πωλήσεις (€)", value=250.0, min_value=0.0, step=50.0)
    cash_discount_rate = st.slider("Ποσοστό Έκπτωσης Πληρωμής με Μετρητά (%)", min_value=0.0, max_value=20.0, value=2.0, step=0.1) / 100
    pct_customers_accept = st.slider("Ποσοστό Πελατών που Αποδέχονται την Έκπτωση (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0) / 100
    days_accept = st.number_input("Μέσες Ημέρες Είσπραξης Πελατών που Αποδέχονται", value=60, min_value=0)
    pct_customers_reject = st.slider("Ποσοστό Πελατών που Απορρίπτουν την Έκπτωση (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0) / 100
    days_reject = st.number_input("Μέσες Ημέρες Είσπραξης Πελατών που Απορρίπτουν", value=120, min_value=0)
    cash_payment_days = st.number_input("Ημέρες Πληρωμής με Μετρητά", value=10, min_value=0)
    cost_of_sales_pct = st.slider("Κόστος Πωλήσεων ως Ποσοστό (%)", min_value=0.0, max_value=100.0, value=80.0, step=1.0) / 100
    cost_of_capital_annual = st.slider("Ετήσιο Κόστος Κεφαλαίου (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.1) / 100
    avg_supplier_pay_days = st.number_input("Μέσες Ημέρες Πληρωμής Προμηθευτών", value=0, min_value=0)

    if st.button("Υπολόγισε Αποτελέσματα"):
        results = calculate_discount_cash(
            current_sales,
            extra_sales,
            cash_discount_rate,
            pct_customers_accept,
            days_accept,
            pct_customers_reject,
            days_reject,
            cash_payment_days,
            cost_of_sales_pct,
            cost_of_capital_annual,
            avg_supplier_pay_days
        )

        st.subheader("Αποτελέσματα Υπολογισμού")
        st.write(f"**Καθαρή Παρούσα Αξία (NPV):** {results['NPV']} €")
        st.write(f"**Μέγιστο Ποσοστό Έκπτωσης:** {results['Max Discount %']} %")
        st.write(f"**Βέλτιστο Ποσοστό Έκπτωσης:** {results['Optimal Discount %']} %")
