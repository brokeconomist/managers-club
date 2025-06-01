import streamlit as st
import numpy as np
import plotly.graph_objects as go

def show_discount_cash_tool():
    DEFAULTS = {
        "current_sales": 1000.0,           # Τρέχουσες πωλήσεις (€)
        "extra_sales": 250.0,              # Επιπλέον πωλήσεις λόγω έκπτωσης (€)
        "gross_margin": 0.20,              # Καθαρό περιθώριο κέρδους (20%)
        "discount_rate": 0.0215,           # Έκπτωση (2,15%)
        "accept_rate": 0.50,               # % πελατών που αποδέχεται έκπτωση (50%)
        "days_accept": 60,                 # Ημέρες πληρωμής αποδεκτών έκπτωσης
        "days_non_accept": 120,            # Ημέρες πληρωμής μη αποδεκτών έκπτωσης
        "current_collection_days": 90,     # Τρέχουσα μέση περίοδος είσπραξης
        "wacc": 0.20                       # WACC (20%)
    }

    def format_number_gr(x):
        return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def format_percentage_gr(x):
        return f"{x*100:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")

    def calculate_cash_discount(
        current_sales, extra_sales, gross_margin,
        discount_rate, accept_rate,
        days_accept, days_non_accept,
        current_collection_days, wacc
    ):
        # 1. Κέρδος από επιπλέον πωλήσεις
        profit_extra = extra_sales * gross_margin

        # 2. Νέο σύνολο πωλήσεων μετά την έκπτωση
        new_sales = current_sales + extra_sales

        # 3. Ποσοστό πελατών μετά την αύξηση πωλήσεων
        pct_new_policy = (current_sales * accept_rate + extra_sales) / new_sales
        pct_old_policy = 1 - pct_new_policy

        # 4. Νέα μεσοσταθμική μέση περίοδος είσπραξης
        new_avg_days = pct_new_policy * days_accept + pct_old_policy * days_non_accept

        # 5. Απαιτήσεις (παλαιές και νέες) σε € (365 ημέρες)
        old_receivables = (current_sales * current_collection_days) / 365
        new_receivables = (new_sales * new_avg_days) / 365

        # 6. Αποδέσμευση κεφαλαίων
        capital_released = old_receivables - new_receivables
        profit_release = capital_released * wacc

        # 7. Κόστος έκπτωσης
        discount_cost = new_sales * pct_new_policy * discount_rate

        # 8. Συνολικό καθαρό όφελος (πριν προεξόφληση)
        total_profit = profit_extra + profit_release - discount_cost

        # 9. Καθαρή Παρούσα Αξία (NPV) – απλή προεξόφληση 1 έτους
        npv = total_profit / (1 + wacc)

        return {
            "profit_extra": profit_extra,
            "profit_release": profit_release,
            "discount_cost": discount_cost,
            "total_profit": total_profit,
            "npv": npv,
            "pct_new_policy": pct_new_policy,
            "new_sales": new_sales
        }

    def find_break_even_and_optimal(
        current_sales, extra_sales, gross_margin,
        accept_rate, days_accept, days_non_accept,
        current_collection_days, wacc
    ):
        # Δοκιμάζουμε ποσοστά έκπτωσης από 0% έως 50% βήμα 0.1%
        discounts = np.linspace(0.0, 0.50, 501)
        npv_list = []
        for d in discounts:
            res = calculate_cash_discount(
                current_sales, extra_sales, gross_margin,
                d, accept_rate, days_accept, days_non_accept,
                current_collection_days, wacc
            )
            npv_list.append(res["npv"])
        npv_arr = np.array(npv_list)

        # 1. Βέλτιστη έκπτωση = εκεί που το NPV μεγιστοποιείται
        idx_opt = npv_arr.argmax()
        optimal_discount = discounts[idx_opt]

        # 2. Break-even έκπτωση (πλησιέστερο σημείο όπου NPV ≈ 0)
        idx_be = (np.abs(npv_arr)).argmin()
        breakeven_discount = discounts[idx_be]

        return optimal_discount, breakeven_discount, discounts, npv_list

    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

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
                "Καθαρό Περιθώριο Κέρδους (%)", 0.0, 100.0,
                int(DEFAULTS["gross_margin"] * 100), step=1
            ) / 100

            discount_rate = st.slider(
                "Έκπτωση (%)", 0.0, 30.0,
                DEFAULTS["discount_rate"] * 100, step=0.1
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
                DEFAULTS["wacc"] * 100, step=0.1
            ) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        # Υπολογισμοί βάσει διορθωμένων τύπων
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

        # Δείχνουμε αποτελέσματα
        st.subheader("Αποτελέσματα")
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Κέρδος από Επιπλέον Πωλήσεις (€)", 
            format_number_gr(res["profit_extra"])
        )
        col1.metric(
            "Κέρδος Αποδέσμευσης Κεφαλαίου (€)", 
            format_number_gr(res["profit_release"])
        )
        col1.metric(
            "Κόστος Έκπτωσης (€)", 
            format_number_gr(res["discount_cost"])
        )

        col2.metric(
            "Συνολικό Κέρδος (€)", 
            format_number_gr(res["total_profit"])
        )
        col2.metric(
            "NPV (€)", 
            format_number_gr(res["npv"])
        )
        col2.metric(
            "Βέλτιστη Έκπτωση", 
            format_percentage_gr(optimal_discount)
        )

        col3.metric(
            "Έκπτωση Break-even", 
            format_percentage_gr(breakeven_discount)
        )
        col3.metric(
            "Νέα Μέση Ημ./Είσπραξης", 
            format_number_gr(
                res["pct_new_policy"] * days_accept + 
                (1 - res["pct_new_policy"]) * days_non_accept
            )  # μόλις για ενημέρωση
        )
        col3.metric(
            "Ποσ.% Πελατών Έκπτωσης", 
            format_percentage_gr(res["pct_new_policy"])
        )

        # Γράφημα NPV vs Έκπτωση
        st.subheader("📈 Διάγραμμα NPV vs Ποσοστό Έκπτωσης")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=np.array(discounts) * 100,
            y=np.array(npv_list),
            mode="lines",
            name="NPV"
        ))
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        fig.add_vline(
            x=optimal_discount * 100, 
            line_dash="dash", line_color="green",
            annotation_text=f"Βέλτιστη: {optimal_discount*100:.2f}%",
            annotation_position="top left"
        )
        fig.add_vline(
            x=breakeven_discount * 100, 
            line_dash="dash", line_color="red",
            annotation_text=f"Break-even: {breakeven_discount*100:.2f}%",
            annotation_position="top right"
        )
        fig.update_layout(
            xaxis_title="Έκπτωση (%)",
            yaxis_title="Καθαρή Παρούσα Αξία (NPV €)",
            template="simple_white",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        - ✅ **Κέρδος από επιπλέον πωλήσεις** μεταφέρει πρόσθετο περιθώριο.
        - ✅ **Κέρδος αποδέσμευσης κεφαλαίου** προκύπτει από τη μείωση των απαιτήσεων.
        - ❌ **Κόστος έκπτωσης** χρεώνει τμήμα τζίρου.
        - 📈 Η πράσινη γραμμή δείχνει τη βέλτιστη έκπτωση, η κόκκινη το Break-even.
        """)

# Για να το χρησιμοποιήσεις, απλώς κάνεις:
# from discount_cash_tool import show_discount_cash_tool
# και το καλείς στο app.py σου
