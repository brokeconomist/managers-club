import streamlit as st
import numpy as np
import plotly.graph_objects as go


def format_number_gr(x):
    """Μορφοποίηση αριθμών με ελληνικά δεκαδικά (κόμμα) και χιλιάδες (τελεία)."""
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(x):
    """Μορφοποίηση ποσοστών με ελληνικά δεκαδικά."""
    return f"{x*100:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")


def calculate(
    current_sales,                     # c2: τρέχουσες πωλήσεις (€)
    gross_margin,                     # c3: περιθώριο κέρδους (π.χ. 0.3 για 30%)
    discount_rate,                   # c5: έκπτωση τοις μετρητοίς (π.χ. 0.02 για 2%)
    customers_accept_discount,       # c6: ποσοστό πελατών που αποδέχεται έκπτωση (π.χ. 0.4)
    days_pay_discount,               # c7: μέρες πληρωμής για πελάτες με έκπτωση (π.χ. 10)
    days_pay_no_discount,            # c8: μέρες πληρωμής πελατών χωρίς έκπτωση (π.χ. 30)
    additional_sales_pct,            # c9: αύξηση πωλήσεων λόγω έκπτωσης (π.χ. 0.1 για +10%)
    wacc,                           # c10: κόστος κεφαλαίου (π.χ. 0.1 για 10% ετήσιο)
    supplier_payment_days           # c15: μέση περίοδος αποπληρωμής προμηθευτών (π.χ. 30)
):
    # 1. Τρέχουσα μέση περίοδος είσπραξης (σταθμισμένος μέσος όρος)
    current_avg_collection_days = (
        days_pay_discount * customers_accept_discount +
        days_pay_no_discount * (1 - customers_accept_discount)
    )
    
    # 2. Τρέχουσες απαιτήσεις
    current_receivables = current_sales * current_avg_collection_days / 365
    
    # 3. Νέα μέση περίοδος είσπραξης μετά την έκπτωση
    new_avg_collection_days_discount = (
        days_pay_discount * customers_accept_discount +
        days_pay_no_discount * (1 - customers_accept_discount)
    )
    
    # 4. Νέες απαιτήσεις μετά την έκπτωση
    new_receivables_discount = current_sales * new_avg_collection_days_discount / 365
    
    # 5. Αποδέσμευση κεφαλαίων από μείωση απαιτήσεων (πριν αύξηση πωλήσεων)
    capital_released_before_sales_increase = current_receivables - new_receivables_discount
    
    # 6. % πελατών που ακολουθεί τη νέα πολιτική επί του νέου συνόλου
    additional_sales = current_sales * additional_sales_pct
    new_total_sales = current_sales + additional_sales
    pct_customers_new_policy = (
        (current_sales * customers_accept_discount + additional_sales) / new_total_sales
    )
    
    # 7. % πελατών που παραμένει με την παλιά κατάσταση επί του νέου συνόλου
    pct_customers_old_policy = 1 - pct_customers_new_policy
    
    # 8. Νέα μέση περίοδος είσπραξης μετά την αύξηση πωλήσεων
    new_avg_collection_days_after_increase = (
        pct_customers_new_policy * days_pay_discount +
        pct_customers_old_policy * days_pay_no_discount
    )
    
    # 9. Απαιτήσεις μετά την αύξηση πωλήσεων
    receivables_after_sales_increase = new_total_sales * new_avg_collection_days_after_increase / 365
    
    # 10. Τελική αποδέσμευση κεφαλαίων μετά την αύξηση πωλήσεων
    capital_released_after_sales_increase = current_receivables - receivables_after_sales_increase
    
    # 11. Κέρδος από επιπλέον πωλήσεις (brutto)
    profit_additional_sales = additional_sales * gross_margin
    
    # 12. Κέρδος από αποδέσμευση κεφαλαίων
    profit_from_capital_release = capital_released_after_sales_increase * wacc
    
    # 13. Κόστος έκπτωσης
    discount_cost = new_total_sales * pct_customers_new_policy * discount_rate
    
    # 14. Συνολικό κέρδος από την πρόταση
    total_profit = profit_additional_sales + profit_from_capital_release - discount_cost
    
    # Παράμετροι για NPV:
    daily_wacc = (1 + wacc) ** (1/365) - 1
    
    # 15. NPV (με προεξόφληση ανά ημέρα)
    npv = (
        new_total_sales * pct_customers_new_policy * (1 - discount_rate) * (1 / (1 + daily_wacc) ** days_pay_discount) +
        new_total_sales * pct_customers_old_policy * (1 / (1 + daily_wacc) ** days_pay_no_discount) -
        current_sales * (additional_sales / current_sales) * (1 / (1 + daily_wacc) ** supplier_payment_days) * discount_cost / discount_rate -  # Προσαρμοσμένο κόστος (c11*...)
        current_sales * (1 / (1 + daily_wacc) ** supplier_payment_days)
    )
    
    # 16. Μέγιστη έκπτωση (Break-even NPV)
    # Έστω:
    A = (1 + daily_wacc) ** (days_pay_discount - days_pay_no_discount)
    B = (1 - (1 / pct_customers_new_policy))
    C = (1 + daily_wacc) ** (days_pay_no_discount - supplier_payment_days)
    D = (additional_sales / current_sales)
    E = (1 + daily_wacc) ** (days_pay_no_discount - supplier_payment_days)
    F = pct_customers_new_policy * (1 + D)
    
    try:
        max_discount = 1 - (A * (B + (C + D * E) / F))
        if max_discount < 0:
            max_discount = 0.0
    except ZeroDivisionError:
        max_discount = 0.0
    
    # 17. Βέλτιστη έκπτωση
    optimal_discount = (1 - (1 + daily_wacc) ** (days_pay_discount - current_avg_collection_days)) / 2
    
    return {
        "current_avg_collection_days": current_avg_collection_days,
        "current_receivables": current_receivables,
        "new_avg_collection_days_discount": new_avg_collection_days_discount,
        "new_receivables_discount": new_receivables_discount,
        "capital_released_before_sales_increase": capital_released_before_sales_increase,
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

def find_break_even_and_optimal(
    current_sales,
    extra_sales,
    gross_margin,
    accept_rate,
    days_accept,
    days_non_accept,
    current_collection_days,
    wacc
):
    discounts = [i / 1000 for i in range(0, 101)]  # 0.0 έως 0.1 (0%–10%)
    npv_list = []

    for d in discounts:
        result = calculate_cash_discount(
            current_sales, extra_sales, gross_margin,
            d, accept_rate, days_accept, days_non_accept,
            current_collection_days, wacc
        )
        npv_list.append(result["npv"])

    max_npv = max(npv_list)
    optimal_index = npv_list.index(max_npv)
    optimal_discount = discounts[optimal_index]

    breakeven_discount = None
    for i in range(1, len(npv_list)):
        if npv_list[i - 1] > 0 and npv_list[i] < 0:
            breakeven_discount = discounts[i]
            break

    return optimal_discount, breakeven_discount, discounts, npv_list


def show_discount_cash_tool():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    DEFAULTS = {
        "current_sales": 1000.0,
        "extra_sales": 250.0,
        "gross_margin": 0.20,
        "discount_rate": 0.0215,
        "accept_rate": 0.50,
        "days_accept": 60,
        "days_non_accept": 120,
        "current_collection_days": 90,
        "wacc": 0.20
    }

    with st.form("discount_form"):
        col1, col2 = st.columns(2)

        with col1:
            current_sales = st.number_input(
                "Τρέχουσες Πωλήσεις (€)",
                value=DEFAULTS["current_sales"],
                min_value=0.0, step=100.0, format="%.2f"
            )
            extra_sales = st.number_input(
                "Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)",
                value=DEFAULTS["extra_sales"],
                min_value=0.0, step=50.0, format="%.2f"
            )
            gross_margin = st.slider(
                "Καθαρό Περιθώριο Κέρδους (%)", 0, 100,
                int(DEFAULTS["gross_margin"] * 100), step=1
            ) / 100
            discount_rate = st.slider(
                "Έκπτωση (%)", 0.0, 30.0,
                DEFAULTS["discount_rate"] * 100, step=0.01
            ) / 100

        with col2:
            accept_rate = st.slider(
                "% Πελατών που Αποδέχεται την Έκπτωση", 0, 100,
                int(DEFAULTS["accept_rate"] * 100), step=5
            ) / 100
            days_accept = st.number_input(
                "Ημέρες Πληρωμής Αποδεκτών Έκπτωσης",
                value=DEFAULTS["days_accept"], min_value=0, max_value=365, step=1, format="%d"
            )
            days_non_accept = st.number_input(
                "Ημέρες Πληρωμής μη Αποδεκτών Έκπτωσης",
                value=DEFAULTS["days_non_accept"], min_value=0, max_value=365, step=1, format="%d"
            )
            current_collection_days = st.number_input(
                "Τρέχουσα Μέση Περίοδος Είσπραξης (μέρες)",
                value=DEFAULTS["current_collection_days"], min_value=0, max_value=365, step=1, format="%d"
            )
            wacc = st.slider(
                "WACC (%)", 0.0, 50.0,
                DEFAULTS["wacc"] * 100, step=0.01
            ) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        res = calculate_cash_discount(
            current_sales, extra_sales, gross_margin,
            discount_rate, accept_rate,
            days_accept, days_non_accept,
            current_collection_days, wacc
        )

        optimal_discount, breakeven_discount, discounts, npv_list = find_break_even_and_optimal(
            current_sales, extra_sales, gross_margin,
            accept_rate, days_accept, days_non_accept,
            current_collection_days, wacc
        )

        st.subheader("Αποτελέσματα")

        col1, col2, col3 = st.columns(3)

        col1.metric("Κέρδος από Επιπλέον Πωλήσεις (€)", format_number_gr(res["profit_extra"]))
        col1.metric("Κέρδος Αποδέσμευσης Κεφαλαίου (€)", format_number_gr(res["capital_saving_profit"]))
        col1.metric("Κόστος Έκπτωσης (€)", format_number_gr(res["discount_cost"]))

        col2.metric("Συνολικό Κέρδος (€)", format_number_gr(res["total_profit"]))
        col2.metric("Καθαρή Παρούσα Αξία (NPV) (€)", format_number_gr(res["npv"]))
        col2.metric("Νέα Μέση Περίοδος Είσπραξης (ημέρες)", f"{res['new_avg_days_total']:.1f}")

        col3.metric("Ποσοστό Πελατών με Έκπτωση (%)", format_percentage_gr(res["new_policy_pct"]))
        col3.metric("Νέες Πωλήσεις (€)", format_number_gr(current_sales + extra_sales))
        col3.metric("WACC (%)", format_percentage_gr(wacc))

        st.markdown("---")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[d * 100 for d in discounts],
            y=npv_list,
            mode='lines+markers',
            name="NPV"
        ))
        fig.add_vline(x=optimal_discount * 100, line_dash="dash", line_color="green",
                      annotation_text="Βέλτιστη Έκπτωση", annotation_position="top left")
        if breakeven_discount:
            fig.add_vline(x=breakeven_discount * 100, line_dash="dot", line_color="red",
                          annotation_text="Σημείο Ισορροπίας", annotation_position="bottom right")

        fig.update_layout(
            title="Ανάλυση Καθαρής Παρούσας Αξίας (NPV) σε Σχέση με την Έκπτωση",
            xaxis_title="Έκπτωση (%)",
            yaxis_title="Καθαρή Παρούσα Αξία (NPV) (€)",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    show_discount_cash_tool()
