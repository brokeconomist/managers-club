import streamlit as st

def calculate_unit_costs(
    sales_regular,
    sales_overtime,
    raw_material_cost,
    operating_cost_regular,
    operating_cost_overtime,
    labor_cost_regular,
    labor_cost_overtime,
):
    total_units = sales_regular + sales_overtime
    total_cost = (
        raw_material_cost +
        operating_cost_regular +
        operating_cost_overtime +
        labor_cost_regular +
        labor_cost_overtime
    )

    # Γενικό μέσο κόστος ανά μονάδα
    avg_cost_total = total_cost / total_units if total_units != 0 else 0

    # Μέσο κόστος στο οχτάωρο
    avg_cost_regular = (
        (labor_cost_regular / sales_regular) +
        (operating_cost_regular / sales_regular) +
        (raw_material_cost / total_units)
        if sales_regular != 0 else 0
    )

    # Μέσο κόστος στις υπερωρίες
    avg_cost_overtime = (
        (labor_cost_overtime / sales_overtime) +
        (operating_cost_overtime / sales_overtime) +
        (raw_material_cost / total_units)
        if sales_overtime != 0 else 0
    )

    return avg_cost_total, avg_cost_regular, avg_cost_overtime


def show_unit_cost_calculator():
    st.title("Υπολογισμός Μέσου Κόστους Ανά Μονάδα")

    st.header("Εισαγωγή Στοιχείων")

    sales_regular = st.number_input("Ημερήσιες πωλήσεις σε μονάδες (οχτάωρο)", value=1000)
    sales_overtime = st.number_input("Ημερήσιες πωλήσεις σε μονάδες (υπερωρίες)", value=100)
    raw_material_cost = st.number_input("Ημερήσιο κόστος πρώτων υλών", value=1500.0)
    operating_cost_regular = st.number_input("Λειτουργικό κόστος στο οχτάωρο", value=4000.0)
    operating_cost_overtime = st.number_input("Λειτουργικό κόστος υπερωρίας", value=400.0)
    labor_cost_regular = st.number_input("Εργατικό κόστος στο οχτάωρο", value=8000.0)
    labor_cost_overtime = st.number_input("Εργατικό κόστος υπερωρίας", value=1200.0)

    if st.button("Υπολογισμός"):
        avg_total, avg_regular, avg_overtime = calculate_unit_costs(
            sales_regular,
            sales_overtime,
            raw_material_cost,
            operating_cost_regular,
            operating_cost_overtime,
            labor_cost_regular,
            labor_cost_overtime
        )

        st.success("Αποτελέσματα Υπολογισμών")
        st.write(f"🔹 **Μέσο κόστος ανά μονάδα προϊόντος (γενικό):** {avg_total:.2f} €")
        st.write(f"🔹 **Μέσο κόστος ανά μονάδα στο οχτάωρο:** {avg_regular:.2f} €")
        st.write(f"🔹 **Μέσο κόστος ανά μονάδα στις υπερωρίες:** {avg_overtime:.2f} €")
