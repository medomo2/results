import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="نتيجة الطلاب", page_icon="🎓", layout="centered")

# --- أهم جزء: اسم ملف الإكسل ---
# لازم الاسم هنا يكون مطابق لاسم الملف اللي رفعته على GitHub
FILE_NAME = 'data.xlsx'

st.title("🎓 نظام الاستعلام عن النتيجة")

# التأكد من وجود الملف
if os.path.exists(FILE_NAME):
    try:
        # قراءة الملف مباشرة (بدون upload)
        df = pd.read_excel(FILE_NAME, dtype=str)
        df.columns = df.columns.str.strip() # تنظيف أسماء الأعمدة

        # خانة البحث
        st.write("### أدخل رقم الجلوس / الكود:")
        student_code = st.text_input("مثال: 120250004617", "")

        if st.button("بحث"):
            if student_code:
                # التأكد من وجود عمود Code
                if 'Code' in df.columns:
                    # تنظيف المدخلات
                    search_val = str(student_code).strip()
                    df['Code'] = df['Code'].astype(str).str.strip()

                    # البحث
                    result = df[df['Code'] == search_val]

                    if not result.empty:
                        st.success("✅ النتيجة موجودة:")
                        st.table(result) # عرض النتيجة
                    else:
                        st.error("❌ الرقم ده مش موجود، حاول تاني.")
                else:
                    st.error("⚠️ خطأ في ملف الإكسل: مفيش عمود اسمه 'Code'.")
            else:
                st.warning("الرجاء كتابة الكود أولاً.")
                
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
else:
    # رسالة لو الملف مش موجود
    st.error("⚠️ ملف البيانات (data.xlsx) غير موجود! يرجى رفعه على GitHub.")

