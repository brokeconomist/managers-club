import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def format_number_gr(number, decimals=2):
    """Μορφοποιεί αριθμό σε ελληνικό format π.χ. '1.234,56'"""
    if number is None:
        return ""
    return f"{number:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(number):
    """Μορφοποιεί ποσοστά με ένα δεκαδικό και ελληνικό κόμμα"""
    if number is None:
        return ""
    return f"{number:,.1f}%".replace(".", ",")

### ΥΠΟΛΟΓΙΣΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ###

def calculate_break_even(price_per_unit, variable_cost, fixed_costs):
    if price_per_unit <= variable_cost:
        return None, None
    contribution_margin = price_per_unit - variable_cost
    break_even_units = fixed_costs / contribution_margin
    break_even_revenue = break_even_units * price_per_unit
    return break_even_units, break_even_revenue

def calculate_break_even_shift_v2(
    old_price, new_price,
    old_unit_cost, new_unit_cost,
    investment_cost, units_sold
):
    denominator = new_price - new_unit_cost
    if denominator == 0 or units_sold == 0:
        return None, None  # Αποφυγή διαίρεσης με 0

    percent_change = -((new_price - old_price) - (new_unit_cost - old_unit_cost)) / denominator \
                     + (investment_cost / (denominator * units_sold))

    units_change = ( -((new_price - old_price) - (new_unit_cost - old_unit_cost)) / denominator * units_sold ) \
                   + (investment_cost / denominator)

    return percent_change * 100, units_change  # Ποσοστό %

def calculate_custom_clv(
    years_retained,
    purchases_per_period,
    price_per_unit,
    cost_per_unit,
    annual_marketing_cost,
    discount_rate
):
    gross_profit = purchases_per_period * (price_per_unit - cost_per_unit)
    net_cash_flow = gross_profit - annual_marketing_cost
    clv = net_cash_flow / ((1 + discount_rate) ** years_retained)
    return clv

def plot_clv_tornado_chart(
    years_retained,
    purchases_per_period,
    price_per_unit,
    cost_per_unit,
    annual_marketing_cost,
    discount_rate
):
    base_clv = calculate_custom_clv(
        years_retained,
        purchases_per_period,
        price_per_unit,
        cost_per_unit,
        annual_marketing_cost,
        discount_rate
    )

    variations = {
        "Χρόνια Πελάτη +10%": (years_retained * 1.1, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Χρόνια Πελάτη -10%": (years_retained * 0.9, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Αγορές/Περίοδο +10%": (years_retained, purchases_per_period * 1.1, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Αγορές/Περίοδο -10%": (years_retained, purchases_per_period * 0.9, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate),
        "Τιμή Πώλησης +10%": (years_retained, purchases_per_period, price_per_unit * 1.1, cost_per_unit, annual_marketing_cost, discount_rate),
        "Τιμή Πώλησης -10%": (years_retained, purchases_per_period, price_per_unit * 0.9, cost_per_unit, annual_marketing_cost, discount_rate),
        "Κόστος Μονάδας +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit * 1.1, annual_marketing_cost, discount_rate),
        "Κόστος Μονάδας -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit * 0.9, annual_marketing_cost, discount_rate),
        "Κόστος Μάρκετινγκ +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost * 1.1, discount_rate),
        "Κόστος Μάρκετινγκ -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost * 0.9, discount_rate),
        "Επιτόκιο +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate * 1.1),
        "Επιτόκιο -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate * 0.9),
    }

    impacts = []
    labels = []

    for label, args in variations.items():
        new_clv = calculate_custom_clv(*args)
        delta = new_clv - base_clv
        impacts.append(delta)
        labels.append(label)

    colors = ['green' if x > 0 else 'red' for x in impacts]
    sorted_indices = np.argsort(np.abs(impacts))[::-1]
    sorted_impacts = np.array(impacts)[sorted_indices]
    sorted_labels = np.array(labels)[sorted_indices]
    sorted_colors = np.array(colors)[sorted_indices]

    fig, ax = plt.subplots()
    ax.barh(sorted_labels, sorted_impacts, color=sorted_colors)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlabel("Μεταβολή στην CLV (€)")
    ax.set_title("Tornado Chart Ευαισθησίας CLV")
    st.pyplot(fig)

def plot_break_even(price_per_unit, variable_cost, fixed_costs, break_even_units):
    units = list(range(0, int(break_even_units * 2) + 1))
    revenue = [price_per_unit * u for u in units]
    total_cost = [fixed_costs + variable_cost * u for u in units]
    fig, ax = plt.subplots()
    ax.plot(units, revenue, label="Έσοδα")
    ax.plot(units, total_cost, label="Συνολικό Κόστος")
    ax.axvline(break_even_units, color="red", linestyle="--", label="Νεκρό Σημείο")
    ax.set_xlabel("Μονάδες Πώλησης")
    ax.set_ylabel("€")
    ax.set_title("Break-Even Analysis")
    ax.legend()
    st.pyplot(fig)

def calculate_max_product_A_sales_drop(old_price, price_increase, profit_A, profit_B, profit_C, profit_D, percent_B, percent_C, percent_D):
    benefit_substitutes = (percent_B * profit_B + percent_C * profit_C + percent_D * profit_D)
    denominator = ((profit_A - benefit_substitutes) / old_price) + price_increase
    numerator = - price_increase
    try:
        max_sales_drop = numerator / denominator
        return max_sales_drop
    except ZeroDivisionError:
        return None

def format_number_gr(number):
    return f"{number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage_gr(number):
    return f"{number:,.1f}%".replace(".", ",")

### UI ΣΥΝΑΡΤΗΣΕΙΣ ###

def show_home():
    st.title("📊 Managers’ Club")
    st.markdown("""
    ### 💼 Ο οικονομικός βοηθός κάθε μικρομεσαίας επιχείρησης

    **Καλώς ήρθες!**

    Το **Managers’ Club** είναι μια online εφαρμογή που σε βοηθά να παίρνεις οικονομικές αποφάσεις χωρίς πολύπλοκα οικονομικά.

    > 🧮 Εδώ, τα οικονομικά είναι στα χέρια σου. Απλά, καθαρά, χρήσιμα.
    """)

    tab1, tab2, tab3 = st.tabs(["📊 Οικονομικά Εργαλεία", "📈 Σενάρια & Στρατηγικές", "💼 Πελάτες & Χρηματοδότηση"])

    with tab1:
        st.markdown("""
        - 📊 Υπολογισμός Νεκρού Σημείου (Break-Even)
        - 📦 Διαχείριση Αποθεμάτων (υπό υλοποίηση)
        - 📥 Διαχείριση Εισπρακτέων Λογαριασμών (υπό υλοποίηση)
        - 📤 Διαχείριση Πληρωτέων Λογαριασμών (υπό υλοποίηση)
        - ⚙️ Μέσο Κόστος Παραγωγής ανά Μονάδα σε Οχτάωρο και Υπερωρίες (υπό υλοποίηση)
        """)

    with tab2:
        st.markdown("""
        - 📈 Ανάλυση του Νεκρού Σημείου με Σενάρια Τιμής, Κόστους & Πάγιων
        - 📉 Αξιολόγηση Επιπτώσεων Επένδυσης σε Νέες Υπηρεσίες ή Προϊόντα
        """)

    with tab3:
        st.markdown("""
        - 💵 Ανάλυση Πελάτη & Διάρκειας Ζωής Πελάτη (CLV)
        - 📅 Εκτίμηση Χρηματοδοτικών Αναγκών
        """)

### ΒΑΣΙΚΕΣ ΕΙΣΟΔΟΙ ΚΑΙ ΥΠΟΛΟΓΙΣΜΟΙ ###

def show_break_even_calculator():
    st.header("Υπολογιστής Νεκρού Σημείου (Break-Even Point)")

    # Είσοδοι ως ελληνικά μορφοποιημένα κείμενα
    price_input = st.text_input("Τιμή Πώλησης ανά Μονάδα (€):", value="10,00")
    variable_cost_input = st.text_input("Μεταβλητό Κόστος ανά Μονάδα (€):", value="6,00")
    fixed_costs_input = st.text_input("Πάγια Έξοδα (€):", value="1000,00")

    price = parse_gr_number(price_input)
    variable_cost = parse_gr_number(variable_cost_input)
    fixed_costs = parse_gr_number(fixed_costs_input)

    if None in (price, variable_cost, fixed_costs):
        st.warning("Παρακαλώ εισάγετε έγκυρους αριθμούς σε όλα τα πεδία.")
        return

    be_units, be_revenue = calculate_break_even(price, variable_cost, fixed_costs)

    if be_units is None:
        st.error("Η Τιμή Πώλησης πρέπει να είναι μεγαλύτερη από το Μεταβλητό Κόστος.")
        return

    st.success(f"Νεκρό Σημείο σε Μονάδες: {format_number_gr(be_units, 0)} μονάδες")
    st.success(f"Νεκρό Σημείο σε Έσοδα: {format_number_gr(be_revenue)} €")

    plot_break_even(price, variable_cost, fixed_costs, be_units)

def show_break_even_shift_calculator():
    st.header("Ανάλυση Αλλαγής στο Νεκρό Σημείο με Νέα Τιμή / Κόστος / Επένδυση")

    old_price_input = st.text_input("Παλιότερη Τιμή Πώλησης (€):", value="10,00", key="old_price")
    new_price_input = st.text_input("Νέα Τιμή Πώλησης (€):", value="11,00", key="new_price")
    old_cost_input = st.text_input("Παλιό Κόστος Μονάδας (€):", value="6,00", key="old_cost")
    new_cost_input = st.text_input("Νέο Κόστος Μονάδας (€):", value="6,50", key="new_cost")
    investment_cost_input = st.text_input("Κόστος Επένδυσης (€):", value="2000,00", key="investment_cost")
    units_sold_input = st.text_input("Πωλήσεις Μονάδων (τελευταία περίοδος):", value="500", key="units_sold")

    old_price = parse_gr_number(old_price_input)
    new_price = parse_gr_number(new_price_input)
    old_cost = parse_gr_number(old_cost_input)
    new_cost = parse_gr_number(new_cost_input)
    investment_cost = parse_gr_number(investment_cost_input)
    units_sold = parse_gr_number(units_sold_input)

    if None in (old_price, new_price, old_cost, new_cost, investment_cost, units_sold):
        st.warning("Παρακαλώ εισάγετε έγκυρους αριθμούς σε όλα τα πεδία.")
        return

    percent_change, units_change = calculate_break_even_shift_v2(
        old_price, new_price, old_cost, new_cost, investment_cost, units_sold
    )

    if percent_change is None:
        st.error("Υπολογισμός αδύνατος με τα δοσμένα στοιχεία (διαίρεση με μηδέν).")
        return

    st.success(f"Αλλαγή Νεκρού Σημείου (%): {percent_change:.2f} %")
    st.success(f"Αλλαγή Νεκρού Σημείου (μονάδες): {format_number_gr(units_change, 0)} μονάδες")

def show_clv_calculator():
    st.header("Υπολογιστής Αξίας Πελάτη (Customer Lifetime Value - CLV)")

    years_retained_input = st.text_input("Χρόνια Διατήρησης Πελάτη:", value="5")
    purchases_per_period_input = st.text_input("Αγορές ανά Περίοδο:", value="12")
    price_per_unit_input = st.text_input("Τιμή Πώλησης ανά Μονάδα (€):", value="100,00")
    cost_per_unit_input = st.text_input("Κόστος Μονάδας (€):", value="60,00")
    annual_marketing_cost_input = st.text_input("Ετήσιο Κόστος Μάρκετινγκ (€):", value="50,00")
    discount_rate_input = st.text_input("Ετήσιο Προεξοφλητικό Επιτόκιο (%):", value="10,00")

    try:
        years_retained = int(years_retained_input)
    except:
        st.warning("Εισάγετε έγκυρο ακέραιο αριθμό για τα χρόνια διατήρησης.")
        return

    purchases_per_period = parse_gr_number(purchases_per_period_input)
    price_per_unit = parse_gr_number(price_per_unit_input)
    cost_per_unit = parse_gr_number(cost_per_unit_input)
    annual_marketing_cost = parse_gr_number(annual_marketing_cost_input)
    discount_rate_pct = parse_gr_number(discount_rate_input)

    if None in (purchases_per_period, price_per_unit, cost_per_unit, annual_marketing_cost, discount_rate_pct):
        st.warning("Παρακαλώ εισάγετε έγκυρους αριθμούς σε όλα τα πεδία.")
        return

    discount_rate = discount_rate_pct / 100

    clv = calculate_custom_clv(
        years_retained,
        purchases_per_period,
        price_per_unit,
        cost_per_unit,
        annual_marketing_cost,
        discount_rate
    )

    st.success(f"Υπολογιζόμενη Αξία Πελάτη (CLV): {format_number_gr(clv)} €")

    if st.checkbox("Εμφάνιση Tornado Chart Ανάλυσης Ευαισθησίας"):
        plot_clv_tornado_chart(
            years_retained,
            purchases_per_period,
            price_per_unit,
            cost_per_unit,
            annual_marketing_cost,
            discount_rate
        )

def show_price_increase_scenario():
    st.header("📈 Εκτίμηση Αποδεκτής Μείωσης Πωλήσεων Προϊόντος Α μετά από Αύξηση Τιμής")

    with st.form("price_increase_form"):
        col1, col2 = st.columns(2)

        with col1:
            old_price = st.number_input("Τιμή ανά κιλό Προϊόντος Α (€)", min_value=0.01, value=1.50, step=0.01)
            price_increase_pct = st.number_input("Αύξηση τιμής (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1) / 100
            profit_A = st.number_input("Κέρδος ανά μονάδα Προϊόντος Α (€)", min_value=0.0, value=0.30, step=0.01)

        with col2:
            profit_B = st.number_input("Κέρδος ανά μονάδα Προϊόντος Β (€)", min_value=0.0, value=0.20, step=0.01)
            profit_C = st.number_input("Κέρδος ανά μονάδα Προϊόντος Γ (€)", min_value=0.0, value=0.20, step=0.01)
            profit_D = st.number_input("Κέρδος ανά μονάδα Προϊόντος Δ (€)", min_value=0.0, value=0.05, step=0.01)

        percent_B = st.slider("Ποσοστό πελατών που θα αγοράσουν Προϊόν Β (%)", 0.0, 100.0, 45.0) / 100
        percent_C = st.slider("Ποσοστό πελατών που θα αγοράσουν Προϊόν Γ (%)", 0.0, 100.0, 20.0) / 100
        percent_D = st.slider("Ποσοστό πελατών που θα αγοράσουν Προϊόν Δ (%)", 0.0, 100.0, 5.0) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        total_substitute = percent_B + percent_C + percent_D
        if total_substitute > 1:
            st.error("❌ Το συνολικό ποσοστό πελατών που επιλέγουν άλλα προϊόντα δεν μπορεί να ξεπερνά το 100%.")
            return

        no_purchase = 1 - total_substitute

        result = calculate_max_product_A_sales_drop(
            old_price,
            price_increase_pct,
            profit_A,
            profit_B,
            profit_C,
            profit_D,
            percent_B,
            percent_C,
            percent_D
        )

        if result is None:
            st.error("❌ Αδυναμία υπολογισμού. Δοκίμασε άλλες τιμές.")
        else:
            st.success(f"✅ Μέγιστη αποδεκτή μείωση πωλήσεων Προϊόντος Α: {format_number_gr(result)}%")
            st.info(f"ℹ️ Ποσοστό πελατών που δεν θα αγοράσουν τίποτα: {format_percentage_gr(no_purchase * 100)}")

### MAIN MENU ###

menu = st.sidebar.radio("📊 Επιλογή Εργαλείου", (
    "Αρχική Σελίδα",
    "Υπολογιστής Νεκρού Σημείου",
    "Ανάλυση Αλλαγής Νεκρού Σημείου",
    "Υπολογιστής Αξίας Πελάτη (CLV)",
    "Ανάλυση Υποκατάστασης Προϊόντων"
))

if menu == "Αρχική Σελίδα":
    show_home()
elif menu == "Υπολογιστής Νεκρού Σημείου":
    show_break_even_calculator()
elif menu == "Ανάλυση Αλλαγής Νεκρού Σημείου":
    show_break_even_shift_calculator()
elif menu == "Υπολογιστής Αξίας Πελάτη (CLV)":
    show_clv_calculator()
elif menu == "Ανάλυση Υποκατάστασης Προϊόντων":
    show_price_increase_scenario()
