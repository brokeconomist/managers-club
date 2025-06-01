import streamlit as st

from home import show_home
from break_even_calculator import show_break_even_calculator
from break_even_shift_calculator import show_break_even_shift_calculator
from clv_calculator import show_clv_calculator
from substitution_analysis import show_substitution_analysis
from complementary_analysis import show_complementary_analysis
from loss_threshold import show_loss_threshold_before_price_cut
from discount_cash_tool import show_discount_cash_tool   # νέο import

st.set_page_config(page_title="Managers’ Club", page_icon="📊", layout="centered")

st.sidebar.title("📊 Managers’ Club - Επιλογή Εργαλείου")

tool = st.sidebar.radio("🧰 Επιλέξτε εργαλείο", [
    "🏠 Αρχική",
    "🟢 Νεκρό Σημείο (Break-Even)",
    "⚙️ Αλλαγή Νεκρού Σημείου (Τιμή / Κόστος / Επένδυση)",
    "👥 CLV - Αξία Πελάτη",
    "🔄 Ανάλυση Υποκατάστασης Προϊόντων",
    "➕ Ανάλυση Συμπληρωματικών Προϊόντων",
    "📉 Όριο Απώλειας Πωλήσεων πριν τη Μείωση Τιμών",
    "💸 Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς"  # νέα επιλογή
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
elif tool == "💸 Αποδοτικότητα Έκπτωσης Τοις Μετρητοίς":
    show_discount_cash_tool()
