import streamlit as st
import numpy as np
import plotly.graph_objects as go

def format_number_gr(x):
    """Μορφοποίηση αριθμών με ελληνικά δεκαδικά (κόμμα) και χιλιάδες (τελεία)."""
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(x):
    """Μορφοποίηση ποσοστών με ελληνικά δεκαδικά."""
    return f"{x*100:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")

def calculate_cash_discount(
    current_sales, extra_sales, gross_margin,
    discount_rate, accept_rate,
    days_accept, days_non_accept,
    current_collection_days, wacc
):
    """
    Υπολογίζει τα διάφορα κέρδη και κόστη από την πολιτική έκπτωσης τοις μετρητοίς.
    Επιστρέφει λεξικό με αποτελέσματα.
    """
    profit_extra = extra_sales * gross_margin
    new_sales = current_sales + extra_sales

    # Ποσοστό πωλήσεων με νέα πολιτική (αποδεκτών έκπτωσης)
    pct_new_policy = (current_sales * accept_rate + extra_sales) / new_sales
    pct_old_policy = 1 - pct_new_policy

    # Νέα μέση μέρα είσπραξης
    new_avg_days = pct_new_policy * days_accept + pct_old_policy * days_non_accept

    # Παλιές και νέες απαιτήσεις σε κεφάλαιο κίνησης (σε μονάδες €)
    old_receivables = (current_sales * current_collection_days) / 365
    new_receivables = (new_sales * new_avg_days) / 365

    capital_released = old_receivables - new_receivables
    profit_release = capital_released * wacc

    discount_cost = new_sales * pct_new_policy * discount_rate

    total_profit = profit_extra + profit_release - discount_cost

    # Καθαρή παρούσα αξία με προεξόφληση WACC
    npv = total_profit / (1 + wacc)

    return {
        "profit_extra": profit_extra,
        "profit_release": profit_release,
        "discount_cost": discount_cost,
        "total_profit": total_profit,
        "npv": npv,
        "pct_new_policy": pct_new_policy,
        "new_sales": new_sales,
        "new_avg_days": new_avg_days
    }

def find_break_even_and_optimal(
    current_sales, extra_sales, gross_margin,
    accept_rate, days_accept, days_non_accept,
    current_collection_days, wacc
):
    """
    Εύρεση βέλτιστης και break-even έκπτωσης με σάρωση από 0% έως 30%.
    Επιστρέφει βέλτιστη έκπτωση, break-even έκπτωση, καθώς και τα δεδομένα για το γράφημα.
    """
    discounts = np.linspace(0.0, 0.30, 301)
    npv_list = []

    for d in discounts:
        res = calculate_cash_discount(
            current_sales, extra_sales, gross_margin,
            d, accept_rate, days_accept, days_non_accept,
            current_collection_days, wacc
        )
        npv_list.append(res["npv"])

    npv_arr = np.array(npv_list)
    idx_opt = npv_arr.argmax()
    optimal_discount = discounts[idx_opt]

    # Break-even: έκπτωση με NPV πιο κοντά στο 0 (είτε θετικό είτε αρνητικό)
    idx_be = (np.abs(npv_arr)).argmin()
    breakeven_discount = discounts[idx_be]

    return optimal_discount, breakeven_discount, discounts, npv_list

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
        col1.metric("Κέρδος Αποδέσμευσης Κεφαλαίου (€)", format_number_gr(res["profit_release"]))
        col1.metric("Κόστος Έκπτωσης (€)", format_number_gr(res["discount_cost"]))

        col2.metric("Συνολικό Κέρδος (€)", format_number_gr(res["total_profit"]))
        col2.metric("Καθαρή Παρούσα Αξία (NPV) (€)", format_number_gr(res["npv"]))
        col2.metric("Νέα Μέση Περίοδος Είσπραξης (ημέρες)", f"{res['new_avg_days']:.1f}")

        col3.metric("Ποσοστό Πελατών με Έκπτωση (%)", format_percentage_gr(res["pct_new_policy"]))
        col3.metric("Νέες Πωλήσεις (€)", format_number_gr(res["new_sales"]))
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

