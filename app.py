import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="برنامج متابعة الحلقات القرآنية", page_icon="📖", layout="wide")

# تهيئة البيانات في الذاكرة المؤقتة (Session State)
if 'students' not in st.session_state:
    st.session_state.students = []
if 'teacher_name' not in st.session_state:
    st.session_state.teacher_name = ""

# قائمة سور القرآن الكريم (أمثلة لبعض السور مع صفحاتها لتوضيح الحساب التلقائي)
surahs_pages = {
    "الفاتحة (ص 1)": 1, "البقرة (ص 2-49)": 2, "آل عمران (ص 50-76)": 50,
    "النساء (ص 77-106)": 77, "المائدة (ص 106-127)": 106, "الأنعام (ص 128-150)": 128,
    "الأعراف (ص 151-176)": 151, "الأنفال (ص 177-186)": 177, "التوبة (ص 187-207)": 187,
    "يونس (ص 208-221)": 208, "هود (ص 221-235)": 221, "يوسف (ص 235-248)": 235,
    # يمكن إضافة بقية السور بنفس الطريقة حتى الناس (ص 604)
}

st.title("📖 برنامج متابعة حلقات القرآن الكريم")
st.markdown("---")

# 1. تسجيل اسم المعلم
with st.sidebar:
    st.header("⚙️ إعدادات الحلقة")
    st.session_state.teacher_name = st.text_input("اسم المعلم المشرف:", value=st.session_state.teacher_name)
    if st.session_state.teacher_name:
        st.success(f"المعلم الحالي: **{st.session_state.teacher_name}**")
    st.markdown("---")
    st.markdown("### تعليمات الاستخدام:")
    st.markdown("- أدخل اسم الطالب.")
    st.markdown("- حدد صفحات الحفظ والمراجعة ليتم حسابها تلقائياً.")
    st.markdown("- سجل الحضور لأيام الأسبوع (من الأحد إلى الخميس).")

# 2. القائمة الرئيسية / نموذج تسجيل بيانات الطالب
st.header("📝 تسجيل وتحديث متابعة طالب")

with st.form("student_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        student_name = st.text_input("اسم الطالب")
        
        st.subheader("📌 الحفظ اليومي")
        hifz_start = st.number_input("من صفحة (الحفظ)", min_value=1, max_value=604, value=1)
        hifz_end = st.number_input("إلى صفحة (الحفظ)", min_value=1, max_value=604, value=1)
        hifz_grade = st.selectbox("تقدير الحفظ", ["ممتاز", "جيد جداً", "جيد", "مقبول", "إخفاق"])

        st.subheader("🔄 المراجعة الكبرى")
        maj_rev_start = st.number_input("من صفحة (المراجعة الكبرى)", min_value=1, max_value=604, value=1)
        maj_rev_end = st.number_input("إلى صفحة (المراجعة الكبرى)", min_value=1, max_value=604, value=1)
        maj_grade = st.selectbox("تقدير المراجعة الكبرى", ["ممتاز", "جيد جداً", "جيد", "مقبول", "إخفاق"])

    with col2:
        st.subheader("🔄 المراجعة الصغرى")
        min_rev_start = st.number_input("من صفحة (المراجعة الصغرى)", min_value=1, max_value=604, value=1)
        min_rev_end = st.number_input("إلى صفحة (المراجعة الصغرى)", min_value=1, max_value=604, value=1)
        min_grade = st.selectbox("تقدير المراجعة الصغرى", ["ممتاز", "جيد جداً", "جيد", "مقبول", "إخفاق"])

        st.subheader("📅 الحضور والغياب (من الأحد إلى الخميس)")
        attendance = st.multiselect(
            "الأيام الحاضر فيها:",
            ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس"]
        )

    submit_button = st.form_submit_button(label="حفظ بيانات الطالب")

    if submit_button:
        if student_name.strip() == "":
            st.error("الرجاء إدخال اسم الطالب على الأقل.")
        else:
            # الحساب التلقائي لعدد الصفحات
            hifz_pages_count = max(0, (hifz_end - hifz_start) + 1)
            maj_pages_count = max(0, (maj_rev_end - maj_rev_start) + 1)
            min_pages_count = max(0, (min_rev_end - min_rev_start) + 1)
            
            attendance_count = len(attendance)
            absence_count = 5 - attendance_count  # الأسبوع 5 أيام دراسية (الأحد للخميس)

            student_data = {
                "اسم المعلم": st.session_state.teacher_name,
                "اسم الطالب": student_name,
                "مقدار الحفظ اليومي": f"{hifz_pages_count} صفحة (من {hifz_start} إلى {hifz_end})",
                "مقدار المراجعة الكبرى": f"{maj_pages_count} صفحة (من {maj_rev_start} إلى {maj_rev_end})",
                "مقدار المراجعة الصغرى": f"{min_pages_count} صفحة (من {min_rev_start} إلى {min_rev_end})",
                "الحضور (أيام)": f"حضور: {attendance_count} | غياب: {absence_count}",
                "تقدير الحفظ": hifz_grade,
                "تقدير المراجعة الكبرى": maj_grade,
                "تقدير المراجعة الصغرى": min_grade
            }
            
            st.session_state.students.append(student_data)
            st.success(f"تم حفظ بيانات الطالب **{student_name}** بنجاح!")

# 3. عرض جدول المتابعة للطلاب المسجلين
st.markdown("---")
st.header("📊 جدول متابعة الحلقة")

if len(st.session_state.students) > 0:
    df = pd.DataFrame(st.session_state.students)
    st.dataframe(df, use_container_width=True)
    
    if st.button("🗑️ مسح جميع البيانات"):
        st.session_state.students = []
        st.rerun()
else:
    st.info("لا توجد بيانات مسجلة حتى الآن. ابدأ بإضافة الطلاب من النموذج أعلاه.")
