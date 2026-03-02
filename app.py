import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

# إعدادات الصفحة بروح VANTROX
st.set_page_config(page_title="AUC English Club - Vantrox", page_icon="🚀", layout="centered")

DB_FILE = "auc_v2_data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame(columns=['Name', 'Days', 'Times'])
    return pd.DataFrame(columns=['Name', 'Days', 'Times'])

# CSS احترافي لإخفاء معالم المنصة
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stButton>button { 
        width: 100%; border-radius: 50px; 
        background: linear-gradient(45deg, #007bff, #00d4ff);
        color: white; height: 3.5em; font-weight: bold; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀دحيحة ال AUC")
st.write("أهلاً يا شباب.. بشمهندس جودة بيمسي، وعشان إنتم نايمين في مايه البطيخ، عملتلكم السيستم ده عشان ننجز ونظبط مواعيد الرومات")

# --- فورم التسجيل ---
with st.container():
    st.subheader("أنجز شويه علشان اخواتك مستعجلين😑")
    name = st.text_input("اسمك المنور (عشان نعرف مين اللي هيسحلنا معاه)")
    days = st.multiselect("اختار أكتر 3 أيام 'رايقين' معاك في الأسبوع", 
                        ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'],
                        max_selections=2)
    times = st.multiselect("(أفضل مواعيد (ماتختارش وقت الماتشات بالله عليك", 
                         ['6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'],
                         max_selections=2)
    
    if st.button("تأكيد وإرسال الاختيارات 🚀"):
        if name and len(days) == 2 and len(times) == 2:
            st.balloons()
            df = load_data()
            new_entry = {'Name': name, 'Days': ", ".join(days), 'Times': ", ".join(times)}
            updated_df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            updated_df.to_csv(DB_FILE, index=False)
            
            st.toast(f'عاش يا {name.split()[0]}.. تم الحفظ!', icon='🔥')
            st.success(f"وصل يا برنس! مواعيدك اتحفظت.")
            time.sleep(2)
            st.rerun()
        else:
            st.error(" ركز يا برنس.. محتاجين الاسم، و 3 أيام، وميعادين بالظبط!")

st.divider()

# --- لوحة التحكم (Admin Dashboard) ---
with st.expander("Admin Access (Mahmoud Only) 🤫"):
    password = st.text_input("كلمة السر", type="password")
    if password == "011405":
        data = load_data()
        # التأكد من وجود العمود الجديد لتجنب الـ KeyError
        if not data.empty and 'Days' in data.columns:
            st.subheader("📊 تحليل المواعيد")
            all_days = []
            for d in data['Days'].dropna():
                all_days.extend(d.split(", "))
            
            if all_days:
                day_counts = pd.Series(all_days).value_counts().reset_index()
                day_counts.columns = ['اليوم', 'عدد الطلاب']
                fig = px.bar(day_counts, x='اليوم', y='عدد الطلاب', color='عدد الطلاب', 
                             color_continuous_scale='Blues', text_auto=True)
                st.plotly_chart(fig, use_container_width=True)
            
            st.write("### قائمة المسجلين:")
            st.table(data)
            
            # حذف تسجيل
            name_to_delete = st.selectbox("حذف طالب:", ["اختار اسم..."] + data['Name'].unique().tolist())
            if st.button("حذف نهائي ❌"):
                if name_to_delete != "اختار اسم...":
                    new_df = data[data['Name'] != name_to_delete]
                    new_df.to_csv(DB_FILE, index=False)
                    st.rerun()
        else:
            st.info("قاعدة البيانات لسه فاضية أو محتاجة أول تسجيل بالنسخة الجديدة.")






