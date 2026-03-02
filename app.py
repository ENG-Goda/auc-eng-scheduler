import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(page_title="AUC English Club - Vantrox", page_icon="😎")

# الربط بجوجل شيت
conn = st.connection("gsheets", type=GSheetsConnection)

# دالة لجلب البيانات وتحديثها
def get_data():
    return conn.read(worksheet="Sheet1", ttl=0) # ttl=0 عشان يقرأ الداتا الجديدة فوراً

# إخفاء معالم Streamlit
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

st.title("🚀 دحيحة الأنجليزي في ال AUC")
st.write("سجل مواعيدك وهتتحفظ في قاعدة بيانات VANTROX فوراً.")

# --- فورم التسجيل ---
name = st.text_input("اسمك المنور")
days = st.multiselect("اختار يومين", ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'], max_selections=2)
times = st.multiselect("أفضل مواعيد", ['6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'])

if st.button("تأكيد وإرسال الاختيارات 🚀"):
    if name and len(days) == 2 and times:
        # 1. جلب البيانات القديمة أولاً
        existing_df = get_data()
        
        # 2. تجهيز الصفوف الجديدة
        new_entries = []
        for day in days:
            for time in times:
                new_entries.append({"Name": name, "Day": day, "Time": time})
        
        new_df = pd.DataFrame(new_entries)
        
        # 3. دمج القديم والجديد
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        # 4. رفع الكل للشيت (ده الحل النهائي للتخزين)
        conn.update(worksheet="Sheet1", data=updated_df)
        
        st.success("تم الحفظ بنجاح! نورت قاعدة بياناتنا يا هندسة.")
        st.balloons()
    else:
        st.error("كمل بياناتك يا برنس.. محتاجين الاسم ويومين بالظبط!")

st.divider()

# --- لوحة تحكم محمود جودة ---
with st.expander("Admin Access (Mahmoud Only) 🤫"):
    password = st.text_input("كلمة السر", type="password")
    if password == "011405":
        # قراءة البيانات لايف من الشيت
        current_data = get_data()
        if not current_data.empty:
            st.write("إحصائيات المواعيد الحالية:")
            fig = px.bar(current_data['Day'].value_counts().reset_index(), x='Day', y='count', color_discrete_sequence=['#007bff'])
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(current_data) # عشان تشوف الأسماء بنفسك
        else:
            st.info("لسه مفيش حد سجل.")
