import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

# إعداد الصفحة
st.set_page_config(page_title="مدارس الأندلس - إدارة المصاعد", layout="wide")

# الربط مع جوجل شيت (للتخزين الدائم)
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏫 نظام إدارة صيانة مصاعد مدارس الأندلس")

# قائمة المدارس وتوزيع المصاعد
schools = {
    "الحمدانية 1": 2, "الحمدانية 2": 2, "الحمدانية 3": 3, "الحمدانية 4": 4,
    "أبحر 1": 4, "الروضة 1": 4, "روضة الأندلس الصغير": 2,
    "المنار 1": 4, "الفيحاء 1": 4, "الفيحاء 2": 4,
    "الزهراء": 1, "الشاطئ دولي": 7, "الشاطئ عام": 4
}

# القائمة الجانبية
school = st.sidebar.selectbox("اختر المدرسة", list(schools.keys()))
lift = st.sidebar.selectbox("اختر المصعد", [f"مصعد {i+1}" for i in range(schools[school])])

# إدخال البيانات الفنية
col1, col2 = st.columns(2)
with col1:
    status = st.selectbox("حالة المصعد الحالية", ["يعمل", "لا يعمل"])
    fault_desc = st.text_area("وصف العطل (مثل نقاط T1, T2...) أو الملاحظات")
with col2:
    service_date = st.date_input("تاريخ الفحص", value=date.today())
    parts = st.text_input("قطع الغيار المستخدمة")

# زر الحفظ المطور
if st.button("💾 حفظ التقرير في السجل العام"):
    new_data = pd.DataFrame([{
        "المدرسة": school, "المصعد": lift, "التاريخ": str(service_date),
        "الحالة": status, "الملاحظات": fault_desc, "قطع الغيار": parts
    }])
    
    try:
        # قراءة البيانات القديمة وإضافة الجديدة في Google Sheets
        existing_df = conn.read()
        updated_df = pd.concat([existing_df, new_data], ignore_index=True)
        conn.update(data=updated_df)
        st.success("✅ تم حفظ البيانات أونلاين بنجاح!")
    except:
        # في حال كانت أول مرة أو لم يتم الربط بعد
        st.warning("⚠️ تأكد من وضع رابط Google Sheet في إعدادات Secrets")

# عرض آخر 5 سجلات للإدارة
st.divider()
st.subheader("📜 آخر التقارير المسجلة")
try:
    df = conn.read()
    st.dataframe(df.tail(5), use_container_width=True)
except:
    st.info("لا توجد بيانات مسجلة حالياً.")
