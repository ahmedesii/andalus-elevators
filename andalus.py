import streamlit as st
import pandas as pd
from datetime import datetime
import time
from io import BytesIO

# 1. إعداد الصفحة والعنوان
st.set_page_config(page_title="نظام مصاعد الأندلس - المهندس أحمد عيسى", layout="wide")

# 2. قاعدة بيانات المدارس الشاملة (البيانات الفنية + شركاء الدعم)
school_data = {
    "Hamdaniya 1": {"count": 2, "type": "Assembly", "control": "Standard", "support": "Company A"},
    "Hamdaniya 2": {"count": 2, "type": "Alfa", "control": "Integrated", "support": "Company B"},
    "Hamdaniya 3": {"count": 3, "type": "Schindler", "control": "Schindler Control", "support": "Schindler Group"},
    "Hamdaniya 4": {"count": 4, "type": "Alfa", "control": "Standard", "support": "Company C"},
    "Obhur 1": {"count": 4, "type": "Alfa fuji Shanjhai", "control": "Fuji System", "support": "Partner X"},
    "Rawdhah 1": {"count": 4, "type": "Mitsubishi + Alfa", "control": "Mixed Systems", "support": "Mitsubishi Support"},
    "Rawdhah little andalus": {"count": 2, "type": "Sword", "control": "Standard", "support": "Company D"},
    "Manar 1": {"count": 4, "type": "Alfa", "control": "Standard", "support": "Company E"},
    "Fayhaa 1": {"count": 4, "type": "Alfa", "control": "Standard", "support": "Company F"},
    "Fayhaa 2": {"count": 4, "type": "Alfa", "control": "Standard", "support": "Company G"},
    "Zahraa": {"count": 1, "type": "Mitsubishi", "control": "Mitsubishi System", "support": "Local Partner"},
    "Shatea International": {"count": 7, "type": "Alfa Asia", "control": "Monarch/Vega", "support": "Asia Support"},
    "Shatea National (Mawheba)": {"count": 4, "type": "Alfa Asia", "control": "Monarch/Vega", "support": "Asia Support"}
}

# 3. واجهة البرنامج (App Header)
st.title("🏗️ نظام الإشراف الفني - المهندس أحمد عيسى")
st.markdown("---")

# 4. اختيار الفرع وعرض البيانات الفنية وموعد الزيارة
selected_school = st.selectbox("🏨 اختر فرع مدارس الأندلس:", list(school_data.keys()))

col_info1, col_info2, col_info3, col_info4 = st.columns(4)
with col_info1:
    st.metric("عدد المصاعد", school_data[selected_school]['count'])
with col_info2:
    st.info(f"**الماكينة:** {school_data[selected_school]['type']}")
with col_info3:
    st.warning(f"**الكنترول:** {school_data[selected_school]['control']}")
with col_info4:
    st.success(f"**شريك الدعم:** {school_data[selected_school]['support']}")

visit_time = datetime.now().strftime("%I:%M %p")
st.write(f"⏱️ **وقت الزيارة الحالي:** {visit_time}")

# 5. إدارة المخزن المؤقت للبيانات
if 'log_entries' not in st.session_state:
    st.session_state.log_entries = []

# 6. المربعات (Tabs) لتسجيل الزيارة والملاحظات الفنية
num_elevators = school_data[selected_school]["count"]
st.subheader(f"📍 تسجيل تقرير الزيارة لفرع: {selected_school}")
tabs = st.tabs([f"مصعد {i+1}" for i in range(num_elevators)])

current_entries = []

for i, tab in enumerate(tabs):
    with tab:
        col1, col2 = st.columns(2)
        with col1:
            status = st.radio(f"الحالة (مصعد {i+1})", ["✅ يعمل", "⚠️ عطل", "🛠️ صيانة"], key=f"s_{selected_school}_{i}")
        with col2:
            notes = st.text_area(f"ملاحظات فنية (مصعد {i+1}):", placeholder="اكتب التفاصيل الفنية هنا...", key=f"n_{selected_school}_{i}")
        
        current_entries.append({
            "التاريخ": datetime.now().strftime("%Y-%m-%d"),
            "الوقت": visit_time,
            "الفرع": selected_school,
            "رقم المصعد": i+1,
            "نوع الماكينة": school_data[selected_school]['type'],
            "نوع الكنترول": school_data[selected_school]['control'],
            "شريك الدعم": school_data[selected_school]['support'],
            "الحالة": status,
            "الملاحظات الفنية": notes
        })

# 7. الحفظ والإشعارات (Notification System)
st.divider()
if st.button("💾 حفظ وإرسال الإشعار"):
    st.session_state.log_entries.extend(current_entries)
    # محاكاة إشعار (Notification)
    with st.spinner('جاري معالجة البيانات وإرسال التنبيه...'):
        time.sleep(1)
        st.toast(f"تم تسجيل زيارة {selected_school} بنجاح!", icon='🚀')
        st.balloons()
    st.success(f"تم تحديث السجل ببيانات {num_elevators} مصاعد.")

# 8. عرض السجل وتحميل ملف الإكسيل الشامل
if st.session_state.log_entries:
    st.subheader("📋 سجل تقارير اليوم")
    df = pd.DataFrame(st.session_state.log_entries)
    st.dataframe(df, use_container_width=True)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    st.download_button(
        label="📥 تحميل التقرير النهائي (Excel)",
        data=output.getvalue(),
        file_name=f"Andalus_Technical_Report_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
