import streamlit as st

# --- Data / Business Logic Functions ---

def calculate_break_even(fixed_costs, price_per_unit, variable_cost_per_unit):
    if price_per_unit <= variable_cost_per_unit:
        return None  # No break-even point if price <= variable cost
    return fixed_costs / (price_per_unit - variable_cost_per_unit)

def calculate_total_cost(fixed_costs, variable_cost_per_unit, units_sold):
    return fixed_costs + variable_cost_per_unit * units_sold

# --- UI Functions ---

def input_section():
    st.sidebar.header("Input Parameters")
    fixed_costs = st.sidebar.number_input("Fixed Costs (€)", min_value=0.0, value=1000.0, step=100.0)
    price_per_unit = st.sidebar.number_input("Price per Unit (€)", min_value=0.01, value=10.0, step=0.1)
    variable_cost_per_unit = st.sidebar.number_input("Variable Cost per Unit (€)", min_value=0.0, value=6.0, step=0.1)
    units_sold = st.sidebar.number_input("Units Sold", min_value=0, value=200, step=10)
    return fixed_costs, price_per_unit, variable_cost_per_unit, units_sold

def display_results(break_even_point, total_cost, revenue, profit):
    st.subheader("Results")
    if break_even_point is None:
        st.warning("Break-even point cannot be calculated because price per unit ≤ variable cost per unit.")
    else:
        st.write(f"**Break-even Point:** {break_even_point:.2f} units")
    st.write(f"**Total Cost:** €{total_cost:.2f}")
    st.write(f"**Total Revenue:** €{revenue:.2f}")
    st.write(f"**Profit:** €{profit:.2f}")

# --- Main App Function ---

def main():
    st.title("Managers' Club - Financial Decision Support")

    fixed_costs, price_per_unit, variable_cost_per_unit, units_sold = input_section()

    break_even_point = calculate_break_even(fixed_costs, price_per_unit, variable_cost_per_unit)
    total_cost = calculate_total_cost(fixed_costs, variable_cost_per_unit, units_sold)
    revenue = price_per_unit * units_sold
    profit = revenue - total_cost

    display_results(break_even_point, total_cost, revenue, profit)

if __name__ == "__main__":
    main()
