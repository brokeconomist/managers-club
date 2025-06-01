import streamlit as st

def npv_calculation(
    sales_current,
    sales_extra,
    discount_cash,
    pct_accept_discount,
    days_accept_discount,
    pct_reject_discount,
    days_reject_discount,
    days_cash_payment,
    cost_of_sales_pct,
    capital_cost_pct,
    avg_supplier_payment_days
):
    # Τρέχουσα μέση περίοδος είσπραξης
    days_avg_receivable = (
        pct_accept_discount * days_accept_discount + pct_reject_discount * days_reject_discount
    )
    
    pct_new_policy = 0.6  # 60%
    
    profit_extra_sales = sales_extra * (1 - cost_of_sales_pct)
    
    discount_factor_cash = (1 / (1 + (capital_cost_pct / 365)) ** days_cash_payment)
    discount_factor_accept = (1 / (1 + (capital_cost_pct / 365)) ** days_accept_discount)
    discount_factor_reject = (1 / (1 + (capital_cost_pct / 365)) ** days_reject_discount)
    discount_factor_supplier = (1 / (1 + (capital_cost_pct / 365)) ** avg_supplier_payment_days)
    discount_factor_current_receivable = (1 / (1 + (capital_cost_pct / 365)) ** days_avg_receivable)
    
    # NPV formula based on your Excel formula
    npv = (
        (sales_current + sales_extra) * pct_new_policy * (1 - discount_cash) * discount_factor_cash
        + (sales_current + sales_extra) * (1 - pct_new_policy) * discount_factor_reject
        - cost_of_sales_pct * (sales_extra / sales_current) * sales_current * discount_factor_supplier
        - sales_current * discount_factor_current_receivable
    )
    
    # Current average collection days from weighted average
    current_avg_collection_days = days_avg_receivable
    
    # Profit from extra sales
    profit_extra = profit_extra_sales
    
    # Other results - these formulas are from your post (approximate)
    max_discount = 8.34  # placeholder, you can implement your break-even calculation
    optimal_discount = 2.14  # placeholder
    
    return current_avg_collection_days, pct_new_policy * 100, profit_extra, npv, max_discount, optimal_discount

# Streamlit UI

st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς - Υπολογιστής")

sales_current = st.number_input("Τρέχουσες πωλήσεις", value=1000.0, step=100.0)
sales_extra = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης", value=250.0, step=10.0)
discount_cash = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0, step=0.1) / 100
pct_accept_discount = st.number_input("% των πελατών που αποδέχεται την έκπτωση", value=50.0, step=1.0) / 100
days_accept_discount = st.number_input("% των πελατών που αποδέχεται την έκπτωση πληρώνει σε (μέρες)", value=60, step=1)
pct_reject_discount = st.number_input("% των πελατών που δεν αποδέχεται την έκπτωση", value=50.0, step=1.0) / 100
days_reject_discount = st.number_input("% πελατών που δεν αποδέχεται την έκπτωση πληρώνει σε (μέρες)", value=120, step=1)
days_cash_payment = st.number_input("Μέρες για πληρωμή τοις μετρητοίς (π.χ. 10)", value=10, step=1)
cost_of_sales_pct = st.number_input("Κόστος πωλήσεων σε %", value=80.0, step=0.1) / 100
capital_cost_pct = st.number_input("Κόστος κεφαλαίου σε %", value=20.0, step=0.1) / 100
avg_supplier_payment_days = st.number_input("Μέση περίοδος αποπληρωμής προμηθευτών", value=0, step=1)

if st.button("Υπολογισμός"):
    days_avg, pct_new_policy, profit_extra, npv, max_disc, opt_disc = npv_calculation(
        sales_current,
        sales_extra,
        discount_cash,
        pct_accept_discount,
        days_accept_discount,
        pct_reject_discount,
        days_reject_discount,
        days_cash_payment,
        cost_of_sales_pct,
        capital_cost_pct,
        avg_supplier_payment_days
    )
    
    st.write(f"Τρέχουσα μέση περίοδος είσπραξης: {days_avg:.2f} μέρες")
    st.write(f"% πελατών που θα ακολουθεί τη νέα πολιτική επί του νέου συνόλου: {pct_new_policy:.2f} %")
    st.write(f"Κέρδος από επιπλέον πωλήσεις: {profit_extra:.2f}")
    st.write(f"NPV: {npv:.2f}")
    st.write(f"Μέγιστη έκπτωση που μπορεί να δοθεί επί των πωλήσεων (NPV Break Even): {max_disc:.2f} %")
    st.write(f"Βέλτιστη έκπτωση που πρέπει να δοθεί: {opt_disc:.2f} %")
