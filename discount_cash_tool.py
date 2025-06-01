import streamlit as st
import numpy as np
import plotly.graph_objects as go

def show_discount_cash_tool():
    DEFAULTS = {
        "current_sales": 1000,
        "extra_sales": 250,
        "cost_pct": 0.80,
        "wacc": 0.20,
        "cash_discount_accept_pct": 0.50,
        "cash_discount_days": 10,
        "non_discount_accept_days": 120,
        "cash_discount_accept_days": 60,
        "current_collection_period": 90
    }

    def format_number_gr(x):
        try:
            return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            return str(x)

    def format_percentage_gr(x):
        try:
            return f"{x*100:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            return str(x)

    def calculate_discount_npv(current_sales, extra_sales, discount_rate, accept_rate,
                               days_discount, days_accept, days_non_accept,
                               cost_pct, wacc, current_collection_period):
        """
        Υπολογίζει NPV βασισμένο στην αποδέσμευση κεφαλαίων, το κέρδος από επιπλέον πωλήσεις, 
        και το κόστος της έκπτωσης.
        """
        # Νέα μέση περίοδος είσπραξης μετά την έκπτωση
        new_avg_collection = accept_rate * days_accept + (1 - accept_rate) * days_non_accept

        # Αποδεσμευόμενα κεφάλαια (παλιά - νέα)
        old_receivables = (current_sales * current_collection_period) / 365
        new_receivables = (current_sales * (1 - discount_rate) * new_avg_collection) / 365
        capital_release = old_receivables - new_receivables

        # Κέρδος από επιπλέον πωλήσεις (με κόστος)
        profit_extra_sales = extra_sales * (1 - cost_pct)

        # Κέρδος από αποδέσμευση κεφαλαίων (πληρώνουμε λιγότερο κόστος κεφαλαίου)
        profit_release = capital_release * wacc

        # Κόστος έκπτωσης που αποδέχονται οι πελάτες
        cost_discount = current_sales * discount_rate * accept_rate

        # Καθαρό NPV
        npv = profit_extra_sales + profit_release - cost_discount

        return {
            'capital_release': capital_release,
            'profit_extra_sales': profit_extra_sales,
            'profit_release': profit_release,
            'cost_discount': cost_discount,
            'total_profit': npv,
            'npv': npv
        }

    def find_optimal_and_breakeven(discount_rates, current_sales, extra_sales, accept_rate,
                                   days_discount, days_accept, days_non_accept,
                                   cost_pct, wacc, current_collection_period):
        npvs = [calculate_discount_npv(
            current_sales, extra_sales, d, accept_rate,
            days_discount, days_accept, days_non_accept,
            cost_pct, wacc, current_collection_period
        )['npv'] for d in discount_rates]

        max_npv = max(npvs)
        max_index = npvs.index(max_npv)
        optimal_discount = discount_rates[max_index]

        # Βρίσκουμε το break-even σημείο (όπου το NPV διασχίζει το 0)
        breakeven_discount = None
        for i in range(1, len(npvs)):
            if npvs[i-1] > 0 >= npvs[i]:
                # Γραμμική παρεμβολή για ακρίβεια
                x0, x1 = discount_rates[i-1], discount_rates[i]
                y0, y1 = npvs[i-1], npvs[i]
                breakeven_discount = x0 - y0 * (x1 - x0) / (y1 - y0)
                break

        return optimal_discount, breakeven_discount, npvs

    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    with st.form("discount_form"):
        col1, col2 = st.columns(2)

        with col1:
            sales_now = st.number_input(
                "Τρέχουσες Πωλήσεις (€)", 
                value=DEFAULTS["current_sales"], 
                min_value=0, 
                step=100, 
                format="%d"
            )
            extra_sales = st.number_input(
                "Επιπλέον Πωλήσεις λόγω Έκπτωσης (€)", 
                value=DEFAULTS["extra_sales"], 
                min_value=0, 
                step=50, 
                format="%d"
            )
            discount_rate = st.slider(
                "Ποσοστό Έκπτωσης (%)", 0.0, 30.0, 2.0, step=0.5
            ) / 100
            accept_rate = st.slider(
                "% Πελατών που Αποδέχεται την Έκπτωση", 0, 100, int(DEFAULTS["cash_discount_accept_pct"]*100), step=5
            ) / 100
            cost_ratio = st.slider(
                "Κόστος Πωλήσεων (% επί των Πωλήσεων)", 0, 100, int(DEFAULTS["cost_pct"]*100), step=1
            ) / 100

        with col2:
            days_discount = st.number_input(
                "Μέρες για Πληρωμή με Έκπτωση", 
                value=DEFAULTS["cash_discount_days"], 
                min_value=0, max_value=180, 
                step=1,
                format="%d"
            )
            days_accept = st.number_input(
                "Μέρες Πληρωμής όσων Αποδέχονται την Έκπτωση", 
                value=DEFAULTS["cash_discount_accept_days"], 
                min_value=0, max_value=180,
                step=1,
                format="%d"
            )
            days_non_accept = st.number_input(
                "Μέρες Πληρωμής όσων Δεν Αποδέχονται την Έκπτωση", 
                value=DEFAULTS["non_discount_accept_days"], 
                min_value=0, max_value=180,
                step=1,
                format="%d"
            )
            wacc = st.slider(
                "Κόστος Κεφαλαίου (WACC %)", 0.0, 30.0, float(DEFAULTS["wacc"]*100), step=1.0
            ) / 100
            avg_collection_days = st.number_input(
                "Τρέχουσα Μέση Περίοδος Είσπραξης (μέρες)", 
                value=DEFAULTS["current_collection_period"], 
                min_value=0, max_value=365,
                step=1,
                format="%d"
            )

        submitted = st.form_submit_button("Υπολογισμός")

        if submitted:
            results = calculate_discount_npv(
                sales_now, extra_sales, discount_rate, accept_rate,
                days_discount, days_accept, days_non_accept,
                cost_ratio, wacc, avg_collection_days
            )

            discount_rates = np.arange(0.0, 0.31, 0.01)
            optimal_discount, breakeven_discount, npvs = find_optimal_and_breakeven(
                discount_rates, sales_now, extra_sales, accept_rate,
                days_discount, days_accept, days_non_accept,
                cost_ratio, wacc, avg_collection_days
            )

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=discount_rates * 100,
                y=npvs,
                mode='lines+markers',
                name='NPV',
                line=dict(color='royalblue')
            ))

            fig.add_vline(x=optimal_discount * 100, line=dict(color='green', dash='dash'),
                          annotation_text=f"Βέλτιστη: {optimal_discount*100:.2f}%", annotation_position="top left")

            if breakeven_discount is not None:
                fig.add_vline(x=breakeven_discount * 100, line=dict(color='red', dash='dash'),
                              annotation_text=f"Break-even: {breakeven_discount*100:.2f}%", annotation_position="top right")

            fig.update_layout(
                xaxis_title='Ποσοστό Έκπτωσης (%)',
                yaxis_title='Καθαρή Παρούσα Αξία (NPV)',
                title='NPV vs Ποσοστό Έκπτωσης για πληρωμή τοις μετρητοίς',
                hovermode='x unified',
                template='simple_white'
            )

            st.subheader("Αποτελέσματα")
            col1, col2, col3 = st.columns(3)

            col1.metric("Αποδέσμευση Κεφαλαίων (€)", format_number_gr(results['capital_release']))
            col1.metric("Κέρδος Επιπλέον Πωλήσεων (€)", format_number_gr(results['profit_extra_sales']))
            col1.metric("Κόστος Έκπτωσης (€)", format_number_gr(results['cost_discount']))

            col2.metric("Κέρδος από Αποδέσμευση (€)", format_number_gr(results['profit_release']))
            col2.metric("Συνολικό Κέρδος (€)", format_number_gr(results['total_profit']))
            col2.metric("NPV (€)", format_number_gr(results['npv']))

            col3.metric("Οριακή Έκπτωση για NPV = 0", format_percentage_gr(breakeven_discount if breakeven_discount else 0))
            col3.metric("Βέλτιστη Έκπτωση", format_percentage_gr(optimal_discount))

            st.subheader("📈 Διάγραμμα NPV σε σχέση με την Έκπτωση")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            - ✅ Η **πράσινη διακεκομμένη γραμμή** δείχνει τη βέλτιστη έκπτωση που μεγιστοποιεί το NPV.
            - ❌ Η **κόκκινη διακεκομμένη γραμμή** δείχνει το break-even σημείο (όπου το NPV = 0).
            - 📉 Πέρα από το βέλτιστο σημείο, το κόστος της έκπτωσης υπερκαλύπτει τα οφέλη.
            """)

# Για να εμφανίσεις το εργαλείο, απλά κάλεσε:
# show_discount_cash_tool()
