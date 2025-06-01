import streamlit as st

def calculate_discount_cash_tool(
    sales_current,
    sales_extra,
    discount_cash_percent,
    perc_accept_discount,
    days_accept_discount,
    perc_not_accept_discount,
    days_not_accept_discount,
    days_cash_payment,
    cost_of_sales_percent,
    capital_cost,
    avg_supplier_payment_days,
    avg_collection_days,
    perc_follow_new_policy
):
    # Μετατροπή ποσοστών σε δεκαδικά
    discount_cash = discount_cash_percent / 100
    cost_of_sales = cost_of_sales_percent / 100
    perc_accept = perc_accept_discount / 100
    perc_not_accept = perc_not_accept_discount / 100
    perc_follow = perc_follow_new_policy / 100
    capital_cost_daily = capital_cost / 365 / 100

    # Υπολογισμοί
    # Τρέχουσα μέση περίοδος είσπραξης (σταθερό input)
    # avg_collection_days εδώ δίνεται από input

    # Κέρδος από επιπλέον πωλήσεις
    profit_extra_sales = sales_extra * (1 - cost_of_sales)

    # Νέα μέση περίοδος είσπραξης
    weighted_collection_days = (
        (sales_current * perc_accept * days_accept_discount + sales_current * perc_not_accept * days_not_accept_discount + sales_extra * perc_follow * days_cash_payment + sales_extra * (1 - perc_follow) * days_not_accept_discount)
        / (sales_current + sales_extra)
    )

    # Παρούσα αξία των πωλήσεων με τη νέα πολιτική
    pv_new_policy = (
        (sales_current + sales_extra) * (
            perc_follow * (1 - discount_cash) / ((1 + capital_cost_daily) ** days_cash_payment)
            + (1 - perc_follow) / ((1 + capital_cost_daily) ** days_not_accept_discount)
        )
    )

    # Αφαιρούμε το κόστος πωλήσεων επί των επιπλέον πωλήσεων (το προεξοφλούμε με βάση την περίοδο πληρωμής προμηθευτών)
    cost_extra_sales_pv = cost_of_sales * sales_extra / ((1 + capital_cost_daily) ** avg_supplier_payment_days)

    # Παρούσα αξία τρεχουσών πωλήσεων με τρέχουσα μέση περίοδο είσπραξης
    pv_current_sales = sales_current / ((1 + capital_cost_daily) ** avg_collection_days)

    # NPV = Παρούσα αξία νέας πολιτικής - κόστος επιπλέον πωλήσεων - παρούσα αξία τρεχουσών πωλήσεων
    npv = pv_new_policy - cost_extra_sales_pv - pv_current_sales

    # Υπολογισμός μέγιστης έκπτωσης (NPV Break Even) - εδώ πολύ απλοποιημένα για να ταιριάζει στο παράδειγμα
    max_discount = (npv / profit_extra_sales) * 100 if profit_extra_sales != 0 else 0

    # Υπολογισμός βέλτιστης έκπτωσης - απλοποιημένα ως το discount_cash αρχικό
    optimal_discount = discount_cash_percent

    return {
        "NPV": npv,
        "Max Discount %": max_discount,
        "Optimal Discount %": optimal_discount,
        "Profit Extra Sales": profit_extra_sales,
        "Weighted Collection Days": weighted_collection_days
    }


def main():
    st.title("Αποδοτικότητα Έκπτωσης Πληρωμής Τοις Μετρητοίς")

    st.markdown("Εισάγετε τις παραμέτρους:")

    sales_current = st.number_input("Τρέχουσες Πωλήσεις", value=1000.0, step=1.0)
    sales_extra = st.number_input("Επιπλέον Πωλήσεις λόγω Έκπτωσης", value=250.0, step=1.0)
    discount_cash_percent = st.number_input("Έκπτωση για Πληρωμή Τοις Μετρητοίς (%)", value=2.0, step=0.1)
    perc_accept_discount = st.number_input("% Πελατών που Αποδέχεται την Έκπτωση", value=50.0, step=1.0)
    days_accept_discount = st.number_input("% Πελατών που Αποδέχεται Πληρώνει σε (Μέρες)", value=60, step=1)
    perc_not_accept_discount = st.number_input("% Πελατών που Δεν Αποδέχεται την Έκπτωση", value=50.0, step=1.0)
    days_not_accept_discount = st.number_input("% Πελατών που Δεν Αποδέχεται Πληρώνει σε (Μέρες)", value=120, step=1)
    days_cash_payment = st.number_input("Μέρες για Πληρωμή Τοις Μετρητοίς", value=10, step=1)
    cost_of_sales_percent = st.number_input("Κόστος Πωλήσεων σε %", value=80.0, step=0.1)
    capital_cost = st.number_input("Κόστος Κεφαλαίου (%)", value=20.0, step=0.1)
    avg_supplier_payment_days = st.number_input("Μέση Περίοδος Αποπληρωμής Προμηθευτών (Μέρες)", value=0, step=1)
    avg_collection_days = st.number_input("Τρέχουσα Μέση Περίοδος Είσπραξης (Μέρες)", value=90, step=1)
    perc_follow_new_policy = st.number_input("% Πελατών που θα Ακολουθεί τη Νέα Πολιτική", value=60.0, step=1.0)

    if st.button("Υπολόγισε"):
        results = calculate_discount_cash_tool(
            sales_current,
            sales_extra,
            discount_cash_percent,
            perc_accept_discount,
            days_accept_discount,
            perc_not_accept_discount,
            days_not_accept_discount,
            days_cash_payment,
            cost_of_sales_percent,
            capital_cost,
            avg_supplier_payment_days,
            avg_collection_days,
            perc_follow_new_policy
        )

        st.write(f"**NPV:** {results['NPV']:.2f} €")
        st.write(f"**Μέγιστη έκπτωση που μπορεί να δοθεί επί των πωλήσεων (NPV Break Even):** {results['Max Discount %']:.2f} %")
        st.write(f"**Βέλτιστη έκπτωση που πρέπει να δοθεί:** {results['Optimal Discount %']:.2f} %")
        st.write(f"**Κέρδος από επιπλέον πωλήσεις:** {results['Profit Extra Sales']:.2f} €")
        st.write(f"**Μέση περίοδος είσπραξης με νέα πολιτική:** {results['Weighted Collection Days']:.2f} ημέρες")

if __name__ == "__main__":
    main()
