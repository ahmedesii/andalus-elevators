import streamlit as st
import pandas as pd
from datetime import date, timedelta

# ===== إعداد الصفحة =====
st.set_page_config(page_title="ANDALUS SCHOOL", layout="wide")

# ===== عنوان البرنامج =====
st.title("🏫 ANDALUS SCHOOL - Elevator Management System")

# ===== المدارس =====
schools = {
    "Hamdaniya 1": 2,
    "Hamdaniya 2": 2,
    "Hamdaniya 3": 3,
    "Hamdaniya 4": 4,
    "Obhur 1": 4,
    "Rawdhah 1": 4,
    "Rawdhah little andalus": 2,
    "Manar 1": 4,
    "Fayhaa 1": 4,
    "Fayhaa 2": 4,
    "Zahraa": 1,
    "Shatea International": 7,
    "Shatea National": 4
}

support_companies = ["شركة 1", "شركة 2", "شركة 3", "شركة 4", "شركة 5"]

# ===== القائمة الجانبية =====
st.sidebar.title("🏫 المدارس")
school = st.sidebar.selectbox("اختار المدرسة", list(schools.keys()))

lifts = [f"{school} - Lift {i+1}" for i in range(schools[school])]
lift = st.sidebar.selectbox("اختار المصعد", lifts)

st.subheader(f"🛗 {lift}")

# ===== Tabs =====
tabs = st.tabs([
    "🟦 البيانات",
    "🟩 الحالة",
    "🟨 الصيانة",
    "🟥 الأعطال",
    "🟪 الصور",
    "🟫 Notes"
])

# ===== البيانات =====
with tabs[0]:
    etype = st.selectbox("نوع المصعد", ["Schindler","Otis","Kone","Other"])
    controller = st.text_input("نوع الكنترول")
    floors = st.number_input("عدد الأدوار",1,50)
    company = st.selectbox("شركة الدعم", support_companies)

# ===== الحالة =====
with tabs[1]:
    status = st.selectbox("حالة المصعد", ["يعمل","لا يعمل"])
    ups = st.selectbox("UPS", ["يعمل","لا يعمل"])
    wires = st.selectbox("حالة الوايرات", ["جيدة","متوسطة","سيئة"])
    light = st.selectbox("إضاءة الكابينة", ["جيدة","ضعيفة","لا تعمل"])
    power = st.selectbox("انقطاع الكهرباء", ["لا يوجد","متكرر"])

# ===== الصيانة =====
with tabs[2]:
    last_service = st.date_input("آخر صيانة", value=date.today())
    next_service = st.date_input("الصيانة القادمة")

    if next_service <= date.today() + timedelta(days=7):
        st.warning("⚠️ تنبيه: موعد الصيانة قريب!")

# ===== الأعطال =====
with tabs[3]:
    fault = st.text_area("وصف العطل")
    spare = st.text_input("قطع الغيار المستخدمة")
    fixed = st.selectbox("تم الإصلاح", ["نعم","لا"])
    fault_date = st.date_input("تاريخ العطل")

# ===== الصور =====
with tabs[4]:
    image = st.file_uploader("ارفع صورة العطل", type=["jpg","png"])

# ===== Notes =====
with tabs[5]:
    notes = st.text_area("ملاحظات عامة")

# ===== حفظ البيانات =====
if st.button("💾 حفظ البيانات"):
    data = {
        "School": school,
        "Lift": lift,
        "Type": etype,
        "Controller": controller,
        "Floors": floors,
        "Company": company,
        "Status": status,
        "UPS": ups,
        "Wires": wires,
        "Light": light,
        "Power": power,
        "Last Service": last_service,
        "Next Service": next_service,
        "Fault": fault,
        "Spare Parts": spare,
        "Fixed": fixed,
        "Fault Date": fault_date,
        "Notes": notes
    }

    df = pd.DataFrame([data])

    try:
        old = pd.read_csv("data.csv")
        df = pd.concat([old, df], ignore_index=True)
    except:
        pass

    df.to_csv("data.csv", index=False)

    st.success("✅ تم حفظ البيانات بنجاح")

# ===== عرض البيانات =====
st.subheader("📊 البيانات المسجلة")

try:
    df = pd.read_csv("data.csv")
    st.dataframe(df)
except:
    st.info("لا توجد بيانات حتى الآن")
