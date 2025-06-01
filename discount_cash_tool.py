import streamlit as st

def discount_cash_flow_calculations(
    current_sales,
    additional_sales,
    cash_discount_pct,
    pct_customers_accept_discount,
    days_discount_payers,
    pct_customers_no_discount,
    days_no_discount_payers,
    days_cash_payment,
    cost_of_sales_pct,
    cost_of_capital_pct,
    avg_receivable_days_current,
    pct_customers_follow_policy,
):
    # Υπολογισμοί κόστους πωλήσεων
    cost_current_sales = current_sales * cost_of_sales_pct / 100
    cost_additional_sales = additional_sales * cost_of_sales_pct / 100

    # Κέρδος από επιπλέον πωλήσεις (μεικτό)
    profit_additional_sales = additional_sales * (1 - cost_of_sales_pct / 100)

    # Μέση περίοδος είσπραξης μετά την αλλαγή πολιτικής (σταθμισμένος μέσος όρος)
    # Ποσοστό πελατών που ακολουθεί τη νέα πολιτική (επί του συνόλου νέων πωλήσεων)
    weighted_days = (
        pct_customers_accept_discount / 100 * days_discount_payers +
        pct_customers_no_discount / 100 * days_no_discount_payers
    )

    # Τρέχουσα μέση περίοδος είσπραξης
    current_avg_receivable_days = avg_receivable_days_current

    # Νέα μέση περίοδος είσπραξης μετά την πολιτική (σταθμισμένη)
    new_avg_receivable_days = (
        pct_customers_follow_policy / 100 * weighted_days +
        (1 - pct_customers_follow_policy / 100) * current_avg_receivable_days
    )

    # Αποδέσμευση κεφαλαίου (μέρες αποπληρωμής αλλάζει)
    capital_released_days = current_avg_receivable_days - new_avg_receivable_days

    # Αξία αποδέσμευσης κεφαλαίου (σε €)
    # Υποθέτουμε ημερήσιες πωλήσεις = συνολικές πωλήσεις / 360 (χρησιμοποιούμε 360 για οικονομία)
    total_sales = current_sales + additional_sales
    daily_sales = total_sales / 360
    capital_released_value = capital_released_days * daily_sales * cost_of_sales_pct / 100

    # Υπολογισμός NPV του κέρδους από επιπλέον πωλήσεις + κεφαλαίου που αποδεσμεύεται
    # Απλοποίηση: κεφάλαιο αποδέσμευσης θεωρείται άμεσο όφελος χωρίς χρονική καθυστέρηση
    # Χρησιμοποιούμε κόστος κεφαλαίου ως προεξοφλητικό συντελεστή για επιπλέον πωλήσεις (1 έτος)
    npv_profit = profit_additional_sales / (1 + cost_of_capital_pct / 100) + capital_released_value

    # Μέγιστη έκπτωση (Break Even) που μπορεί να δοθεί
    # Ισοδυναμεί στο να μηδενίζει το npv (από απλοποίηση)
    # max_discount = npv / (additional_sales * pct_customers_accept_discount / 100)
    # Θα το εκφράσουμε ως % επί των επιπλέον πωλήσεων

    max_discount = (npv_profit / (additional_sales * pct_customers_accept_discount / 100)) * 100 if additional_sales * pct_customers_accept_discount != 0 else 0

    # Βέλτιστη έκπτωση (για παράδειγμα το 1/4 της μέγιστης ως απλή υπόθεση)
    optimal_discount = max_discount / 4

    return {
        "Κέρδος από επιπλέον πωλήσεις": round(profit_additional_sales, 2),
        "NPV": round(npv_profit, 2),
        "Μέγιστη έκπτωση (Break Even %)": round(max_discount, 2),
        "Βέλτιστη έκπτωση (%)": round(optimal_discount, 2),
        "Νέα μέση περίοδος είσπραξης (μέρες)": round(new_avg_receivable_days, 2),
        "Αποδέσμευση κεφαλαίου (€)": round(capital_released_value, 2),
    }


def main():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    st.markdown("Συμπληρώστε τις παρακάτω παραμέτρους:")

    current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    additional_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", min_value=0.0, value=250.0, step=50.0, format="%.2f")
    cash_discount_pct = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1, format="%.2f")

    pct_customers_accept_discount = st.number_input("% πελατών που αποδέχεται την έκπτωση (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
    days_discount_payers = st.number_input("% πελατών που αποδέχεται την έκπτωση πληρώνει σε (μέρες)", min_value=0, value=60, step=1)

    pct_customers_no_discount = st.number_input("% πελατών που δεν αποδέχεται την έκπτωση (%)", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
    days_no_discount_payers = st.number_input("% πελατών που δεν αποδέχεται την έκπτωση πληρώνει σε (μέρες)", min_value=0, value=120, step=1)

    days_cash_payment = st.number_input("Μέρες για πληρωμή τοις μετρητοίς (π.χ. 10)", min_value=0, value=10, step=1)

    cost_of_sales_pct = st.number_input("Κόστος πωλήσεων σε %", min_value=0.0, max_value=100.0, value=80.0, step=0.1, format="%.2f")
    cost_of_capital_pct = st.number_input("Κόστος κεφαλαίου σε %", min_value=0.0, max_value=100.0, value=20.0, step=0.1, format="%.2f")

    avg_receivable_days_current = st.number_input("Τρέχουσα μέση περίοδος είσπραξης (μέρες)", min_value=0, value=90, step=1)

    pct_customers_follow_policy = st.number_input("% πελατών που θα ακολουθεί τη νέα πολιτική επί του νέου συνόλου (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)

    if st.button("Υπολόγισε"):
        results = discount_cash_flow_calculations(
            current_sales,
            additional_sales,
            cash_discount_pct,
            pct_customers_accept_discount,
            days_discount_payers,
            pct_customers_no_discount,
            days_no_discount_payers,
            days_cash_payment,
            cost_of_sales_pct,
            cost_of_capital_pct,
            avg_receivable_days_current,
            pct_customers_follow_policy,
        )

        st.subheader("Αποτελέσματα:")
        for key, value in results.items():
            st.write(f"**{key}:** {value}")

if __name__ == "__main__":
    main()
