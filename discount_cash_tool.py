import streamlit as st
import numpy as np
import plotly.graph_objects as go

from discount_cash_calculations import calculate_cash_discount, find_break_even_and_optimal

def format_number_gr(x):
    """Μορφοποίηση αριθμών με ελληνικά δεκαδικά (κόμμα) και χιλιάδες (τελεία)."""
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
def format_percentage_gr(x):
    """Μορφοποίηση ποσοστών με ελληνικά δεκαδικά."""
    return f"{x*100:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")

# Δημιουργούμε τη νέα version της συνάρτησης υπολογισμού με βάση τους αναλυτικούς τύπους του χρήστη

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
    decline_rate = 1 - accept_rate
    total_sales = current_sales + extra_sales

    # Τρέχουσες απαιτήσεις
    current_receivables = (current_sales * current_collection_days) / 365

    # Νέα μέση περίοδος είσπραξης μετά την έκπτωση (πριν την αύξηση πωλήσεων)
    new_avg_days_discount_only = (
        accept_rate * days_accept +
        decline_rate * days_non_accept
    )

    # Νέες απαιτήσεις με βάση τις τρέχουσες πωλήσεις
    new_receivables_discount_only = (current_sales * new_avg_days_discount_only) / 365

    # Αποδέσμευση κεφαλαίου (πριν την αύξηση πωλήσεων)
    capital_release_discount_only = current_receivables - new_receivables_discount_only

    # Ποσοστό πελατών που ακολουθεί τη νέα πολιτική στο νέο σύνολο
    new_policy_pct = ((current_sales * accept_rate) + extra_sales) / total_sales
    old_policy_pct = 1 - new_policy_pct

    # Νέα μέση περίοδος είσπραξης μετά την αύξηση πωλήσεων
    new_avg_days_total = (
        new_policy_pct * days_accept +
        old_policy_pct * days_non_accept
    )

    # Νέες απαιτήσεις μετά την αύξηση πωλήσεων
    new_receivables_total = (total_sales * new_avg_days_total) / 365

    # Οριστική αποδέσμευση κεφαλαίου
    capital_release_total = current_receivables - new_receivables_total

    # Κέρδος από επιπλέον πωλήσεις
    profit_extra = extra_sales * gross_margin

    # Κέρδος από αποδέσμευση κεφαλαίου (τοκισμένο)
    capital_saving_profit = capital_release_total * wacc

    # Κόστος έκπτωσης
    discount_cost = total_sales * new_policy_pct * discount_rate

    # Συνολικό κέρδος
    total_profit = profit_extra + capital_saving_profit - discount_cost

    # NPV (αναλυτικά με προεξόφληση)
    daily_wacc = wacc / 365
    npv = (
        total_sales * new_policy_pct * (1 - discount_rate) /
        ((1 + daily_wacc) ** days_accept)
        +
        total_sales * (1 - new_policy_pct) /
        ((1 + daily_wacc) ** days_non_accept)
        -
        discount_cost * (extra_sales / current_sales)
    )

    return {
        "current_receivables": round(current_receivables, 2),
        "new_avg_days_discount_only": round(new_avg_days_discount_only, 2),
        "new_receivables_discount_only": round(new_receivables_discount_only, 2),
        "capital_release_discount_only": round(capital_release_discount_only, 2),
        "new_policy_pct": round(new_policy_pct, 2),
        "old_policy_pct": round(old_policy_pct, 2),
        "new_avg_days_total": round(new_avg_days_total, 2),
        "new_receivables_total": round(new_receivables_total, 2),
        "capital_release_total": round(capital_release_total, 2),
        "profit_extra": round(profit_extra, 2),
        "capital_saving_profit": round(capital_saving_profit, 2),
        "discount_cost": round(discount_cost, 2),
        "total_profit": round(total_profit, 2),
        "npv": round(npv, 2)
    }

def show_discount_cash_tool():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    # Προεπιλεγμένες τιμές
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

        # Γράφημα NPV ανά ποσοστό έκπτωσης
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=discounts * 100,
            y=npv_list,
            mode='lines+markers',
            name="NPV"
        ))
        fig.add_vline(x=optimal_discount * 100, line_dash="dash", line_color="green",
                      annotation_text=f"Βέλτιστη Έκπτωση: {optimal_discount*100:.2f}%",
                      annotation_position="top left")
        fig.add_vline(x=breakeven_discount * 100, line_dash="dash", line_color="red",
                      annotation_text=f"Break-Even Έκπτωση: {breakeven_discount*100:.2f}%",
                      annotation_position="bottom right")

        fig.update_layout(
            title="Καμπύλη Καθαρής Παρούσας Αξίας (NPV) ανά Ποσοστό Έκπτωσης",
            xaxis_title="Ποσοστό Έκπτωσης (%)",
            yaxis_title="NPV (€)",
            template="plotly_white",
            height=400,
            margin=dict(t=50, b=40, l=60, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    show_discount_cash_tool()
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
    discounts = [i / 1000 for i in range(0, 101)]  # 0.0 έως 0.1 (δηλ. 0%–10%)
    npv_list = []
    
    for d in discounts:
        result = calculate_cash_discount(
            current_sales, extra_sales, gross_margin,
            d, accept_rate, days_accept, days_non_accept,
            current_collection_days, wacc
        )
        npv_list.append(result["npv"])
    
    # Βέλτιστη έκπτωση: αυτή που δίνει μέγιστο NPV
    max_npv = max(npv_list)
    optimal_index = npv_list.index(max_npv)
    optimal_discount = discounts[optimal_index]
    
    # Break-even: όπου το NPV αλλάζει πρόσημο
    breakeven_discount = None
    for i in range(1, len(npv_list)):
        if npv_list[i - 1] > 0 and npv_list[i] < 0:
            breakeven_discount = discounts[i]
            break

    return optimal_discount, breakeven_discount, discounts, npv_list
