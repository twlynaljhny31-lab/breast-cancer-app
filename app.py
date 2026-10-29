import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

st.title("مشروع إبداع - تصنيف سرطان الثدي")

@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('model.h5')

try:
    model = load_my_model()
except Exception as e:
    st.error(f"تعذر تحميل الموديل: {e}")

uploaded_file = st.file_uploader("اختر صورة الأشعة للفحص...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='الصورة المرفوعة للفحص', use_container_width=True)
    
    if st.button('تحليل الصورة الآن'):
        with st.spinner('جاري تحليل النموذج...'):
            try:
                img = image.resize((224, 224))
                img_array = np.array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)
                
                prediction = model.predict(img_array)
                
                score = float(prediction[0][0]) if prediction.shape[-1] == 1 else float(np.max(prediction))
                
                st.success("تم التحليل بنجاح!")
                
                if score > 0.5:
                    st.warning(f"النتيجة: يوجد اشتباه (درجة الثقة: {score:.2f})")
                else:
                    st.info(f"النتيجة: سليم (درجة الثقة: {1-score:.2f})")
                    
            except Exception as e:
                st.error(f"تفاصيل الخطأ التقني أثناء التنبؤ: {e}")
