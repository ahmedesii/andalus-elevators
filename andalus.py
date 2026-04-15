import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# 1. إعداد الصفحة والعنوان
st.set_page_config(page_title="نظام مصاعد الأندلس", layout="wide")

# 2. تعريف بيانات المدارس والمصاعد (تأكد من وجود كل الفروع)
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

# 3. واجهة البرنامج
st.title("🏗️ نظام الإشراف الفني - المهندس أحمد عيسى")
st.write(f"تاريخ اليوم: {datetime.now().strftime('%Y-%m-%d')}")

# 4. اختيار الفرع
selected_school = st.selectbox("🏨 اختر فرع مدارس الأندلس:", list(school_data.keys()))
num_elevators = school_data[selected_school]["count"]

# 5. إنشاء المخزن المؤقت للبيانات
if 'log_entries' not in st.session_state:
    st.session_state.log_entries = []

# 6. توزيع المربعات (Tabs) حسب عدد المصاعد
st.subheader(f"تسجيل بيانات مصاعد فرع: {selected_school}")
tabs = st.tabs([f"مصعد {i+1}" for i in range(num_elevators)])

current_entries = []

for i, tab in enumerate(tabs):
    with tab:
        col1, col2 = st.columns(2)
        with col1:
            status = st.radio(f"حالة المصعد {i+1}", ["✅ يعمل", "⚠️ عطل", "🛠️ تحت الصيانة"], key=f"status_{selected_school}_{i}")
        with col2:
            notes = st.text_area(f"ملاحظات فنية للمصعد {i+1}:", placeholder="اكتب حالة المصعد أو الأعطال هنا...", key=f"notes_{selected_school}_{i}")
        
        current_entries.append({
            "التاريخ": datetime.now().strftime("%Y-%m-%d"),
            "الفرع": selected_school,
            "المصعد": i+1,
            "الحالة": status,
            "الملاحظات": notes
        })

# 7. أزرار الحفظ والتحميل
st.divider()
col_save, col_del = st.columns(2)

with col_save:
    if st.button("💾 حفظ الزيارات الحالية"):
        st.session_state.log_entries.extend(current_entries)
        st.success(f"تم حفظ بيانات {num_elevators} مصاعد بنجاح!")

with col_del:
    if st.button("🗑️ مسح السجل المؤقت"):
        st.session_state.log_entries = []
        st.warning("تم مسح السجل")

# 8. عرض السجل وإمكانية التحميل
if st.session_state.log_entries:
    st.subheader("📋 السجل الحالي (قبل التحميل)")
    df = pd.DataFrame(st.session_state.log_entries)
    st.dataframe(df, use_container_width=True)
    
    # تحويل لملف إكسيل للتحميل
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    st.download_button(
        label="📥 تحميل سجل الزيارات (Excel)",
        data=output.getvalue(),
        file_name=f"Andalus_Report_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
