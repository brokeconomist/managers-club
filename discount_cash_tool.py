import numpy as np
import matplotlib.pyplot as plt

def calculate_cash_discount_analysis(
    initial_sales,
    new_sales,
    gross_margin,
    old_collection_days,
    new_collection_days,
    discount_rate,
    wacc
):
    # Κέρδος από επιπλέον πωλήσεις
    sales_increase = new_sales - initial_sales
    profit_from_extra_sales = sales_increase * gross_margin

    # Υπολογισμός απαιτήσεων (μεσοσταθμικά, 365 ημέρες)
    initial_receivables = (initial_sales * old_collection_days) / 365
    new_receivables = (new_sales * new_collection_days) / 365

    # Αποδέσμευση κεφαλαίων
    capital_release = initial_receivables - new_receivables
    profit_from_release = capital_release * wacc

    # Κόστος έκπτωσης
    discount_cost = new_sales * discount_rate

    # Συνολικό κέρδος
    total_profit = profit_from_extra_sales + profit_from_release - discount_cost

    # NPV
    npv = total_profit / (1 + wacc)

    results = {
        "Κέρδος από επιπλέον πωλήσεις": round(profit_from_extra_sales, 2),
        "Κέρδος αποδέσμευσης": round(profit_from_release, 2),
        "Κόστος έκπτωσης": round(discount_cost, 2),
        "Συνολικό κέρδος από την πρόταση": round(total_profit, 2),
        "NPV": round(npv, 2),
    }

    return results, profit_from_extra_sales, profit_from_release, new_sales, wacc


def find_max_discount_for_zero_npv(
    initial_sales,
    new_sales,
    gross_margin,
    old_collection_days,
    new_collection_days,
    wacc
):
    def npv_for_discount(d):
        results, _, _, _, _ = calculate_cash_discount_analysis(
            initial_sales,
            new_sales,
            gross_margin,
            old_collection_days,
            new_collection_days,
            d,
            wacc
        )
        return results["NPV"]

    # Δοκιμές για εύρος εκπτώσεων 0%–50%
    discounts = np.linspace(0, 0.5, 1000)
    npvs = [npv_for_discount(d) for d in discounts]

    # Εύρεση κοντινότερου στο 0
    npv_array = np.array(npvs)
    closest_index = (np.abs(npv_array - 0)).argmin()
    max_discount = discounts[closest_index]

    return round(max_discount * 100, 2), discounts, npvs


def find_optimal_discount(
    initial_sales,
    new_sales,
    gross_margin,
    old_collection_days,
    new_collection_days,
    wacc
):
    def npv_for_discount(d):
        results, _, _, _, _ = calculate_cash_discount_analysis(
            initial_sales,
            new_sales,
            gross_margin,
            old_collection_days,
            new_collection_days,
            d,
            wacc
        )
        return results["NPV"]

    discounts = np.linspace(0, 0.5, 1000)
    npvs = [npv_for_discount(d) for d in discounts]
    npv_array = np.array(npvs)
    optimal_index = npv_array.argmax()
    optimal_discount = discounts[optimal_index]

    return round(optimal_discount * 100, 2)


def plot_npv_vs_discount(discounts, npvs):
    plt.figure(figsize=(8, 5))
    plt.plot(discounts * 100, npvs, label="NPV")
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("Σχέση Έκπτωσης με NPV")
    plt.xlabel("Ποσοστό Έκπτωσης (%)")
    plt.ylabel("Καθαρή Παρούσα Αξία (NPV)")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
