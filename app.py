import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة الاحترافية
st.set_config = st.set_page_config(page_title="AUC English Club - Vantrox Edition", page_icon="😎", layout="centered")

# حتة الصياعة: إخفاء أي أثر لـ Streamlit
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
    /* تحسين العرض على الموبايل */
    @media (max-width: 600px) {
        .reportview-container { padding-top: 0px; }
    }
    </style>
    """, unsafe_allow_html=True)

# الهيدر بلمسة Vantrox
st.title("🚀 دحيحة الأنجليزي في ال AUC")
st.write("أهلاً يا شباب.. محمود جودة بيمسي، وعشان إنتم نايمين في مايه البطيخ، عملتلكم السيستم ده عشان ننجز ونظبط مواعيد الرومات.")

# قاعدة بيانات مؤقتة (Session State)
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Name', 'Day', 'Time'])

# --- فورم التسجيل (User Interface) ---
with st.container():
    st.subheader("سجل حضورك  👇")
    name = st.text_input("اسمك المنور (عشان نعرف مين اللي هيسحلنا معاه)")
    
    days = st.multiselect("اختار أكتر يومين 'رايقين' معاك في الأسبوع", 
                        ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'],
                        max_selections=2)
    
    times = st.multiselect("أفضل مواعيد (ماتختارش وقت الماتشات بالله عليك)", 
                         ['6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'])
    
    # الزرار الاحترافي
    if st.button("تأكيد وإرسال الاختيارات 🚀"):
        if name and len(days) == 2 and times:
            for day in days:
                for time in times:
                    new_entry = {'Name': name, 'Day': day, 'Time': time}
                    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_entry])], ignore_index=True)
            st.success(f"وصل يا {name.split()[0]}! استنى بقى لما أشوف باقي الشلة ونقرر.")
            st.balloons()
        else:
            st.error("يا أستاذ/أستاذه ركزو.. محتاجين اسمك ويومين بالظبط!")

st.divider()

# --- لوحة تحكم المهندس (Admin Dashboard) ---
with st.expander("Admin Access (Mahmoud Only) 🤫"):
    password = st.text_input("كلمة السر", type="password")
    if password == "011405":
        st.header("📊 تحليلات البيانات - VANTROX")
        if not st.session_state.data.empty:
            # Chart الأيام
            fig_days = px.bar(st.session_state.data['Day'].value_counts().reset_index(), 
                             x='Day', y='count', title="أكتر أيام مطلوبة", color_discrete_sequence=['#007bff'])
            st.plotly_chart(fig_days, use_container_width=True)
            
            # Heatmap المواعيد
            st.write("### مصفوفة المواعيد (Heatmap)")
            pivot_df = st.session_state.data.pivot_table(index='Time', columns='Day', aggfunc='size', fill_value=0)
            st.dataframe(pivot_df, use_container_width=True)
        else:
            st.info("لسه مفيش داتا دخلت يا هندسة.")
