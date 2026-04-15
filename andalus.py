import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="نظام مصاعد الأندلس - أحمد عيسى", layout="wide")

# اسم ملف السجل
LOG_FILE = "andalus_log.xlsx"

# وظيفة الحفظ
def save_to_excel(new_data):
    df_new = pd.DataFrame(new_data)
    if not os.path.isfile(LOG_FILE):
        df_new.to_excel(LOG_FILE, index=False)
    else:
        df_old = pd.read_excel(LOG_FILE)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        df_combined.to_excel(LOG_FILE, index=False)

# بيانات المدارس
school_data = {
    "Hamdaniya 1": {"count": 2, "type": "assembly"},
    "Hamdaniya 2": {"count": 2, "type": "Alfa"},
    "Hamdaniya 3": {"count": 3, "type": "Schindler"},
    "Hamdaniya 4": {"count": 4, "type": "Alfa"},
    "Obhur 1": {"count": 4, "type": "Alfa fuji Shanjhai"},
    "Rawdhah 1": {"count": 4, "type": "Mitsubishi + Alfa"},
    "Rawdhah little andalus": {"count": 2, "type": "Sword"},
    "Manar 1": {"count": 4, "type": "Alfa"},
    "Fayhaa 1": {"count": 4, "type": "Alfa"},
    "Fayhaa 2": {"count": 4, "type": "Alfa"},
    "Zahraa": {"count": 1, "type": "Mitsubishi"},
    "Shatea International": {"count": 7, "type": "Alfa Asia"},
    "Shatea National (Mawheba)": {"count": 4, "type": "Alfa Asia"}
}

today = datetime.now().date()
tomorrow = today + timedelta(days=1)

# التنسيق
st.markdown("""
    <style>
    .stApp { background-color: #F0F7FF; }
    h1 { color: #004578; text-align: center; border-bottom: 2px solid #0078D4; }
    .stButton>button { background-color: #0078D4; color: white; border-radius: 10px; height: 3em; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"<h1>نظام الإشراف الفني - المهندس أحمد عيسى</h1>", unsafe_allow_html=True)

# السجل في الجنب
if os.path.exists(LOG_FILE):
    if st.sidebar.button("📂 فتح سجل الزيارات السابقة"):
        history = pd.read_excel(LOG_FILE)
        st.subheader("📜 أرشيف الزيارات")
        st.dataframe(history)

st.divider()

# اختيار الفرع
selected_school = st.selectbox("🏨 اختر الفرع:", list(school_data.keys()))
num_elevators = school_data[selected_school]["count"]
default_type = school_data[selected_school]["type"]

data_list = []
tabs = st.tabs([f"🔹 مصعد {i+1}" for i in range(num_elevators)])

for i, tab in enumerate(tabs):
    with tab:
        col1, col2, col3 = st.columns([2, 2, 1.5])
        with col1:
            status = st.selectbox("الحالة", ["✅ يعمل", "⚠️ عطل", "🛠️ صيانة"], key=f"s_{i}")
            v_date = st.date_input("موعد الزيارة القادم", value=today + timedelta(days=30), key=f"d_{i}")
        with col2:
            extra = st.text_area("🗒️ ملاحظات عامة:", key=f"e_{i}")
            tech = st.text_area("📝 ملاحظات فنية (أحمد عيسى):", key=f"t_{i}")
        with col3:
            img = st.file_uploader("📷 صورة", type=["jpg", "png", "jpeg"], key=f"i_{i}")
            if img: st.image(Image.open(img), use_container_width=True)

        data_list.append({
            "تاريخ التسجيل": datetime.now().strftime("%Y-%m-%d"),
            "المشرف": "أحمد عيسى",
            "الفرع": selected_school,
            "المصعد": i+1,
            "الحالة": status,
            "ملاحظات فنية": tech,
            "الزيارة القادمة": str(v_date)
        })

if st.button("💾 اعتماد وحفظ الزيارة في ملف الاكسيل"):
    save_to_excel(data_list)
    st.success(f"✅ تم الحفظ في ملف {LOG_FILE}")
    st.balloons()