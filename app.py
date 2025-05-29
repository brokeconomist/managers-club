import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Managers' Club", page_icon="📊", layout="centered")

# --- Βοηθητικές συναρτήσεις μορφοποίησης αριθμών ---
def format_number_gr(x, decimals=2):
    if x is None:
        return "-"
    return f"{x:,.{decimals}f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def parse_gr_number(s):
    """Μετατρέπει μορφή '1.234,56' σε float 1234.56"""
    if s is None or s.strip() == "":
        return None
    try:
        return float(s.replace('.', '').replace(',', '.'))
    except:
        return None

def format_percentage_gr(x):
    return f"{x*100:,.2f}%".replace(',', 'X').replace('.', ',').replace('X', '.')

# --- Υπολογισμοί ---
def calculate_break_even(price, variable_cost, fixed_costs):
    margin = price - variable_cost
    if margin <= 0:
        return None, None
    units = fixed_costs / margin
    revenue = units * price
    return units, revenue

def calculate_break_even_shift_v2(old_price, new_price, old_cost, new_cost, investment_cost, units_sold):
    old_margin = old_price - old_cost
    new_margin = new_price - new_cost
    if old_margin <= 0 or new_margin <= 0:
        return None, None
    old_break_even_units = investment_cost / old_margin if old_margin != 0 else None
    new_break_even_units = investment_cost / new_margin if new_margin != 0 else None
    percent_change = (new_break_even_units - old_break_even_units) / old_break_even_units if old_break_even_units else None
    units_change = new_break_even_units - old_break_even_units if old_break_even_units else None
    return percent_change, units_change

def calculate_clv(years, purchases_per_year, margin_per_purchase, marketing_cost, discount_rate):
    total_gross = years * purchases_per_year * margin_per_purchase - marketing_cost * years
    if discount_rate == 0:
        total_net = total_gross
    else:
        annuity_factor = (1 - (1 + discount_rate) ** (-years)) / discount_rate
        total_net = ((purchases_per_year * margin_per_purchase) - marketing_cost) * annuity_factor
    return total_gross, total_net

def calculate_max_product_A_sales_drop(old_price, price_increase_absolute, profit_A, profit_B, profit_C, profit_D, percent_B, percent_C, percent_D):
    benefit_substitutes = percent_B * profit_B + percent_C * profit_C + percent_D * profit_D
    denominator = ((profit_A - benefit_substitutes) / old_price) + price_increase_absolute
    numerator = -price_increase_absolute
    try:
        max_sales_drop_decimal = numerator / denominator
        max_sales_drop_percent = max_sales_drop_decimal * 100
        return max_sales_drop_percent
    except ZeroDivisionError:
        return None

def calculate_min_required_sales_increase(price_A, profit_A, profit_B, profit_C, price_change_pct, percent_B, percent_C):
    percent_B = percent_B / 100
    percent_C = percent_C / 100
    price_change = price_A * price_change_pct / 100
    added_profit = profit_B * percent_B + profit_C * percent_C
    numerator = -price_change
    denominator = ((profit_A + added_profit) / price_A) + price_change_pct / 100
    try:
        result_pct = numerator / denominator * 100
        return result_pct
    except ZeroDivisionError:
        return None

def calculate_required_sales_increase(price_per_unit_A, profit_per_unit_A, profit_per_unit_B, profit_per_unit_C, percent_B, percent_C, price_reduction_pct):
    price_reduction = price_reduction_pct / 100
    total_supplement_profit = (profit_per_unit_B * percent_B / 100) + (profit_per_unit_C * percent_C / 100)
    denominator = ((profit_per_unit_A + total_supplement_profit) / price_per_unit_A) + price_reduction
    if denominator == 0:
        return None
    required_sales_increase = -price_reduction / denominator
    return required_sales_increase * 100

### UI ΣΥΝΑΡΤΗΣΕΙΣ ###

def show_home():
    st.title("📊 Managers’ Club")
    st.markdown("""
    ### 💼 Ο οικονομικός βοηθός κάθε μικρομεσαίας επιχείρησης

    **Καλώς ήρθες!**

    Το **Managers’ Club** είναι μια online εφαρμογή που σε βοηθά να παίρνεις οικονομικές αποφάσεις χωρίς πολύπλοκα οικονομικά.

    > 🧮 Εδώ, τα οικονομικά είναι στα χέρια σου. Απλά, καθαρά, χρήσιμα.
    """)

def show_break_even_calculator():
    st.title("Πόσο πρέπει να πουλήσω για να μη μπαίνω μέσα;")

    price_input = st.text_input("Τιμή Πώλησης ανά Μονάδα (€):", value="10,00")
    variable_cost_input = st.text_input("Μεταβλητό Κόστος ανά Μονάδα (€):", value="6,00")
    fixed_costs_input = st.text_input("Πάγια Έξοδα (€):", value="1.000,00")

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

    st.success("📊 Αποτελέσματα Νεκρού Σημείου")
    st.metric("🔢 Τεμάχια για κάλυψη κόστους", format_number_gr(be_units, 2))
    st.metric("💶 Τζίρος για κάλυψη κόστους", f"{format_number_gr(be_revenue)} €")

def show_break_even_shift_calculator():
    st.title("Ανάλυση Αλλαγής στο Νεκρό Σημείο με Νέα Τιμή / Κόστος / Επένδυση")

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
        st.error("Υπολογισμός αδύνατος με τα δοσμένα στοιχεία.")
        return

    st.success(f"Αλλαγή Νεκρού Σημείου (%): {format_percentage_gr(percent_change)}")
    st.success(f"Αλλαγή Νεκρού Σημείου (μονάδες): {format_number_gr(units_change, 0)} μονάδες")

def show_clv_calculator():
    st.title("Υπολογιστής Αξίας Πελάτη (CLV)")

    years_retained_input = st.text_input("Χρόνια Διατήρησης Πελάτη:", value="5", key="clv_years")
    purchase_frequency_input = st.text_input("Αγορές ανά Έτος:", value="3", key="clv_freq")
    avg_margin_input = st.text_input("Μέσο Κέρδος ανά Αγορά (€):", value="100,00", key="clv_margin")
    marketing_cost_input = st.text_input("Δαπάνες Μάρκετινγκ ανά Πελάτη (€):", value="50,00", key="clv_marketing")
    discount_rate_input = st.text_input("Επιτόκιο Προεξόφλησης (%):", value="10", key="clv_rate")

    years_retained = parse_gr_number(years_retained_input)
    purchase_frequency = parse_gr_number(purchase_frequency_input)
    avg_margin = parse_gr_number(avg_margin_input)
    marketing_cost = parse_gr_number(marketing_cost_input)
    discount_rate = parse_gr_number(discount_rate_input)

    if None in (years_retained, purchase_frequency, avg_margin, marketing_cost, discount_rate):
        st.warning("Παρακαλώ εισάγετε έγκυρους αριθμούς σε όλα τα πεδία.")
        return

    clv_gross, clv_net = calculate_clv(
        years_retained, purchase_frequency, avg_margin, marketing_cost, discount_rate/100
    )

    st.success(f"Εκτιμώμενη Συνολική Αξία Πελάτη: {format_number_gr(clv_gross)} €")
    st.success(f"Καθαρή Παρούσα Αξία (CLV): {format_number_gr(clv_net)} €")

def show_price_increase_scenario():
    st.header("📈 Εκτίμηση Αποδεκτής Μείωσης Πωλήσεων Προϊόντος Α μετά από Αύξηση Τιμής")
    st.title("Τι θα γίνει αν οι πελάτες προτιμήσουν άλλο προϊόν μου; 🔄")
    st.markdown("""
    Έχετε 2 προϊόντα και σκεφτήκατε να αλλάξετε τιμή στο ένα;

    👉 Αυτό το εργαλείο σάς δείχνει με βάση το ποσοστό των πελατών που εκτιμάτε ότι θα μετακινηθούν από το ένα στο άλλο
     πώς θα επηρεαστούν οι συνολικές σας πωλήσεις και τα έσοδα.

    Χρήσιμο όταν έχετε παρόμοια προϊόντα ή όταν σκέφτεστε προωθητικές ενέργειες.
    """)
    with st.form("price_increase_form"):
        col1, col2 = st.columns(2)

        with col1:
            old_price_input = st.text_input("Τιμή ανά μονάδα Προϊόντος Α (€)", value=format_number_gr(1.50))
            price_increase_input = st.text_input("Αύξηση τιμής (%)", value=format_number_gr(5.0))
            profit_A_input = st.text_input("Κέρδος ανά μονάδα Προϊόντος Α (€)", value=format_number_gr(0.30))

        with col2:
            profit_B_input = st.text_input("Κέρδος ανά μονάδα Προϊόντος Β (€)", value=format_number_gr(0.20))
            profit_C_input = st.text_input("Κέρδος ανά μονάδα Προϊόντος Γ (€)", value=format_number_gr(0.20))
            profit_D_input = st.text_input("Κέρδος ανά μονάδα Προϊόντος Δ (€)", value=format_number_gr(0.05))

        percent_B = st.slider("Ποσοστό πελατών που θα αγοράσουν Προϊόν Β (%)", 0.0, 100.0, 45.0) / 100
        percent_C = st.slider("Ποσοστό πελατών που θα αγοράσουν Προϊόν Γ (%)", 0.0, 100.0, 20.0) / 100
        percent_D = st.slider("Ποσοστό πελατών που θα αγοράσουν Προϊόν Δ (%)", 0.0, 100.0, 5.0) / 100

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        old_price = parse_gr_number(old_price_input)
        price_increase_pct = parse_gr_number(price_increase_input) / 100
        profit_A = parse_gr_number(profit_A_input)
        profit_B = parse_gr_number(profit_B_input)
        profit_C = parse_gr_number(profit_C_input)
        profit_D = parse_gr_number(profit_D_input)

        if None in (old_price, price_increase_pct, profit_A, profit_B, profit_C, profit_D):
            st.error("❌ Έλεγξε ότι όλα τα αριθμητικά πεδία είναι σωστά συμπληρωμένα.")
            return

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
            st.success(f"✅ Μέγιστη αποδεκτή μείωση πωλήσεων Προϊόντος Α: {format_percentage_gr(result)}")
            st.info(f"ℹ️ Ποσοστό πελατών που δεν θα αγοράσουν τίποτα: {format_percentage_gr(no_purchase * 100)}")

def show_required_sales_increase_calculator():
    st.header("📈 Ανάλυση Συμπληρωματικών Προϊόντων")
    st.title("Τι θα γίνει αν προτείνω δεύτερο προϊόν μαζί με το βασικό; 🔗")
    st.markdown("""
    Πουλάτε κάτι και θέλετε να κάνετε έκπτωση;

    👉 Αυτό το εργαλείο σάς δείχνει με βάση το ποσοστό των πελατών που εκτιμάτε ότι θα αγοράσουν και κάτι άλλο μαζί λόγω έκπτωσης:
    - Πώς θα επηρεαστεί το συνολικό σας κέρδος
    - Αν αξίζει να δώσετε προσφορά-πακέτο

    Τέλειο για upselling, bundles, ή έξυπνες προτάσεις πώλησης!
    """)
    with st.form("complementary_products_form"):
        col1, col2 = st.columns(2)

        with col1:
            price_A_input = st.text_input("Τιμή ανά μονάδα Προϊόντος Α (€)", value=format_number_gr(200.00))
            profit_A_input = st.text_input("Κέρδος ανά μονάδα Προϊόντος Α (€)", value=format_number_gr(100.00))
            profit_B_input = st.text_input("Κέρδος ανά μονάδα Προϊόντος Β (€)", value=format_number_gr(40.00))

        with col2:
            profit_C_input = st.text_input("Κέρδος ανά μονάδα Προϊόντος Γ (€)", value=format_number_gr(15.00))
            price_reduction_pct_input = st.text_input("Μείωση Τιμής Προϊόντος Α (%)", value=format_number_gr(-10.00))

        st.markdown("### 📊 Συμπεριφορές πελατών σε συμπληρωματικά προϊόντα λόγω έκπτωσης στο βασικό προϊόν")

        percent_B = st.slider("% Πελατών που αγοράζουν και Προϊόν Β", 0.0, 100.0, 50.0)
        percent_C = st.slider("% Πελατών που αγοράζουν και Προϊόν Γ", 0.0, 100.0, 30.0)

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        price_A = parse_gr_number(price_A_input)
        profit_A = parse_gr_number(profit_A_input)
        profit_B = parse_gr_number(profit_B_input)
        profit_C = parse_gr_number(profit_C_input)
        price_reduction_pct = parse_gr_number(price_reduction_pct_input)

        if None in (price_A, profit_A, profit_B, profit_C, price_reduction_pct):
            st.error("⚠️ Έλεγξε ότι όλα τα αριθμητικά πεδία είναι σωστά συμπληρωμένα.")
            return

        result = calculate_required_sales_increase(
            price_A,
            profit_A,
            profit_B,
            profit_C,
            percent_B,
            percent_C,
            price_reduction_pct
        )

        if result is None:
            st.error("⚠️ Δεν μπορεί να υπολογιστεί. Έλεγξε τις τιμές.")
        else:
            st.success(f"✅ Ελάχιστη Απαιτούμενη Αύξηση Πωλήσεων στο Προϊόν Α: {format_percentage_gr(result)}")

    # Κενός χώρος για οπτική συνέπεια
    st.markdown("---")
    st.markdown(" ")
    st.markdown(" ")

def calculate_sales_loss_threshold(
    competitor_old_price,
    competitor_new_price,
    our_price,
    unit_cost
):
    try:
        top = (competitor_new_price - competitor_old_price) / competitor_old_price
        bottom = (unit_cost - our_price) / our_price
        if bottom == 0:
            return None
        result = top / bottom
        return result * 100  # Ποσοστό
    except ZeroDivisionError:
        return None

def show_loss_threshold_before_price_cut():
    st.header("📉 Όριο Απώλειας Πωλήσεων πριν τη Μείωση Τιμών")
    st.title("Πόσες πωλήσεις μπορώ να χάσω πριν σκεφτώ μείωση τιμής; ⚖️")
    st.markdown("""
    Έριξαν την τιμή στο προϊόν οι ανταγωνιστές και σκέφτεστε να κάνετε το ίδιο;

    👉 Αυτό το εργαλείο σάς δείχνει μια εκτίμηση του **πόσες** πωλήσεις μπορείτε να χάσετε πριν αρχίσετε να σκέφτεστε τη **μείωση τιμής** του προϊόνος.

    """)
    with st.form("loss_threshold_form"):
        col1, col2 = st.columns(2)

        with col1:
            competitor_old_price_input = st.text_input("Αρχική τιμή ανταγωνιστή πριν την μείωση (€)", value=format_number_gr(8.0))
            our_price_input = st.text_input("Τιμή πώλησης προϊόντος (€)", value=format_number_gr(8.0))

        with col2:
            competitor_new_price_input = st.text_input("Νέα τιμή ανταγωνιστή μετά την μείωση (€)", value=format_number_gr(7.2))
            unit_cost_input = st.text_input("Κόστος ανά μονάδα προϊόντος (€)", value=format_number_gr(4.5))

        submitted = st.form_submit_button("Υπολογισμός")

    if submitted:
        competitor_old_price = parse_gr_number(competitor_old_price_input)
        competitor_new_price = parse_gr_number(competitor_new_price_input)
        our_price = parse_gr_number(our_price_input)
        unit_cost = parse_gr_number(unit_cost_input)

        if None in (competitor_old_price, competitor_new_price, our_price, unit_cost):
            st.error("⚠️ Έλεγξε ότι όλα τα αριθμητικά πεδία είναι σωστά συμπληρωμένα.")
            return

        result = calculate_sales_loss_threshold(
            competitor_old_price,
            competitor_new_price,
            our_price,
            unit_cost
        )

        if result is None:
            st.error("⚠️ Δεν μπορεί να υπολογιστεί. Έλεγξε τις τιμές.")
        else:
            st.success(f"✅ Μέγιστο % Πωλήσεων που μπορεί να χαθεί πριν μειωθεί η τιμή: {format_percentage_gr(result)}")

    # Οπτική συνέπεια
    st.markdown("---")
    st.markdown(" ")

### MAIN MENU ###

menu = st.sidebar.radio("📊 Επιλογή Εργαλείου", (
    "Αρχική Σελίδα",
    "Υπολογιστής Νεκρού Σημείου",
    "Ανάλυση Αλλαγής Νεκρού Σημείου",
    "Υπολογιστής Αξίας Πελάτη (CLV)",
    "Ανάλυση Υποκατάστασης Προϊόντων",
    "Ανάλυση Συμπληρωματικών Προϊόντων",
    "Όριο Απώλειας Πωλήσεων πριν Μείωση Τιμής"
))

def main():
    st.set_page_config(page_title="Managers’ Club", layout="wide")

    st.sidebar.title("Μενού")
    menu = st.sidebar.radio("Επιλέξτε Εργαλείο:", 
                            ("Αρχική", "Υπολογιστής Νεκρού Σημείου", "Ανάλυση Αλλαγής Νεκρού Σημείου", "Υπολογιστής CLV"))

    if menu == "Αρχική":
        show_home()
    elif menu == "Υπολογιστής Νεκρού Σημείου":
        show_break_even_calculator()
    elif menu == "Ανάλυση Αλλαγής Νεκρού Σημείου":
        show_break_even_shift_calculator()
    elif menu == "Υπολογιστής CLV":
        show_clv_calculator()
elif menu == "Ανάλυση Υποκατάστασης Προϊόντων":
    show_price_increase_scenario()
elif menu == "Ανάλυση Συμπληρωματικών Προϊόντων":
    show_required_sales_increase_calculator()
elif menu == "Όριο Απώλειας Πωλήσεων πριν Μείωση Τιμής":
    show_loss_threshold_before_price_cut()
if __name__ == "__main__":
    main()
