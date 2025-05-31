tool = st.sidebar.radio("🧰 Επιλέξτε εργαλείο", [
    "🏠 Αρχική",
    "🟢 Νεκρό Σημείο (Break-Even)",
    "⚙️ Αλλαγή Νεκρού Σημείου (Τιμή / Κόστος / Επένδυση)",
    "👥 CLV - Αξία Πελάτη",
    "🔄 Ανάλυση Υποκατάστασης Προϊόντων",
    "➕ Ανάλυση Συμπληρωματικών Προϊόντων",
    "📉 Όριο Απώλειας Πωλήσεων πριν τη Μείωση Τιμών"
])

if tool == "🏠 Αρχική":
    show_home()
elif tool == "🟢 Νεκρό Σημείο (Break-Even)":
    show_break_even_calculator()
elif tool == "⚙️ Αλλαγή Νεκρού Σημείου (Τιμή / Κόστος / Επένδυση)":
    show_break_even_shift_calculator()
elif tool == "👥 CLV - Αξία Πελάτη":
    show_clv_calculator()
elif tool == "🔄 Ανάλυση Υποκατάστασης Προϊόντων":
    show_substitution_analysis()
elif tool == "➕ Ανάλυση Συμπληρωματικών Προϊόντων":
    show_complementary_analysis()
elif tool == "📉 Όριο Απώλειας Πωλήσεων πριν τη Μείωση Τιμών":
    show_loss_threshold_before_price_cut()
