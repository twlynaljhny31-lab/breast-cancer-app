import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

st.title("مشروع إبداع - تصنيف سرطان الثدي")

@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('model.h5', compile=False)

try:
    model = load_my_model()
except Exception as e:
    st.error(f"خطأ في تحميل الموديل: {e}")

uploaded_file = st.file_uploader("اختر صورة الأشعة للفحص...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='الصورة المرفوعة للفحص', use_container_width=True)
    
    if st.button('فحص الصورة'):
        with st.spinner('جاري تحليل الصورة...'):
            try:
                # تحجيم الصورة وتجهيزها بمصفوفة مبسطة
                img = image.resize((224, 224))
                x = np.array(img) / 255.0
                x = np.expand_dims(x, axis=0)
                
                # تنفيذ التنبؤ بأمان تام
                preds = model.predict(x)
                
                st.success("تم التحليل بنجاح!")
                
                # طباعة النتيجة بناءً على قيمة التنبؤ المباشرة
                val = float(preds[0][0]) if preds.ndim > 1 else float(preds[0])
                
                if val > 0.5:
                    st.warning(f"النتيجة المتوقعة: يوجد اشتباه (نسبة الثقة: {val:.2f})")
                else:
                    st.info(f"النتيجة المتوقعة: سليم (نسبة الثقة: {1-val:.2f})")
                    
            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة الموديل للصورة: {e}")
