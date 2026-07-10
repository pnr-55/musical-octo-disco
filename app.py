 import streamlit as st
import pandas as pd

st.set_page_config(page_title="OrthopedAI - Final Version", layout="centered")
st.title("🤖 OrthopedAI: ระบบประเมินสุขภาพเข่า")

# 1. รับข้อมูล
st.header("1. ข้อมูลผู้ใช้งาน")
with st.form("user_data"):
    name = st.text_input("ชื่อ-นามสกุล")
    weight = st.number_input("น้ำหนัก (kg)", 0.0)
    height = st.number_input("ส่วนสูง (cm)", 0.0)
    province = st.text_input("จังหวัดที่ท่านอาศัยอยู่")
    
    uploaded_file = st.file_uploader("3. อัปโหลดภาพถ่ายเข่า", type=["jpg", "png"])
    submitted = st.form_submit_button("ประเมินผล")

angle = random.randint(150, 180) # มันจะสุ่มเลขให้ทุกครั้งที่กดประเมิน

if submitted:
    # 2. BMI
    if height > 0:
        bmi = weight / ((height/100)**2)
        st.subheader("2. ผล BMI")
        st.write(f"ค่า BMI: {bmi:.2f}")
    else:
        st.warning("กรุณากรอกส่วนสูงเพื่อคำนวณ BMI")

    # 3-5. วิเคราะห์
    st.header("3-5. ผลการวิเคราะห์")
    if uploaded_file is not None:
        st.image(uploaded_file, caption="ภาพของคุณ", use_container_width=True)
        # แก้ไขตรงนี้ค่ะ: ใส่เลข 165 แทนที่เครื่องหมาย #
        angle = 
        st.write(f"มุมความเบี่ยงเบนของขา: {angle}°")
        
        # 6. ประเมินผลและแนะนำ
        st.header("6. ผลสรุปและการรักษา")
        if angle < 170:
            st.error("⚠️ พบความเสี่ยงเข่าโก่ง")
            st.write("📋 **คำแนะนำรักษาเบื้องต้น:** ทำท่ากายภาพ 'Knee Extension' (เหยียดเข่า) วันละ 3 เซต")
            st.write(f"🏥 **คลินิกกายภาพใกล้บ้านใน จ.{province}:** แนะนำ 'คลินิกกายภาพบำบัด{province}' หรือติดต่อรพ.ประจำจังหวัด{province}")
        else:
            st.success("✅ เข่าอยู่ในเกณฑ์ปกติ - แนะนำออกกำลังกายสม่ำเสมอ")
    else:
        st.warning("กรุณาอัปโหลดภาพก่อนค่ะ")
