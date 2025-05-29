import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Managers' Club", page_icon="📊", layout="centered")

### Βοηθητικές συναρτήσεις μορφοποίησης και parsing ###

def format_number_gr(num, decimals=2):
    """Μορφοποιεί αριθμό σε ελληνικό format '1.234,56'"""
    if num is None:
        return ""
    s = f"{num:,.{decimals}f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return s

def format_percentage_gr(number):
    """Μορφοποιεί αριθμό σε ποσοστό με δύο δεκαδικά σε ελληνική μορφή"""
    return f"{number:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")
    
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

def calculate_clv_detailed(
    years_retained,
    purchases_per_period,
    price_per_unit,
    cost_per_unit,
    marketing_cost_per_year,
    discount_rate
):
    gross_profit_per_period = purchases_per_period * (price_per_unit - cost_per_unit)

    # 1. Εκτιμώμενη συνολική αξία εισπράξεων
    total_value = (gross_profit_per_period * years_retained) - (marketing_cost_per_year * years_retained)

    # 2. Εκτιμώμενη καθαρή παρούσα αξία (NPV τύπου προσόδου)
    if discount_rate == 0:
        discounted_value = total_value  # Χωρίς προεξόφληση
    else:
        annuity_factor = (1 - (1 + discount_rate) ** (-years_retained)) / discount_rate
        discounted_value = (gross_profit_per_period - marketing_cost_per_year) * annuity_factor

    return total_value, discounted_value

def plot_clv_tornado_chart(
    years_retained,
    purchases_per_period,
    price_per_unit,
    cost_per_unit,
    marketing_cost,
    discount_rate
):
    _, base_clv = calculate_clv_detailed(
        years_retained,
        purchases_per_period,
        price_per_unit,
        cost_per_unit,
        marketing_cost,
        discount_rate
    )

    variations = {
        "Χρόνια Πελάτη +10%": (years_retained * 1.1, purchases_per_period, price_per_unit, cost_per_unit, marketing_cost, discount_rate),
        "Χρόνια Πελάτη -10%": (years_retained * 0.9, purchases_per_period, price_per_unit, cost_per_unit, marketing_cost, discount_rate),
        "Αγορές/Περίοδο +10%": (years_retained, purchases_per_period * 1.1, price_per_unit, cost_per_unit, marketing_cost, discount_rate),
        "Αγορές/Περίοδο -10%": (years_retained, purchases_per_period * 0.9, price_per_unit, cost_per_unit, marketing_cost, discount_rate),
        "Τιμή Πώλησης +10%": (years_retained, purchases_per_period, price_per_unit * 1.1, cost_per_unit, marketing_cost, discount_rate),
        "Τιμή Πώλησης -10%": (years_retained, purchases_per_period, price_per_unit * 0.9, cost_per_unit, marketing_cost, discount_rate),
        "Κόστος Μονάδας +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit * 1.1, marketing_cost, discount_rate),
        "Κόστος Μονάδας -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit * 0.9, marketing_cost, discount_rate),
        "Κόστος Μάρκετινγκ +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, marketing_cost * 1.1, discount_rate),
        "Κόστος Μάρκετινγκ -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, marketing_cost * 0.9, discount_rate),
        "Επιτόκιο +10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, marketing_cost, discount_rate * 1.1),
        "Επιτόκιο -10%": (years_retained, purchases_per_period, price_per_unit, cost_per_unit, marketing_cost, discount_rate * 0.9),
    }

    impacts = []
    labels = []

    for label, args in variations.items():
        try:
            _, new_clv = calculate_clv_detailed(*args)
            delta = new_clv - base_clv
            impacts.append(delta)
            labels.append(label)
        except:
            continue

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

def calculate_max_product_A_sales_drop(
    old_price,
    price_increase_absolute,  # σε ευρώ (π.χ. 0.10)
    profit_A,
    profit_B,
    profit_C,
    profit_D,
    percent_B,  # π.χ. 0.40 για 40%
    percent_C,
    percent_D
):
    """
    Επιστρέφει το εκτιμώμενο μέγιστο % μείωσης των πωλήσεων του Προϊόντος Α
    ώστε το συνολικό κέρδος να μην μειωθεί, με ακρίβεια ποσοστού (π.χ. -31.00).
    """
    # Κέρδος από υποκατάστατα
    benefit_substitutes = (
        percent_B * profit_B +
        percent_C * profit_C +
        percent_D * profit_D
    )

    denominator = ((profit_A - benefit_substitutes) / old_price) + price_increase_absolute
    numerator = -price_increase_absolute

    try:
        max_sales_drop_decimal = numerator / denominator
        max_sales_drop_percent = max_sales_drop_decimal * 100  # Μετατροπή σε ποσοστό
        return max_sales_drop_percent  # π.χ. -31.00
    except ZeroDivisionError:
        return None

def format_percentage_gr(number):
    """Μορφοποιεί αριθμό σε ποσοστό με δύο δεκαδικά σε ελληνική μορφή"""
    return f"{number:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")

def calculate_min_required_sales_increase(
    price_A,
    profit_A,
    profit_B,
    profit_C,
    price_change_pct,
    percent_B,
    percent_C
):
    percent_B = percent_B / 100
    percent_C = percent_C / 100
    price_change = price_A * price_change_pct / 100  # π.χ. -10% => -20€

    added_profit = profit_B * percent_B + profit_C * percent_C
    numerator = -price_change
    denominator = ((profit_A + added_profit) / price_A) + price_change_pct / 100

    try:
        result_pct = numerator / denominator * 100
        return result_pct
    except ZeroDivisionError:
        return None
        
def format_percentage_gr(number):
    """Μορφοποιεί αριθμό σε ποσοστό με δύο δεκαδικά σε ελληνική μορφή"""
    return f"{number:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")

def calculate_required_sales_increase(
    price_per_unit_A,
    profit_per_unit_A,
    profit_per_unit_B,
    profit_per_unit_C,
    percent_B,
    percent_C,
    price_reduction_pct  # σε μορφή ποσοστού π.χ. -10 για -10%
):
    """
    Υπολογίζει την ελάχιστη αύξηση πωλήσεων που απαιτείται μετά από μείωση τιμής
    ώστε να διατηρηθεί το ίδιο συνολικό κέρδος, λαμβάνοντας υπόψη τα συμπληρωματικά προϊόντα.
    """
    price_reduction = price_reduction_pct / 100  # μετατροπή σε δεκαδικό

    total_supplement_profit = (profit_per_unit_B * percent_B / 100) + (profit_per_unit_C * percent_C / 100)
    denominator = ((profit_per_unit_A + total_supplement_profit) / price_per_unit_A) + price_reduction

    if denominator == 0:
        return None

    required_sales_increase = -price_reduction / denominator
    return required_sales_increase * 100  # Επιστρέφεται ως ποσοστό

### UI ΣΥΝΑΡΤΗΣΕΙΣ ###

import streamlit as st
import streamlit.components.v1 as components

# ----- Page Config -----
st.set_page_config(
    page_title="Managers' Club",
    page_icon="📊",
    layout="wide",
)

# ----- Custom CSS -----
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .title-text {
        font-size: 36px;
        font-weight: 700;
        color: #1F4E79;
    }
    .subtitle-text {
        font-size: 18px;
        color: #444;
        margin-bottom: 20px;
    }
    .feature-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        height: 100%;
    }
    .footer {
        font-size: 14px;
        color: gray;
        margin-top: 40px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ----- Header -----
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://i.imgur.com/1A4dJ8U.png", width=120)  # Logo
with col2:
    st.markdown('<div class="title-text">Managers’ Club</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Έξυπνα εργαλεία για οικονομικές αποφάσεις σε μικρές επιχειρήσεις</div>', unsafe_allow_html=True)

st.markdown("---")

# ----- Call-to-Action -----
st.markdown("#### 🚀 Ξεκίνα τώρα")
st.markdown("Χρησιμοποίησε τα εργαλεία για να βρεις το break-even σημείο, να αναλύσεις την αξία πελατών ή να δεις την επίδραση τιμής στις πωλήσεις.")
cta = st.button("🔎 Μετάβαση στο Dashboard")

if cta:
    st.switch_page("pages/01_📈_Ανάλυση_Κερδοφορίας.py")  # προσαρμόστε το όνομα σελίδας

# ----- Χαρακτηριστικά -----
st.markdown("### 🧰 Βασικά Εργαλεία")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="feature-card">📉 <b>Break-Even Analysis</b><br>Ανακάλυψε το ελάχιστο απαιτούμενο για να μη μπαίνεις μέσα.</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="feature-card">💰 <b>CLV Υπολογιστής</b><br>Δες πόσα αξίζει κάθε πελάτης σου πραγματικά.</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="feature-card">🔄 <b>Ανάλυση Υποκατάστασης</b><br>Μέτρησε την επίδραση αλλαγών τιμών σε άλλα προϊόντα.</div>', unsafe_allow_html=True)

st.markdown("")

# ----- Feedback Form -----
st.markdown("### 📬 Πες μας τη γνώμη σου")
components.iframe("https://tally.so/r/xyz123", height=300)  # βάλε το δικό σου feedback form

# ----- Footer -----
st.markdown('<div class="footer">© 2025 Managers’ Club | Developed with ❤️ using Streamlit</div>', unsafe_allow_html=True)

### ΒΑΣΙΚΕΣ ΕΙΣΟΔΟΙ ΚΑΙ ΥΠΟΛΟΓΙΣΜΟΙ ###

def show_break_even_calculator():
    st.title("Πόσο πρέπει να πουλήσω για να μη μπαίνω μέσα;")
    st.markdown("""
    Θέλετε να μάθετε πόσα **τεμάχια** ή ποιο **τζίρο** πρέπει να κάνετε για να καλύψετε τα έξοδά σας;

    👉 Αυτό το εργαλείο σάς δείχνει μια εκτίμηση του νεκρού σημείου – δηλαδή εκεί που **δεν** έχετε ούτε κέρδος ούτε ζημιά.

    Ιδανικό για: νέες επιχειρήσεις, νέες τιμολογήσεις, ή όταν ζυγίζετε αν «σας βγαίνει» μια προσπάθεια.
    """)
    # Είσοδοι ως ελληνικά μορφοποιημένα κείμενα
    price_input = st.text_input("Τιμή Πώλησης ανά Μονάδα (€):", value="10,00")
    variable_cost_input = st.text_input("Μεταβλητό Κόστος ανά Μονάδα (€):", value="6,00")
    fixed_costs_input = st.text_input("Πάγια Έξοδα (€):", value=format_number_gr(1000.00))

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

    plot_break_even(price, variable_cost, fixed_costs, be_units)

def show_break_even_shift_calculator():
    st.header("Ανάλυση Αλλαγής στο Νεκρό Σημείο με Νέα Τιμή / Κόστος / Επένδυση")
    st.title("Τι αλλάζει στο 'μηδέν' μου αν ανεβάσω τιμές ή επενδύσω;")
    st.markdown("""
    Σκεφτήκατε να ανεβάσετε τιμή; Ή να επενδύσετε σε κάτι νέο;

    👉 Αυτό το εργαλείο δείχνει μια εκτίμηση του πώς **αλλάζει** το νεκρό σας σημείο (σε τεμάχια και ευρώ) όταν:
    - Ανεβάζετε τιμή
    - Αλλάζει το κόστος
    - Ή κάνετε μια νέα επένδυση

    Ιδανικό για να πάρετε απόφαση αν «σας συμφέρει».
    """)
    old_price_input = st.text_input("Παλιότερη Τιμή Πώλησης (€):", value="10,00", key="old_price")
    new_price_input = st.text_input("Νέα Τιμή Πώλησης (€):", value="11,00", key="new_price")
    old_cost_input = st.text_input("Παλιό Κόστος Μονάδας (€):", value="6,00", key="old_cost")
    new_cost_input = st.text_input("Νέο Κόστος Μονάδας (€):", value="6,50", key="new_cost")
    investment_cost_input = st.text_input("Κόστος Επένδυσης (€):", value=format_number_gr(2000.00), key="investment_cost")
    units_sold_input = st.text_input("Πωλήσεις Μονάδων (τελευταία περίοδος):", value=format_number_gr(500, decimals=0), key="units_sold")
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

    st.success(f"Αλλαγή Νεκρού Σημείου (%): {format_percentage_gr(percent_change)}")
    st.success(f"Αλλαγή Νεκρού Σημείου (μονάδες): {format_number_gr(units_change, 0)} μονάδες")

def parse_gr_number(s):
    """Μετατρέπει αριθμό μορφής '1.234,56' σε float 1234.56"""
    if s is None or s.strip() == "":
        return None
    try:
        return float(s.replace('.', '').replace(',', '.'))
    except:
        return None

def show_clv_calculator():
    st.header("Υπολογιστής Αξίας Πελάτη (CLV)") 
    st.title("Πόσο αξίζει ένας πελάτης σας; 💰")
    st.markdown("""
    Θέλετε να μάθετε αν ένας πελάτης «βγάζει τα λεφτά του»; Αυτό το εργαλείο σάς δείχνει μια εκτίμηση του πόσα χρήματα κερδίζετε καθαρά από κάθε πελάτη δηλδή μετά τα έξοδα που κάνετε ειδικά για αυτόν.

    👉 Απλώς συμπληρώστε:
    - **Κάθε πότε αγοράζει**
    - **Πόσα καθαρά κερδίζετε ανά αγορά**
    - **Για πόσα χρόνια μένει**
    - **Πόσο σας κόστισε να τον αποκτήσετε**

    Και το εργαλείο θα σας δείξει:
    - Την **εκτιμώμενη συνολική αξία**
    - Την **καθαρή παρούσα αξία**
    - Η μεταβολή ποιών στοιχείων **επηρεάζει** περισσότερο τα δύο παραπάνω (Tornado Chart)
    """)
    years_retained_input = st.text_input("Χρόνια Διατήρησης Πελάτη:", value="5")
    purchases_per_period_input = st.text_input("Αγορές ανά Περίοδο:", value="12")
    price_per_unit_input = st.text_input("Τιμή Πώλησης ανά Μονάδα (€):", value="100,00")
    cost_per_unit_input = st.text_input("Κόστος Μονάδας (€):", value="60,00")
    marketing_cost_input = st.text_input("Ετήσιο Κόστος Μάρκετινγκ (€):", value="100,00")
    discount_rate_input = st.text_input("Ετήσιο Προεξοφλητικό Επιτόκιο (%):", value="10,00")

    try:
        years_retained = int(years_retained_input)
    except:
        st.warning("Εισάγετε έγκυρο ακέραιο αριθμό για τα χρόνια διατήρησης.")
        return

    purchases_per_period = parse_gr_number(purchases_per_period_input)
    price_per_unit = parse_gr_number(price_per_unit_input)
    cost_per_unit = parse_gr_number(cost_per_unit_input)
    marketing_cost = parse_gr_number(marketing_cost_input)
    discount_rate_pct = parse_gr_number(discount_rate_input)

    if None in (purchases_per_period, price_per_unit, cost_per_unit, marketing_cost, discount_rate_pct):
        st.warning("Παρακαλώ εισάγετε έγκυρους αριθμούς σε όλα τα πεδία.")
        return

    discount_rate = discount_rate_pct / 100

    total_value, discounted_value = calculate_clv_detailed(
        years_retained,
        purchases_per_period,
        price_per_unit,
        cost_per_unit,
        marketing_cost,
        discount_rate
    )

    st.success(f"Εκτιμώμενη Συνολική Αξία Εισπράξεων: {format_number_gr(total_value)} €")
    st.success(f"Εκτιμώμενη Καθαρή Παρούσα Αξία Εισπράξεων (CLV): {format_number_gr(discounted_value)} €")

    if st.checkbox("Εμφάνιση Tornado Chart Ανάλυσης Ευαισθησίας"):
        plot_clv_tornado_chart(
            years_retained,
            purchases_per_period,
            price_per_unit,
            cost_per_unit,
            marketing_cost,
            discount_rate
        )

def show_price_increase_scenario():
    st.header("📈 Εκτίμηση Αποδεκτής Μείωσης Πωλήσεων Προϊόντος Α μετά από Αύξηση Τιμής")
    st.title("Τι θα γίνει αν οι πελάτες προτιμήσουν άλλο προϊόν μου; 🔄")
    st.markdown("""
    Έχετε 2 προϊόντα και σκεφτήκατε να αυξήσετε την τιμή στο ένα;

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
elif menu == "Ανάλυση Συμπληρωματικών Προϊόντων":
    show_required_sales_increase_calculator()
elif menu == "Όριο Απώλειας Πωλήσεων πριν Μείωση Τιμής":
    show_loss_threshold_before_price_cut()
