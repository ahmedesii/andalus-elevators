import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from io import BytesIO

# إعداد الصفحة
st.set_page_config(page_title="نظام مصاعد الأندلس - أحمد عيسى", layout="wide")

LOG_FILE = "andalus_log.xlsx"

# وظيفة لحفظ البيانات (داخل جلسة العمل)
if 'main_data' not in st.session_state:
    st.session_state.main_data = []

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

st.markdown(f"<h1>نظام الإشراف الفني - المهندس أحمد عيسى</h1>", unsafe_allow_html=True)

selected_school = st.selectbox("🏨 اختر الفرع:", list(school_data.keys()))
num_elevators = school_data[selected_school]["count"]
default_type = school_data[selected_school]["type"]

temp_list = []
tabs = st.tabs([f"🔹 مصعد {i+1}" for i in range(num_elevators)])

for i, tab in enumerate(tabs):
    with tab:
        col1, col2 = st.columns(2)
        with col1:
            status = st.selectbox("الحالة", ["✅ يعمل", "⚠️ عطل", "🛠️ صيانة"], key=f"s_{i}")
        with col2:
            tech = st.text_area("📝 ملاحظات فنية:", key=f"t_{i}")
        
        temp_list.append({
            "التاريخ": datetime.now().strftime("%Y-%m-%d"),
            "الفرع": selected_school,
            "المصعد": i+1,
            "الحالة": status,
            "الملاحظات": tech
        })

# زرار الحفظ والتحميل
st.divider()
if st.button("✅ اعتماد البيانات الحالية"):
    st.session_state.main_data.extend(temp_list)
    st.success("تم الحفظ في ذاكرة البرنامج المؤقتة")

if st.session_state.main_data:
    df_export = pd.DataFrame(st.session_state.main_data)
    
    # تحويل البيانات لملف اكسيل في الرامات (عشان يتحمل)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_export.to_excel(writer, index=False)
    
    st.download_button(
        label="📥 تحميل سجل الزيارات كملف Excel",
        data=output.getvalue(),
        file_name=f"Andalus_Report_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
