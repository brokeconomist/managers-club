import streamlit as st

def format_number_gr(num):
    """Μορφοποίηση αριθμού με ελληνικά δεκαδικά (κόμμα) και χιλιάδες (τελεία)."""
    return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(value):
    """Μορφοποίηση ποσοστού με ελληνικό δεκαδικό κόμμα."""
    return f"{value * 100:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")

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

    current_receivables = (current_sales * current_collection_days) / 365

    new_days_post_discount = (
        accept_rate * days_accept +
        decline_rate * days_non_accept
    )

    new_receivables_pre_increase = (current_sales * new_days_post_discount) / 365

    capital_release_intermediate = current_receivables - new_receivables_pre_increase

    new_policy_share = ((current_sales * accept_rate) + extra_sales) / total_sales
    old_policy_share = 1 - new_policy_share

    new_collection_days = (
        new_policy_share * days_accept +
        old_policy_share * days_non_accept
    )

    new_receivables_total = (total_sales * new_collection_days) / 365

    capital_release = current_receivables - new_receivables_total

    profit_from_extra_sales = extra_sales * gross_margin

    capital_benefit = capital_release * wacc

    discount_cost = total_sales * new_policy_share * discount_rate

    total_profit = profit_from_extra_sales + capital_benefit - discount_cost

    daily_wacc = wacc / 365
    npv = (
        total_sales * new_policy_share * (1 - discount_rate) /
        ((1 + daily_wacc) ** days_accept)
        +
        total_sales * (1 - new_policy_share) /
        ((1 + daily_wacc) ** days_non_accept)
        -
        discount_cost * (extra_sales / current_sales)
    )

    return {
        "new_policy_share": new_policy_share,
        "new_collection_days": new_collection_days,
        "current_receivables": current_receivables,
        "new_receivables_total": new_receivables_total,
        "capital_release": capital_release,
        "profit_from_extra_sales": profit_from_extra_sales,
        "discount_cost": discount_cost,
        "capital_benefit": capital_benefit,
        "total_profit": total_profit,
        "npv": npv,
        "new_sales": total_sales
    }

def show_discount_cash_tool():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    current_sales = st.number_input("Τρέχουσες Πωλήσεις (€)", min_value=0.0, value=1000000.0, step=1000.0, format="%.2f")
    extra_sales = st.number_input("Επιπλέον Πωλήσεις από Έκπτωση (€)", min_value=0.0, value=100000.0, step=1000.0, format="%.2f")
    gross_margin = st.number_input("Μικτό Περιθώριο Κέρδους (π.χ. 0.35 για 35%)", min_value=0.0, max_value=1.0, value=0.35, format="%.4f")
    discount_rate = st.number_input("Ποσοστό Έκπτωσης (π.χ. 0.05 για 5%)", min_value=0.0, max_value=1.0, value=0.05, format="%.4f")
    accept_rate = st.number_input("Ποσοστό Πελατών που Αποδέχονται την Έκπτωση (π.χ. 0.8 για 80%)", min_value=0.0, max_value=1.0, value=0.8, format="%.4f")
    days_accept = st.number_input("Μέση Περίοδος Είσπραξης Πελατών με Έκπτωση (ημέρες)", min_value=1, value=20)
    days_non_accept = st.number_input("Μέση Περίοδος Είσπραξης Πελατών χωρίς Έκπτωση (ημέρες)", min_value=1, value=30)
    current_collection_days = st.number_input("Τρέχουσα Μέση Περίοδος Είσπραξης (ημέρες)", min_value=1, value=35)
    wacc = st.number_input("WACC (π.χ. 0.12 για 12%)", min_value=0.0, max_value=1.0, value=0.12, format="%.4f")

    if st.button("Υπολογισμός"):
        res = calculate_cash_discount(
            current_sales,
            extra_sales,
            gross_margin,
            discount_rate,
            accept_rate,
            days_accept,
            days_non_accept,
            current_collection_days,
            wacc
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Κέρδος από Επιπλέον Πωλήσεις (€)", format_number_gr(res["profit_from_extra_sales"]))
        col1.metric("Κέρδος Αποδέσμευσης Κεφαλαίου (€)", format_number_gr(res["capital_benefit"]))
        col1.metric("Κόστος Έκπτωσης (€)", format_number_gr(res["discount_cost"]))

        col2.metric("Συνολικό Κέρδος (€)", format_number_gr(res["total_profit"]))
        col2.metric("Καθαρή Παρούσα Αξία (NPV) (€)", format_number_gr(res["npv"]))
        col2.metric("Νέα Μέση Περίοδος Είσπραξης (ημέρες)", f"{res['new_collection_days']:.1f}")

        col3.metric("Ποσοστό Πελατών με Έκπτωση (%)", format_percentage_gr(res["new_policy_share"]))
        col3.metric("Νέες Πωλήσεις (€)", format_number_gr(res["new_sales"]))
        col3.metric("WACC (%)", format_percentage_gr(wacc))

if __name__ == "__main__":
    show_discount_cash_tool()
