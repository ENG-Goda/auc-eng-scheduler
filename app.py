import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

# 1. إعدادات الصفحة بروح VANTROX
st.set_page_config(page_title="AUC English Club - Vantrox", page_icon="🚀", layout="centered")

DB_FILE = "auc_data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=['Name', 'Days', 'Times'])

# 2. CSS احترافي لإخفاء معالم المنصة وتجميل الواجهة
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stButton>button { 
        width: 100%; border-radius: 50px; 
        background: linear-gradient(45deg, #007bff, #00d4ff);
        color: white; height: 3.5em; font-weight: bold; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 10px 20px rgba(0,123,255,0.3); }
    [data-testid="stExpander"] { border: 1px solid #e6e9ef; border-radius: 15px; background: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 دحيحة الإنجليزي في AUC")
st.write("محمود جودة بيمسي.. السيستم ده معمول بالحب عشان ننجز المواعيد.")

# 3. فورم التسجيل بتعديل الـ 3 أيام
with st.container():
    st.subheader("سجل حضورك يا بطل 👇")
    name = st.text_input("اسمك المنور")
    
    # تعديل: اختيار 3 أيام
    days = st.multiselect("اختار أفضل 3 أيام للرومات ف الأسبوع", 
                        ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'],
                        max_selections=3)
    
    times = st.multiselect("اختار ميعادين مناسبين ليك", 
                         ['6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'],
                         max_selections=2)
    
    if st.button("تأكيد وإرسال الاختيارات 🚀"):
        if name and len(days) == 3 and len(times) == 2:
            # الأكشن الروش: بالونات + احتفال
            st.balloons()
            
            # حفظ البيانات بشكل "نظيف" (اسم واحد لكل تسجيل)
            df = load_data()
            new_entry = {
                'Name': name, 
                'Days': ", ".join(days), 
                'Times': ", ".join(times)
            }
            
            updated_df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            updated_df.to_csv(DB_FILE, index=False)
            
            # رسالة نجاح روشة
            st.toast(f'عاش يا {name.split()[0]}.. تم الحفظ بنجاح!', icon='🔥')
            st.success(f"وصل يا برنس! مواعيدك اتحفظت ف سيرفرات VANTROX.")
            time.sleep(2)
            st.rerun()
        else:
            st.error("يا هندسة ركز.. محتاجين الاسم، و 3 أيام، وميعادين بالظبط!")

st.divider()

# 4. لوحة التحكم المطورة (Admin Dashboard)
with st.expander("Admin Access (Mahmoud Only) 🤫"):
    password = st.text_input("كلمة السر", type="password")
    if password == "011405":
        data = load_data()
        if not data.empty:
            st.subheader("📊 تحليل المواعيد الأكثر طلباً")
            
            # معالجة البيانات للتشارت (تفكيك الأيام عشان نحسب كل يوم لوحده)
            all_days = []
            for d in data['Days']:
                all_days.extend(d.split(", "))
            
            day_counts = pd.Series(all_days).value_counts().reset_index()
            day_counts.columns = ['اليوم', 'عدد الطلاب']
            
            # تشارت احترافي ملون
            fig = px.bar(day_counts, x='اليوم', y='عدد الطلاب', 
                         color='عدد الطلاب', color_continuous_scale='Blues',
                         text_auto=True, title="توزيع اختيارات الطلاب على الأيام")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # عرض الجدول النظيف (اسم واحد لكل شخص)
            st.write("### قائمة المسجلين (بدون تكرار):")
            st.table(data) # استخدمنا Table عشان يبقى أوضح من DataFrame
            
            # حذف تسجيل
            st.divider()
            name_to_delete = st.selectbox("حذف طالب معين:", ["اختار اسم..."] + data['Name'].unique().tolist())
            if st.button("حذف نهائي ❌"):
                if name_to_delete != "اختار اسم...":
                    new_df = data[data['Name'] != name_to_delete]
                    new_df.to_csv(DB_FILE, index=False)
                    st.warning(f"تم مسح {name_to_delete}.. جاري التحديث.")
                    time.sleep(1)
                    st.rerun()
        else:
            st.info("لسه مفيش داتا دخلت يا هندسة.")
