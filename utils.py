import streamlit as st
from break_even_calculator import show_break_even_calculator
from break_even_shift import show_break_even_shift_calculator
from clv_calculator import show_clv_calculator
from substitution import show_substitution_tool
from complementary import show_complementary_tool
from loss_threshold import show_loss_threshold_before_price_cut

st.set_page_config(page_title="Managers' Club", page_icon="📊", layout="centered")

st.sidebar.title("📊 Managers' Club")
tool = st.sidebar.radio("🧰 Επιλέξτε εργαλείο", [
    "🟢 Νεκρό Σημείο (Break-Even)",
    "⚙️ Αλλαγή Νεκρού Σημείου (Τιμή / Κόστος / Επένδυση)",
    "👥 CLV - Αξία Πελάτη",
    "🔄 Ανάλυση Υποκατάστασης Προϊόντος",
    "➕ Ανάλυση Συμπληρωματικών Προϊόντων",
    "📉 Όριο Απώλειας Πωλήσεων πριν Μείωση Τιμών"
])

if tool == "🟢 Νεκρό Σημείο (Break-Even)":
    show_break_even_calculator()
elif tool == "⚙️ Αλλαγή Νεκρού Σημείου (Τιμή / Κόστος / Επένδυση)":
    show_break_even_shift_calculator()
elif tool == "👥 CLV - Αξία Πελάτη":
    show_clv_calculator()
elif tool == "🔄 Ανάλυση Υποκατάστασης Προϊόντος":
    show_substitution_tool()
elif tool == "➕ Ανάλυση Συμπληρωματικών Προϊόντων":
    show_complementary_tool()
elif tool == "📉 Όριο Απώλειας Πωλήσεων πριν Μείωση Τιμών":
    show_loss_threshold_before_price_cut()
