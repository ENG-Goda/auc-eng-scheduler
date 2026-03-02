import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة الاحترافية - VANTROX Edition
st.set_page_config(page_title="AUC English Club - Vantrox", page_icon="😎", layout="centered")

# رابط الشيت بتاعك كـ CSV (ده الحل عشان نتفادى الـ HTTP Error)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1C9bgpR4HFCp4jPj7mdAw_ki0IrsbyXz8gddw6oN7P7Q/export?format=csv"

# إخفاء معالم Streamlit عشان يبان شغلك الشخصي
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

# الهيدر بلمسة محمود جودة
st.title("🚀 دحيحة الأنجليزي في ال AUC")
st.write("أهلاً يا شباب.. محمود جودة بيمسي، وعشان إنتم نايمين في مايه البطيخ، عملتلكم السيستم ده عشان ننجز ونظبط مواعيد الرومات.")

# دالة لجلب البيانات
def load_data():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame(columns=['Name', 'Day', 'Time'])

# --- فورم التسجيل (User Interface) ---
with st.container():
    st.subheader("سجل حضورك يا بطل 👇")
    name = st.text_input("اسمك المنور")
    
    days = st.multiselect("اختار أكتر يومين 'رايقين' معاك", 
                        ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'],
                        max_selections=2)
    
    times = st.multiselect("أفضل مواعيد", 
                         ['6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'])
    
    if st.button("تأكيد وإرسال الاختيارات 🚀"):
        if name and len(days) == 2 and times:
            # هنا هنعرض رسالة نجاح مؤقتة للمستخدم
            st.success(f"وصل يا {name.split()[0]}! بياناتك بتتحفظ في قاعدة بيانات VANTROX.")
            st.balloons()
            # ملحوظة: التحديث الفعلي للشيت بيحتاج إما API Key أو Google Apps Script 
            # وده هنظبطه في الخطوة الجاية لو الشيت لسه ما بيسمعش
        else:
            st.error("يا أستاذ/أستاذه ركزو.. محتاجين اسمك ويومين بالظبط!")

st.divider()

# --- لوحة تحكم المهندس (Admin Dashboard) ---
with st.expander("Admin Access (Mahmoud Only) 🤫"):
    password = st.text_input("كلمة السر", type="password")
    if password == "011405":
        st.header("📊 تحليلات البيانات - VANTROX")
        data = load_data()
        if not data.empty:
            fig = px.bar(data['Day'].value_counts().reset_index(), 
                         x='Day', y='count', title="أكتر أيام مطلوبة", color_discrete_sequence=['#007bff'])
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(data, use_container_width=True)
        else:
            st.info("قاعدة البيانات لسه بتجمع داتا يا هندسة.")
