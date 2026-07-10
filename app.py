import streamlit as st
import pandas as pd

st.set_page_config(page_title="OrthopedAI Workflow", layout="centered")
st.title("🤖 OrthopedAI: ระบบประเมินสุขภาพเข่า")

# 1. รับข้อมูล
st.header("1. รับข้อมูลผู้ใช้งาน")
with st.form("user_data"):
    name = st.text_input("ชื่อ-นามสกุล")
    weight = st.number_input("น้ำหนัก (kg)", 0.0)
    height = st.number_input("ส่วนสูง (cm)", 0.0)
    hospital = st.selectbox("เลือกโรงพยาบาล", ["รพ.พระนารายณ์", "รพ.พัฒนานิคม"])
    
    # เพิ่มส่วนอัปโหลดภาพที่นี่
    uploaded_file = st.file_uploader("3. อัปโหลดภาพถ่ายเข่า (ตาม Workflow)", type=["jpg", "png"])
    
    submitted = st.form_submit_button("คำนวณและประเมินผล")

if submitted:
    # 2. คำนวณ BMI
    bmi = weight / ((height/100)**2)
    st.subheader("2. ผล BMI")
    st.write(f"ค่า BMI ของคุณคือ: {bmi:.2f}")

    # 3-5. วิเคราะห์ภาพ
    st.header("3-5. วิเคราะห์ด้วย AI และคณิตศาสตร์")
    if uploaded_file is not None:
        st.image(uploaded_file, caption="ภาพที่อัปโหลด", use_container_width=True)
        st.info("กำลังประมวลผล Computer Vision และคำนวณมุมความเบี่ยงเบน...")
        angle = 165 # ค่าจำลองการคำนวณ
        st.write(f"มุมความเบี่ยงเบนของขา: {angle}°")
    else:
        st.warning("กรุณาอัปโหลดภาพก่อนประเมินผลค่ะ")
        angle = 180

    # 6. ประเมินผล
    st.header("6. ประเมินผลและส่งต่อ")
    if angle < 170:
        st.error("⚠️ พบความเสี่ยงเข่าโก่ง")
        st.write(f"ระบบส่งข้อมูลของคุณไปยัง {hospital} เรียบร้อยแล้ว")
    else:
        st.success("✅ เข่าอยู่ในเกณฑ์ปกติ")
