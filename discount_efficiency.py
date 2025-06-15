import streamlit as st

# ---- Βοηθητικές συναρτήσεις για μορφοποίηση ----
def format_number_gr(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(x):
    return f"{x * 100:.2f}%".replace(".", ",")

# ---- Πυρήνας υπολογισμού ----
def calculate_discount_efficiency(
    total_sales,
    discount_rate,
    acceptance_rate,
    days_reduction,
    annual_discount_rate
):
    """
    Υπολογίζει:
    - NPV απόδοσης έκπτωσης τοις μετρητοίς
    - Μέγιστο ποσοστό έκπτωσης που συμφέρει (Dmax)
    """
    if total_sales == 0 or acceptance_rate == 0 or days_reduction == 0 or annual_discount_rate == 0:
        return 0.0, 0.0

    accepted_sales = total_sales * acceptance_rate

    daily_rate = annual_discount_rate / 365
    benefit = accepted_sales * daily_rate * days_reduction
    discount_cost = accepted_sales * discount_rate
    npv_gain = benefit - discount_cost

    dmax = daily_rate * days_reduction

    return dmax, npv_gain

# ---- UI με Streamlit ----
def show_dmax_calculator():
    st.title("💸 Ανάλυση Απόδοσης Έκπτωσης Τοις Μετρητοίς")

    st.markdown(
        "Υπολογίστε αν συμφέρει να προσφέρετε έκπτωση για άμεση πληρωμή, "
        "με βάση την εξοικονόμηση από την ταχύτερη είσπραξη και το κόστος κεφαλαίου."
    )

    col1, col2 = st.columns(2)

    with col1:
        total_sales = st.number_input(
            "Επιπλέον Πωλήσεις που Αναμένονται (€)", min_value=0.0, value=10000.0, format="%.2f"
        )
        discount_rate = st.number_input(
            "Ποσοστό Έκπτωσης (%)", min_value=0.0, max_value=100.0, value=2.0, format="%.2f"
        ) / 100
        acceptance_rate = st.number_input(
            "Ποσοστό Πελατών που Αποδέχονται την Έκπτωση (%)", min_value=0.0, max_value=100.0, value=50.0, format="%.2f"
        ) / 100

    with col2:
        days_reduction = st.number_input(
            "Μείωση Ημερών Είσπραξης", min_value=0.0, value=15.0, format="%.1f"
        )
        annual_discount_rate = st.number_input(
            "Ετήσιο Κόστος Κεφαλαίου (%)", min_value=0.0, max_value=100.0, value=10.0, format="%.2f"
        ) / 100

    if st.button("Υπολογισμός Απόδοσης"):
        dmax, npv_gain = calculate_discount_efficiency(
            total_sales,
            discount_rate,
            acceptance_rate,
            days_reduction,
            annual_discount_rate
        )

        st.success("Αποτελέσματα:")
        st.metric("📈 Μέγιστο Ποσοστό Έκπτωσης που Συμφέρει (Dmax)", format_percentage_gr(dmax))
        st.metric("💰 Καθαρό Όφελος (NPV) από την Έκπτωση", format_number_gr(npv_gain) + " €")

if __name__ == "__main__":
    show_dmax_calculator()
