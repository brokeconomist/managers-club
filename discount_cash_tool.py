import streamlit as st
import matplotlib.pyplot as plt

def cash_discount_analysis(
    current_sales, extra_sales, discount_rate,
    accept_rate, days_accept, days_non_accept,
    current_collection_days, gross_margin, wacc
):
    days_per_year = 365

    # --- Stage 1: Only discount effect ---
    new_sales_stage1 = current_sales
    pct_new_policy_stage1 = accept_rate
    pct_old_policy_stage1 = 1 - pct_new_policy_stage1
    new_avg_days_stage1 = pct_new_policy_stage1 * days_accept + pct_old_policy_stage1 * days_non_accept
    old_receivables = (current_sales * current_collection_days) / days_per_year
    new_receivables_stage1 = (new_sales_stage1 * new_avg_days_stage1) / days_per_year
    capital_released_stage1 = old_receivables - new_receivables_stage1
    profit_release_stage1 = capital_released_stage1 * wacc
    discount_cost_stage1 = new_sales_stage1 * pct_new_policy_stage1 * discount_rate
    profit_extra_stage1 = 0
    total_profit_stage1 = profit_extra_stage1 + profit_release_stage1 - discount_cost_stage1
    npv_stage1 = total_profit_stage1 / (1 + wacc)

    # --- Stage 2: Discount + extra sales ---
    new_sales_stage2 = current_sales + extra_sales
    pct_new_policy_stage2 = (current_sales * accept_rate + extra_sales) / new_sales_stage2
    pct_old_policy_stage2 = 1 - pct_new_policy_stage2
    new_avg_days_stage2 = pct_new_policy_stage2 * days_accept + pct_old_policy_stage2 * days_non_accept
    new_receivables_stage2 = (new_sales_stage2 * new_avg_days_stage2) / days_per_year
    capital_released_stage2 = old_receivables - new_receivables_stage2
    profit_release_stage2 = capital_released_stage2 * wacc
    profit_extra_stage2 = extra_sales * gross_margin
    discount_cost_stage2 = new_sales_stage2 * pct_new_policy_stage2 * discount_rate
    total_profit_stage2 = profit_extra_stage2 + profit_release_stage2 - discount_cost_stage2
    npv_stage2 = total_profit_stage2 / (1 + wacc)

    return {
        "stage1": {
            "new_sales": new_sales_stage1,
            "pct_new_policy": pct_new_policy_stage1,
            "pct_old_policy": pct_old_policy_stage1,
            "new_avg_days": new_avg_days_stage1,
            "old_receivables": old_receivables,
            "new_receivables": new_receivables_stage1,
            "capital_released": capital_released_stage1,
            "profit_release": profit_release_stage1,
            "discount_cost": discount_cost_stage1,
            "profit_extra": profit_extra_stage1,
            "total_profit": total_profit_stage1,
            "npv": npv_stage1,
        },
        "stage2": {
            "new_sales": new_sales_stage2,
            "pct_new_policy": pct_new_policy_stage2,
            "pct_old_policy": pct_old_policy_stage2,
            "new_avg_days": new_avg_days_stage2,
            "old_receivables": old_receivables,
            "new_receivables": new_receivables_stage2,
            "capital_released": capital_released_stage2,
            "profit_release": profit_release_stage2,
            "discount_cost": discount_cost_stage2,
            "profit_extra": profit_extra_stage2,
            "total_profit": total_profit_stage2,
            "npv": npv_stage2,
        }
    }


def plot_results(results):
    # Βασικά μεγέθη για σύγκριση
    labels = ['NPV', 'Κέρδος Αποδέσμευσης', 'Κόστος Έκπτωσης', 'Κέρδος Επιπλέον Πωλήσεων']
    stage1_vals = [
        results['stage1']['npv'],
        results['stage1']['profit_release'],
        results['stage1']['discount_cost'],
        results['stage1']['profit_extra']
    ]
    stage2_vals = [
        results['stage2']['npv'],
        results['stage2']['profit_release'],
        results['stage2']['discount_cost'],
        results['stage2']['profit_extra']
    ]

    x = range(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x, stage1_vals, width, label='Μόνο Έκπτωση')
    ax.bar([p + width for p in x], stage2_vals, width, label='Έκπτωση + Επιπλέον Πωλήσεις')

    ax.set_ylabel('€')
    ax.set_title('Σύγκριση Μεγεθών ανά Στάδιο')
    ax.set_xticks([p + width/2 for p in x])
    ax.set_xticklabels(labels)
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)


def main():
    st.title("Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς")

    # Inputs
    current_sales = st.number_input("Τρέχουσες πωλήσεις (€)", value=1000.0, step=50.0)
    extra_sales = st.number_input("Επιπλέον πωλήσεις λόγω έκπτωσης (€)", value=250.0, step=10.0)
    discount_rate = st.number_input("Έκπτωση για πληρωμή τοις μετρητοίς (%)", value=2.0, min_value=0.0, max_value=100.0) / 100
    accept_rate = st.number_input("% πελατών που αποδέχεται την έκπτωση (%)", value=60.0, min_value=0.0, max_value=100.0) / 100
    days_accept = st.number_input("% πελατών που αποδέχεται πληρώνει σε (μέρες)", value=60, min_value=0)
    days_non_accept = st.number_input("% πελατών που δεν αποδέχεται πληρώνει σε (μέρες)", value=120, min_value=0)
    current_collection_days = st.number_input("Τρέχουσα μέση περίοδος είσπραξης (μέρες)", value=84, min_value=0)
    gross_margin = st.number_input("Μικτό περιθώριο κέρδους (σε %)", value=20.0, min_value=0.0, max_value=100.0) / 100
    wacc = st.number_input("Κόστος κεφαλαίου (WACC σε %)", value=20.0, min_value=0.0, max_value=100.0) / 100

    if st.button("Υπολόγισε"):
        results = cash_discount_analysis(
            current_sales, extra_sales, discount_rate,
            accept_rate, days_accept, days_non_accept,
            current_collection_days, gross_margin, wacc
        )

        st.subheader("Αποτελέσματα Σταδίου 1 - Μόνο Έκπτωση")
        for k, v in results["stage1"].items():
            st.write(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")

        st.subheader("Αποτελέσματα Σταδίου 2 - Έκπτωση + Επιπλέον Πωλήσεις")
        for k, v in results["stage2"].items():
            st.write(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")

        st.subheader("Σύγκριση Μεγεθών")
        plot_results(results)


if __name__ == "__main__":
    main()
