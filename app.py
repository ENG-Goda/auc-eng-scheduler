import streamlit as st
import pandas as pd
import plotly.express as px
import os

# إعدادات الصفحة - VANTROX Edition
st.set_page_config(page_title="AUC English Club - Vantrox", page_icon="😎", layout="centered")

# اسم ملف البيانات (بيتحفظ على السيرفر للأبد)
DB_FILE = "auc_data.csv"

# دالة لتحميل البيانات من الملف
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=['Name', 'Day', 'Time'])

# إخفاء معالم المنصة عشان البراندينج بتاعك
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

st.title("🚀 دحيحة الأنجليزي في ال AUC")
st.write("سجل مواعيدك وهتتحفظ في سيرفرات VANTROX فوراً.")

# --- فورم التسجيل ---
with st.form("registration_form", clear_on_submit=True):
    name = st.text_input("اسمك المنور")
    days = st.multiselect("اختار يومين", ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'], max_selections=2)
    times = st.multiselect("أفضل مواعيد", ['6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'])
    submit = st.form_submit_button("تأكيد وإرسال 🚀")

    if submit:
        if name and len(days) == 2 and times:
            df = load_data()
            new_entries = []
            for day in days:
                for time in times:
                    new_entries.append({"Name": name, "Day": day, "Time": time})
            
            # إضافة البيانات الجديدة وحفظها في الملف
            updated_df = pd.concat([df, pd.DataFrame(new_entries)], ignore_index=True)
            updated_df.to_csv(DB_FILE, index=False)
            
            st.success(f"تم الحفظ بنجاح يا {name}! نورت قاعدة البيانات.")
            st.balloons()
        else:
            st.error("كمل بياناتك (الاسم ويومين بالظبط)!")

st.divider()

# --- الجزء اللي أنت عاوزه (الـ Chart والنتائج) ---
with st.expander("لوحة التحكم (Admin Access) 🤫"):
    password = st.text_input("كلمة السر", type="password")
    if password == "011405":
        current_data = load_data()
        if not current_data.empty:
            st.subheader("📊 إحصائيات المواعيد الأكثر طلباً")
            
            # رسم التشارت (أهم جزء طلبته)
            fig = px.bar(current_data['Day'].value_counts().reset_index(), 
                         x='Day', y='count', 
                         labels={'count':'عدد الطلاب', 'Day':'اليوم'},
                         color_discrete_sequence=['#007bff'])
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("### الأسماء المسجلة:")
            st.dataframe(current_data, use_container_width=True)
            
            # زرار تحميل إكسيل لو احتجته
            csv = current_data.to_csv(index=False).encode('utf-8-sig')
            st.download_button("تحميل البيانات Excel", data=csv, file_name="AUC_Results.csv")
        else:
            st.info("لسه مفيش حد سجل بيانات.")
