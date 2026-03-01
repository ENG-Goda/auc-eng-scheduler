import streamlit as st
import pandas as pd
import plotly.express as px

# ستايل احترافي مع لمسة صياعة
st.set_page_config(page_title="AUC English Club - Vantrox Edition", page_icon="😎")

# CSS بسيط عشان نخلي الشكل "روقان" على الموبايل
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    .main { background-color: #f5f7f9; }
    </style>
    """, unsafe_allow_index=True)

st.title("🚀 دحيحة الإنجليزي في AUC")
st.write("أهلاً يا شباب.. محمود جودة بيمسي، وعشان إحنا مهندسين مش بتوع ورق وقلم، عملتلكم السيستم ده عشان ننجز ونظبط مواعيد الرومات.")

# --- الفورم بلهجة عامية ---
with st.form("pro_form"):
    st.subheader("سجل حضورك يا بطل 👇")
    name = st.text_input("اسمك المنور (عشان نعرف مين اللي هيسحلنا معاه)")
    
    days = st.multiselect("اختار أكتر يومين 'رايقين' معاك في الأسبوع", 
                        ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'],
                        max_selections=2)
    
    times = st.multiselect("أفضل مواعيد (ماتختارش وقت الماتشات بالله عليك)", 
                         ['6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'])
    
    # حتة "الصياعة" اللي طلبتها: كومنت عشوائي يظهر لكل واحد
    submit = st.form_submit_button("إرسال الاختيارات 🚀")
    
    if submit:
        if name and len(days) == 2 and times:
            # هنا هنخزن البيانات (مبدئياً في الـ Session)
            st.success(f"وصل يا {name.split()[0]}! استنى بقى لما أشوف باقي الشلة ونقرر.")
            st.balloons() # حركة صايعة بتطلع بالونات في الشاشة
        else:
            st.warning("يا هندسة ركز.. محتاجين اسمك ويومين بالظبط!")

# --- لوحة تحكم الأدمن (محمود جودة) ---
st.sidebar.title("Area 51 (Top Secret) 🤫")
if st.sidebar.checkbox("أنا محمود جودة شخصياً"):
    pw = st.sidebar.text_input("الباسورد يا هندسة", type="password")
    if pw == "VantroxAdmin":
        st.header("📊 إحصائيات السهرة")
        st.info("هنا بنشوف مين اللي مسيطر على المواعيد")
        # هنا هتحط الـ Charts زي الكود اللي فات