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

# CSS احترافي مطور لضمان وضوح الخط في السكرين شوت
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stButton>button { 
        width: 100%; border-radius: 50px; 
        background: linear-gradient(45deg, #007bff, #00d4ff);
        color: white; height: 3.5em; font-weight: bold; border: none;
    }
    .summary-box {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 25px;
        border: 2px solid #007bff;
        margin-top: 30px;
        color: #1a1a1a !important; /* لون خط أسود غامق جداً */
    }
    .summary-box h4, .summary-box p, .summary-box b {
        color: #1a1a1a !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀دحيحة ال AUC")
st.write("أهلاً يا شباب.. بشمهندس جودة بيمسي، وعشان إنتم نايمين في مايه البطيخ، عملتلكم السيستم ده عشان ننجز ونظبط مواعيد الرومات")

# --- فورم التسجيل ---
with st.container():
    st.subheader("أنجز شويه علشان اخواتك مستعجلين😑")
    name = st.text_input("اسمك المنور (عشان نعرف مين اللي هيسحلنا معاه)")
    days = st.multiselect("اختار أكتر يومين 'رايقين' معاك في الأسبوع", 
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
            st.error(" ركز يا برنس.. محتاجين الاسم، ويومين، وميعادين بالظبط!")

st.divider()

# --- لوحة التحكم (Admin Dashboard) ---
with st.expander("Admin Access (Mahmoud Only) 🤫"):
    password = st.text_input("كلمة السر", type="password")
    if password == "011405":
        data = load_data()
        if not data.empty and 'Days' in data.columns:
            
            st.subheader("📊 تحليل المواعيد التفصيلي")
            all_days = []
            for d in data['Days'].dropna():
                all_days.extend(d.split(", "))
            
            if all_days:
                day_counts = pd.Series(all_days).value_counts().reset_index()
                day_counts.columns = ['اليوم', 'عدد الطلاب']
                fig = px.bar(day_counts, x='اليوم', y='عدد الطلاب', color='عدد الطلاب', 
                             color_continuous_scale='Blues', text_auto=True)
                
                fig.update_yaxes(tickformat=',d') # أرقام صحيحة
                st.plotly_chart(fig, use_container_width=True)
            
            st.write("### قائمة المسجلين:")
            display_df = data.copy()
            display_df.index = display_df.index + 1 # البدء من 1
            st.table(display_df)
            
            # --- المربع المختصر في آخر الصفحة ---
            st.divider()
            all_times = []
            for t in data['Times'].dropna():
                all_times.extend(t.split(", "))

            top_days = pd.Series(all_days).value_counts().head(2).index.tolist()
            top_times = pd.Series(all_times).value_counts().head(2).index.tolist()

            st.subheader("📝 النتيجة النهائية (VANTROX Insights)")
            summary_html = f"""
            <div class="summary-box">
                <p style='font-size: 20px;'>📌 <b>الخلاصة لزوم السكرين شوت:</b></p>
                <p style='font-size: 18px;'>✅ <b>أكثر يومين مطلوبين:</b> {', '.join(top_days)}</p>
                <p style='font-size: 18px;'>⏰ <b>أفضل ميعادين للرومات:</b> {', '.join(top_times)}</p>
                <p style='font-size: 18px;'>👥 <b>إجمالي عدد المسجلين:</b> {len(data['Name'].unique())} طالب</p>
            </div>
            """
            st.markdown(summary_html, unsafe_allow_html=True)

            # حذف تسجيل
            st.divider()
            name_to_delete = st.selectbox("حذف طالب:", ["اختار اسم..."] + data['Name'].unique().tolist())
            if st.button("حذف نهائي ❌"):
                if name_to_delete != "اختار اسم...":
                    new_df = data[data['Name'] != name_to_delete]
                    new_df.to_csv(DB_FILE, index=False)
                    st.rerun()
        else:
            st.info("قاعدة البيانات لسه فاضية.")
