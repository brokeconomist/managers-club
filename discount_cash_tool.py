import streamlit as st
import numpy as np

def format_number_gr(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(x):
    return f"{x*100:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")

def calculate(
    current_sales,
    additional_sales,
    discount_rate,
    pct_accept_discount,
    days_pay_discount,
    pct_no_discount,
    days_pay_no_discount,
    days_pay_cash,
    cost_of_sales_pct,
    wacc,
    supplier_payment_days
):
    # Μέση τρέχουσα περίοδος είσπραξης (input)
    current_avg_collection_days = (
        days_pay_discount * pct_accept_discount + days_pay_no_discount * pct_no_discount
    )

    # Νέο σύνολο πωλήσεων
    new_total_sales = current_sales + additional_sales

    # Ποσοστό πελατών που ακολουθούν τη νέα πολιτική επί του νέου συνόλου
    pct_new_policy = (current_sales * pct_accept_discount + additional_sales) / new_total_sales
    pct_old_policy = 1 - pct_new_policy

    # Νέα μέση περίοδος είσπραξης μετά την αύξηση πωλήσεων
    new_avg_collection_days = (
        pct_new_policy * days_pay_discount + pct_old_policy * days_pay_no_discount
    )

    # Κέρδος από επιπλέον πωλήσεις (μικτό κέρδος = πωλήσεις * (1 - κόστος πωλήσεων %))
    margin_per_euro = 1 - cost_of_sales_pct
    profit_additional_sales = additional_sales * margin_per_euro

    # Υπολογισμός NPV απλοποιημένος
    daily_wacc = (1 + wacc) ** (1/365) - 1

    npv = (
        new_total_sales * pct_new_policy * (1 - discount_rate) / (1 + daily_wacc) ** days_pay_discount +
        new_total_sales * pct_old_policy / (1 + daily_wacc) ** days_pay_no_discount -
        current_sales / (1 + daily_wacc) ** supplier_payment_days
    )

    # Μέγιστη έκπτωση NPV break even (απλοποιημένος υπολογισμός)
    A = (1 + daily_wacc) ** (days_pay_discount - days_pay_no_discount)
    B = (1 - (1 / pct_new_policy)) if pct_new_policy != 0 else 0
    C = (1 + daily_wacc) ** (days_pay_no_discount - supplier_payment_days)
    try:
        max_discount = 1 - (A * (B + C))
        max_discount = max(0, max_discount)
    except:
        max_discount = 0

    # Βέλτιστη έκπτωση (προσέγγιση)
    optimal_discount = (1 - (1 + daily_wacc) ** (days_pay_discount - current_avg_collection_days)) / 2
    if optimal_discount < 0:
        optimal_discount = 0

    return {
        "current_avg_collection_days": current_avg_collection_days,
        "pct_new_policy": pct_new_policy,
        "profit_additional_sales": profit_additional_sales,
        "npv": npv,
        "max_discount": max_discount,
        "optimal_discount": optimal_discount
    }

def main():
    st.title("Υπολογισμός Αποδοτικότητας Έκπτωσης Τοις Μετρητοίς")

    # Inputs
    current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", value=1000.0, min_value=0.0, step=10.0, format="%.2f")
    additional_sales = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", value=250.0, min_value=0.0, step=10.0, format="%.2f")
    discount_rate = st.number_input("Έκπτωση για Πληρωμή Τοις Μετρητοίς (%)", value=2.0, min_value=0.0, max_value=100.0, step=0.1)/100
    pct_accept_discount = st.number_input("% Πελατών που Αποδέχονται Έκπτωση (%)", value=50.0, min_value=0.0, max_value=100.0, step=1.0)/100
    days_pay_discount = st.number_input("Μέρες Πληρωμής Πελατών με Έκπτωση", value=60, min_value=0, max_value=365, step=1)
    pct_no_discount = st.number_input("% Πελατών που ΔΕΝ Αποδέχονται Έκπτωση (%)", value=50.0, min_value=0.0, max_value=100.0, step=1.0)/100
    days_pay_no_discount = st.number_input("Μέρες Πληρωμής Πελατών χωρίς Έκπτωση", value=120, min_value=0, max_value=365, step=1)
    days_pay_cash = st.number_input("Μέρες για Πληρωμή Τοις Μετρητοίς (π.χ. 10 μέρες)", value=10, min_value=0, max_value=365, step=1)
    cost_of_sales_pct = st.number_input("Κόστος Πωλήσεων σε %", value=80.0, min_value=0.0, max_value=100.0, step=0.1)/100
    wacc = st.number_input("Κόστος Κεφαλαίου (WACC) σε %", value=20.0, min_value=0.0, max_value=100.0, step=0.1)/100
    supplier_payment_days = st.number_input("Μέση Περίοδος Αποπληρωμής Προμηθευτών (ημέρες)", value=0, min_value=0, max_value=365, step=1)

    if st.button("Υπολογισμός"):
        results = calculate(
            current_sales,
            additional_sales,
            discount_rate,
            pct_accept_discount,
            days_pay_discount,
            pct_no_discount,
            days_pay_no_discount,
            days_pay_cash,
            cost_of_sales_pct,
            wacc,
            supplier_payment_days
        )

        st.subheader("Αποτελέσματα Υπολογισμού")
        st.write(f"Τρέχουσα Μέση Περίοδος Είσπραξης (ημέρες): {results['current_avg_collection_days']:.1f}")
        st.write(f"% Πελατών που ακολουθούν τη νέα πολιτική: {results['pct_new_policy']*100:.1f} %")
        st.write(f"Κέρδος από Επιπλέον Πωλήσεις (€): {format_number_gr(results['profit_additional_sales'])}")
        st.write(f"NPV (€): {format_number_gr(results['npv'])}")
        st.write(f"Μέγιστη Έκπτωση που μπορεί να δοθεί (NPV Break Even): {format_percentage_gr(results['max_discount'])}")
        st.write(f"Βέλτιστη Έκπτωση που πρέπει να δοθεί: {format_percentage_gr(results['optimal_discount'])}")

if __name__ == "__main__":
    main()
