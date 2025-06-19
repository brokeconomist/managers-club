def show_gross_profit_template():
    st.title("Test Input")

    τιμη = st.number_input("Δώσε τιμή", value=10)
    st.write(f"Η τιμή που έδωσες είναι: {τιμη}")
