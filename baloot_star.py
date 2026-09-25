import streamlit as st
import random

# إعدادات الصفحة واسم اللعبة الجديد
st.set_page_config(page_title="بلوت النجمة المطور", page_icon="⭐", layout="centered")

st.title("⭐ بلوت النجمة المطور ⭐")
st.caption("نظام 40 كارت | الصن: 41 درجة | الحكم: 24 درجة | المكابرة بالأكبر")

# الأصناف الخمسة ورتب البلوت
SUITS = ['♠️', '♥️', '♦️', '♣️', '⭐']
RANKS = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def create_deck():
    return [f"{rank}{suit}" for suit in SUITS for rank in RANKS]

def card_value_sun(card):
    rank = card[:-1]
    suit = card[-1]
    if suit == '⭐':
        values = {'A': 22, '10': 20, 'K': 8, 'Q': 6, 'J': 4, '9': 5, '8': 5, '7': 5}
        return values.get(rank, 0)
    else:
        values = {'A': 11, '10': 10, 'K': 4, 'Q': 3, 'J': 2, '9': 0, '8': 0, '7': 0}
        return values.get(rank, 0)

# إدارة نظام التوزيع والدورة (3-2-2)
if 'deck' not in st.session_state or st.button("توزيع جولة جديدة 🃏"):
    deck = create_deck()
    random.shuffle(deck)
    
    # 7 كروت لكل لاعب
    st.session_state.player_hand = sorted([deck.pop() for _ in range(7)])
    st.session_state.p2_hand = [deck.pop() for _ in range(7)]
    st.session_state.p3_hand = [deck.pop() for _ in range(7)]
    st.session_state.p4_hand = [deck.pop() for _ in range(7)]
    
    # الكارت الثامن المكشوف
    st.session_state.up_card = deck.pop()
    st.session_state.remaining_deck = deck

st.divider()

# عرض كارت الشراء
st.subheader("📌 كارت الشراء الثامن (المكشوف):")
st.warning(f"## {st.session_state.up_card}")

if '⭐' in st.session_state.up_card:
    st.info("💡 تنبيه: لا يجوز الشراء 'حكم نجمة' لأن النجمة نقاطها ثابتة ومُدبلة ولا تكون حكماً.")

st.divider()

# عرض كروت اللاعب الـ 7
st.subheader("🃏 كروتك (7 كروت):")
cols = st.columns(7)
for i in range(7):
    with cols[i]:
        st.info(f"### {st.session_state.player_hand[i]}")

hand_points = sum(card_value_sun(c) for c in st.session_state.player_hand)
st.caption(f"📊 مجموع نقاط كروتك في الصن: **{hand_points} نقطة**")

st.divider()

# خيارات الشراء والمزايدة
st.subheader("📢 خيارات الشراء والمزايدة:")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("صن ☀️"):
        st.success("تم اختيار: صن | الحساب: 205 نقاط ÷ 5 = 41 درجة.")
with col2:
    is_star = '⭐' in st.session_state.up_card
    if st.button("حكم 👑", disabled=is_star):
        st.success("تم اختيار: حكم | الحساب: 237 نقطة ÷ 10 = 24 درجة.")
with col3:
    if st.button("بس (تمرير) ✋"):
        st.write("تم التمرير")

st.divider()

# قواعد المشاريع والمكابرة
st.subheader("🏆 قاعدة المكابرة والمشاريع:")
st.markdown("""
* **أولوية المشاريع:** المشاريع تُحسب **بالأكبر فقط** (500 > 400 > 200 > 100 > 50).
* **المكابرة بالنجمة:** تدخل أوراق النجمة ⭐ في المكابرة بالمشاريع، والمشروع الأكبر قيمة هو الذي ينزل ويُسجل للفريق.
* **عند التساوي:** ينزل المشروع الأكبر صاحب الأولوية وتُلغى مشاريع الخصم المنساوية أو الأصغر.
""")

st.divider()
st.success("🎉 أهلاً بك في ملف لعبة بلوت النجمة المطور الجديد!")
