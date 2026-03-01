import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة والبراندينج الخاص بـ VANTROX
st.set_page_config(page_title="AUC English Club - Vantrox Edition", page_icon="😎", layout="centered")

# CSS احترافي لضبط الاتجاه (RTL) وتنسيق الألوان
st.markdown("""
    <style>
    /* تنسيق الجسم الرئيسي والخطوط */
    .main { 
        background-color: #f5f7f9; 
        direction: rtl; 
        text-align: right; 
    }
    
    /* ضبط اتجاه النصوص والعناوين */
    h1, h2, h3, h4, h5, h6, p, span, label, div { 
        direction: rtl; 
        text-align: right; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* تنسيق الزرار عشان يبقى مالي الشاشة وشكله شيك */
    .stButton>button { 
        width: 100%; 
        border-radius: 20px; 
        background-color: #007bff; 
        color: white; 
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    
    /* لمسة جمالية للقوائم المنسدلة */
    .stMultiSelect div {
        direction: rtl;
    }
    </style>
    """, unsafe_allow_html=True)

# محاكاة لقاعدة البيانات (Session State)
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Name', 'Day', 'Time'])

# الواجهة الرئيسية
st.title("🚀 دحيحة AUC في الإنجليزي")
st.write("أهلاً يا شباب.. محمود جودة بيمسي، وعشان إحنا مهندسين مش بتوع ورق وقلم، عملتلكم السيستم ده على منصة **VANTROX** عشان ننجز ونظبط مواعيد الرومات.")

# --- فورم التسجيل ---
with st.container():
    with st.form("pro_form", clear_on_submit=True):
        st.subheader("سجل حضورك يا بطل 👇")
        
        name = st.text_input("اسمك المنور (عشان نعرف مين اللي هيسحلنا معاه)")
        
        days = st.multiselect("اختار أكتر يومين 'رايقين' معاك في الأسبوع", 
                            ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'],
                            max_selections=2)
        
        times = st.multiselect("أفضل مواعيد (ماتختارش وقت الماتشات بالله عليك)", 
                             ['6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'])
        
        submit = st.form_submit_button("إرسال الاختيارات 🚀")
        
        if submit:
            if name and len(days) == 2 and times:
                # إضافة البيانات للجدول
                for day in days:
                    for time in times:
                        new_row = pd.DataFrame([{'Name': name, 'Day': day, 'Time': time}])
                        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
                
                st.success(f"وصل يا {name.split()[0]}! استنى بقى لما أشوف باقي الشلة ونقرر.")
                st.balloons()
            else:
                st.error("يا هندسة ركز.. محتاجين اسمك ويومين بالظبط عشان السيستم يقبل!")

# --- لوحة تحكم محمود (الـ Admin) ---
st.sidebar.title("Area 51 (Top Secret) 🤫")
if st.sidebar.checkbox("أنا محمود جودة شخصياً"):
    pw = st.sidebar.text_input("باسورد المهندس", type="password")
    if pw == "Vantrox2026":
        st.header("📊 إحصائيات السهرة")
        
        if not st.session_state.data.empty:
            # Chart الأيام
            df_days = st.session_state.data['Day'].value_counts().reset_index()
            fig_days = px.bar(df_days, x='Day', y='count', title="أكتر الأيام المطلوبة", color_discrete_sequence=['#007bff'])
            st.plotly_chart(fig_days)
            
            # Heatmap المواعيد
            st.write("### مصفوفة المواعيد (الخلاصة)")
            pivot = st.session_state.data.pivot_table(index='Time', columns='Day', aggfunc='size', fill_value=0)
            st.dataframe(pivot.style.background_gradient(cmap='Blues'))
        else:
            st.info("لسه مفيش حد سجل.. أول ما يسجلوا الداتا هتظهرلك هنا.")
