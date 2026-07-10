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
    submitted = st.form_submit_button("คำนวณและประเมินผล")

if submitted:
    # 2. คำนวณ BMI
    bmi = weight / ((height/100)**2)
    st.subheader("2. ผล BMI")
    st.write(f"ค่า BMI ของคุณคือ: {bmi:.2f}")

    # 3-5. จำลองกระบวนการ AI และคณิตศาสตร์
    st.header("3-5. วิเคราะห์ด้วย AI และคณิตศาสตร์")
    st.info("กำลังประมวลผล Computer Vision และจุดข้อต่อ...")
    
    # จำลององศาเข่า (ถ้าเป็นของจริงจะใช้จุดพิกัดจากรูป)
    angle = 165 # สมมติค่า
    st.write(f"มุมความเบี่ยงเบนของขา: {angle}°")

    # 6. ประเมินผล
    st.header("6. ประเมินผลและส่งต่อ")
    if angle < 170:
        st.error("⚠️ พบความเสี่ยงเข่าโก่ง")
        st.write(f"ระบบส่งข้อมูลของคุณไปยัง {hospital} เรียบร้อยแล้ว")
    else:
        st.success("✅ เข่าอยู่ในเกณฑ์ปกติ")

    # บันทึกประวัติ
    data = {"ชื่อ": [name], "BMI": [bmi], "มุมเข่า": [angle]}
    st.table(pd.DataFrame(data))
