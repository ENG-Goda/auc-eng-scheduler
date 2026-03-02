import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# إعدادات الصفحة الاحترافية - VANTROX Edition
st.set_page_config(page_title="AUC English Club - Vantrox", page_icon="😎", layout="centered")

# الربط بجوجل شيت (قاعدة البيانات)
conn = st.connection("gsheets", type=GSheetsConnection)

# دالة لجلب البيانات وتحديثها فوراً
def get_data():
    return conn.read(ttl=0)

# إخفاء معالم المنصة عشان البراندينج بتاع Vantrox
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button { 
        width: 100%; 
        border-radius: 25px; 
        background-color: #007bff; 
        color: white;
        height: 3em;
        font-weight: bold;
        border: none;
    }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# الهيدر بلمستك الخاصة
st.title("🚀 دحيحة الأنجليزي في ال AUC")
st.write("أهلاً يا شباب.. محمود جودة بيمسي، وعشان إنتم نايمين في مايه البطيخ، عملتلكم السيستم ده عشان ننجز ونظبط مواعيد الرومات.")

# --- فورم التسجيل (User Interface) ---
with st.container():
    st.subheader("سجل حضورك يا بطل 👇")
    name = st.text_input("اسمك المنور (عشان نعرف مين اللي هيسحلنا معاه)")
    
    days = st.multiselect("اختار أكتر يومين 'رايقين' معاك في الأسبوع", 
                        ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'],
                        max_selections=2)
    
    times = st.multiselect("أفضل مواعيد (ماتختارش وقت الماتشات بالله عليك)", 
                         ['6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'])
    
    if st.button("تأكيد وإرسال الاختيارات 🚀"):
        if name and len(days) == 2 and times:
            # 1. جلب البيانات القديمة
            existing_df = get_data()
            
            # 2. تجهيز الصفوف الجديدة
            new_entries = []
            for day in days:
                for time in times:
                    new_entries.append({"Name": name, "Day": day, "Time": time})
            
            new_df = pd.DataFrame(new_entries)
            
            # 3. دمج البيانات
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # 4. التحديث النهائي في جوجل شيت (السطر اللي طلبته يا هندسة)
            conn.update(worksheet="الورقة1", data=updated_df)
            
            st.success(f"وصل يا {name.split()[0]}! بياناتك اتحفظت في قاعدة بيانات VANTROX للأبد.")
            st.balloons()
        else:
            st.error("يا أستاذ/أستاذه ركزو.. محتاجين اسمك ويومين بالظبط!")

st.divider()

# --- لوحة تحكم المهندس (Admin Dashboard) ---
with st.expander("Admin Access (Mahmoud Only) 🤫"):
    password = st.text_input("كلمة السر", type="password")
    if password == "011405":
        st.header("📊 تحليلات البيانات - VANTROX")
        # قراءة البيانات لايف
        current_data = get_data()
        if not current_data.empty:
            # Chart الأيام
            fig_days = px.bar(current_data['Day'].value_counts().reset_index(), 
                             x='Day', y='count', title="أكتر أيام مطلوبة", color_discrete_sequence=['#007bff'])
            st.plotly_chart(fig_days, use_container_width=True)
            
            # عرض الجدول كامل
            st.write("### الأسماء والمواعيد المسجلة حالياً:")
            st.dataframe(current_data, use_container_width=True)
        else:
            st.info("قاعدة البيانات لسه فاضية يا هندسة.")
