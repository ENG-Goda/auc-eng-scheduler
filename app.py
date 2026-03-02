import streamlit as st
import pandas as pd
import plotly.express as px
import os

# إعدادات الصفحة الاحترافية - VANTROX Edition
st.set_page_config(page_title="AUC English Club - Vantrox", page_icon="😎", layout="centered")

# اسم ملف قاعدة البيانات المحلي
DB_FILE = "auc_data.csv"

# دالة لتحميل البيانات
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=['Name', 'Day', 'Time'])

# إخفاء معالم Streamlit
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

st.title("🚀 دحيحة الأنجليزي في ال AUC")
st.write("أهلاً يا شباب.. محمود جودة بيمسي، سجل مواعيدك وهتتحفظ في سيرفرات VANTROX فوراً.")

# --- فورم التسجيل ---
with st.form("registration_form", clear_on_submit=True):
    name = st.text_input("اسمك المنور")
    days = st.multiselect("اختار يومين رايقين", ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة'], max_selections=2)
    times = st.multiselect("أفضل مواعيد", ['6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'])
    submit = st.form_submit_button("تأكيد وإرسال 🚀")

    if submit:
        if name and len(days) == 2 and times:
            df = load_data()
            new_entries = []
            for day in days:
                for time in times:
                    new_entries.append({"Name": name, "Day": day, "Time": time})
            
            updated_df = pd.concat([df, pd.DataFrame(new_entries)], ignore_index=True)
            updated_df.to_csv(DB_FILE, index=False)
            st.success(f"تم الحفظ بنجاح يا {name}!")
            st.balloons()
            st.rerun() # تحديث الصفحة عشان البيانات تظهر فوراً
        else:
            st.error("كمل بياناتك (الاسم ويومين بالظبط)!")

st.divider()

# --- لوحة تحكم المهندس (Admin Dashboard) مع خاصية الحذف ---
with st.expander("Admin Access (Mahmoud Only) 🤫"):
    password = st.text_input("كلمة السر", type="password")
    if password == "011405":
        data = load_data()
        if not data.empty:
            st.subheader("📊 إحصائيات المواعيد")
            fig = px.bar(data['Day'].value_counts().reset_index(), x='Day', y='count', color_discrete_sequence=['#007bff'])
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("### التحكم في البيانات")
            st.dataframe(data, use_container_width=True)
            
            # --- خاصية الحذف اللي طلبتها يا هندسة ---
            st.divider()
            st.write("🗑️ **مسح تسجيل معين:**")
            list_of_names = data['Name'].unique().tolist()
            name_to_delete = st.selectbox("اختار الاسم اللي عاوز تمسحه:", ["اختار اسم..."] + list_of_names)
            
            if st.button("حذف هذا الشخص نهائياً ❌"):
                if name_to_delete != "اختار اسم...":
                    # فلترة البيانات واستبعاد الاسم المختار
                    new_df = data[data['Name'] != name_to_delete]
                    new_df.to_csv(DB_FILE, index=False)
                    st.warning(f"تم حذف {name_to_delete} من قاعدة البيانات.")
                    st.rerun() # إعادة تحميل الصفحة لتحديث الجدول والـ Chart
                else:
                    st.error("من فضلك اختار اسم أولاً!")
            
            # زرار تحميل إكسيل
            csv = data.to_csv(index=False).encode('utf-8-sig')
            st.download_button("تحميل البيانات بالكامل Excel", data=csv, file_name="AUC_Results.csv")
        else:
            st.info("قاعدة البيانات لسه فاضية.")
