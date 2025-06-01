import streamlit as st
import numpy as np

def format_number_gr(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(x):
    return f"{x*100:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")

def calculate(
    current_sales,
    cost_of_goods_sold,
    discount_rate,
    customers_accept_discount,
    days_pay_discount,
    days_pay_no_discount,
    additional_sales_pct,
    wacc,
    supplier_payment_days
):
    current_avg_collection_days = (
        days_pay_discount * customers_accept_discount +
        days_pay_no_discount * (1 - customers_accept_discount)
    )
    current_receivables = current_sales * current_avg_collection_days / 365

    additional_sales = current_sales * additional_sales_pct
    new_total_sales = current_sales + additional_sales

    pct_customers_new_policy = (
        (current_sales * customers_accept_discount + additional_sales) / new_total_sales
    )
    pct_customers_old_policy = 1 - pct_customers_new_policy

    new_avg_collection_days_after_increase = (
        pct_customers_new_policy * days_pay_discount +
        pct_customers_old_policy * days_pay_no_discount
    )
    receivables_after_sales_increase = new_total_sales * new_avg_collection_days_after_increase / 365

    capital_released_after_sales_increase = current_receivables - receivables_after_sales_increase

    margin_per_euro = 1 - (cost_of_goods_sold / current_sales) if current_sales != 0 else 0

    profit_additional_sales = additional_sales * margin_per_euro
    profit_from_capital_release = capital_released_after_sales_increase * wacc
    discount_cost = new_total_sales * pct_customers_new_policy * discount_rate
    total_profit = profit_additional_sales + profit_from_capital_release - discount_cost

    daily_wacc = (1 + wacc) ** (1/365) - 1

    npv = (
        new_total_sales * pct_customers_new_policy * (1 - discount_rate) * (1 / (1 + daily_wacc) ** days_pay_discount) +
        new_total_sales * pct_customers_old_policy * (1 / (1 + daily_wacc) ** days_pay_no_discount) -
        current_sales * (additional_sales / current_sales) * (1 / (1 + daily_wacc) ** supplier_payment_days) * discount_cost / discount_rate -
        current_sales * (1 / (1 + daily_wacc) ** supplier_payment_days)
    )

    A = (1 + daily_wacc) ** (days_pay_discount - days_pay_no_discount)
    B = (1 - (1 / pct_customers_new_policy)) if pct_customers_new_policy != 0 else 0
    C = (1 + daily_wacc) ** (days_pay_no_discount - supplier_payment_days)
    D = (additional_sales / current_sales)
    E = (1 + daily_wacc) ** (days_pay_no_discount - supplier_payment_days)
    F = pct_customers_new_policy * (1 + D)

    try:
        max_discount = 1 - (A * (B + (C + D * E) / F))
        max_discount = max(0.0, max_discount)
    except ZeroDivisionError:
        max_discount = 0.0

    optimal_discount = (1 - (1 + daily_wacc) ** (days_pay_discount - current_avg_collection_days)) / 2

    return {
        "current_avg_collection_days": current_avg_collection_days,
        "current_receivables": current_receivables,
        "additional_sales": additional_sales,
        "new_total_sales": new_total_sales,
        "pct_customers_new_policy": pct_customers_new_policy,
        "pct_customers_old_policy": pct_customers_old_policy,
        "new_avg_collection_days_after_increase": new_avg_collection_days_after_increase,
        "receivables_after_sales_increase": receivables_after_sales_increase,
        "capital_released_after_sales_increase": capital_released_after_sales_increase,
        "profit_additional_sales": profit_additional_sales,
        "profit_from_capital_release": profit_from_capital_release,
        "discount_cost": discount_cost,
        "total_profit": total_profit,
        "npv": npv,
        "max_discount": max_discount,
        "optimal_discount": optimal_discount,
    }

def show_discount_cash_tool():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    DEFAULTS = {
        "current_sales": 1000.0,
        "cost_of_goods_sold": 800.0,
        "discount_rate": 0.02,
        "customers_accept_discount": 0.4,
        "days_pay_discount": 10,
        "days_pay_no_discount": 30,
        "additional_sales_pct": 0.1,
        "wacc": 0.10,
        "supplier_payment_days": 30
    }

    with st.form("discount_form"):
        col1, col2 = st.columns(2)

        with col1:
            current_sales = st.number_input(
                "Τρέχουσες Πωλήσεις (€)",
                value=DEFAULTS["current_sales"], min_value=0.0, step=100.0, format="%.2f"
            )
            cost_of_goods_sold = st.number_input(
                "Κόστος Πωληθέντων (€)",
                value=DEFAULTS["cost_of_goods_sold"], min_value=0.0, max_value=current_sales, step=50.0, format="%.2f"
            )
            discount_rate = st.slider(
                "Έκπτωση (%)",
                0.0, 30.0, DEFAULTS["discount_rate"]*100, step=0.1
            ) / 100
            customers_accept_discount = st.slider(
                "% Πελατών που Αποδέχεται Έκπτωση",
                0, 100, int(DEFAULTS["customers_accept_discount"]*100), step=1
            ) / 100

        with col2:
            days_pay_discount = st.number_input(
                "Ημέρες Πληρωμής με Έκπτωση",
                value=DEFAULTS["days_pay_discount"], min_value=0, max_value=365, step=1
            )
            days_pay_no_discount = st.number_input(
                "Ημέρες Πληρωμής χωρίς Έκπτωση",
                value=DEFAULTS["days_pay_no_discount"], min_value=0, max_value=365, step=1
            )
            additional_sales_pct = st.slider(
                "Αύξηση Πωλήσεων λόγω Έκπτωσης (%)",
                0, 100, int(DEFAULTS["additional_sales_pct"]*100), step=1
            ) / 100
            wacc = st.slider(
                "WACC (%)",
                0.0, 50.0, DEFAULTS["wacc"]*100, step=0.01
            ) / 100
            supplier_payment_days = st.number_input(
                "Ημέρες Αποπληρωμής Προμηθευτών",
                value=DEFAULTS["supplier_payment_days"], min_value=0, max_value=365, step=1
            )

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        res = calculate(
            current_sales,
            cost_of_goods_sold,
            discount_rate,
            customers_accept_discount,
            days_pay_discount,
            days_pay_no_discount,
            additional_sales_pct,
            wacc,
            supplier_payment_days
        )

        st.subheader("Αποτελέσματα")
        col1, col2, col3 = st.columns(3)

        col1.metric("Κέρδος από Επιπλέον Πωλήσεις (€)", format_number_gr(res["profit_additional_sales"]))
        col1.metric("Κέρδος Αποδέσμευσης Κεφαλαίου (€)", format_number_gr(res["profit_from_capital_release"]))
        col1.metric("Κόστος Έκπτωσης (€)", format_number_gr(res["discount_cost"]))
        col2.metric("Συνολικό Καθαρό Κέρδος (€)", format_number_gr(res["total_profit"]))
        col2.metric("Καθαρό Κεφάλαιο Πελατών (ημ.)", f'{res["current_avg_collection_days"]:.1f}')
        col2.metric("Νέες Ημέρες Είσπραξης (ημ.)", f'{res["new_avg_collection_days_after_increase"]:.1f}')
        col3.metric("Κεφάλαιο σε Είσπραξη (πριν) (€)", format_number_gr(res["current_receivables"]))
        col3.metric("Κεφάλαιο σε Είσπραξη (μετά) (€)", format_number_gr(res["receivables_after_sales_increase"]))
        col3.metric("Αποδεσμευμένο Κεφάλαιο (€)", format_number_gr(res["capital_released_after_sales_increase"]))

        st.markdown(f"**Μέγιστη Επιτρεπτή Έκπτωση:** {format_percentage_gr(res['max_discount'])}")
