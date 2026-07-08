import streamlit as st

st.set_page_config(page_title="Knee AI Innovation", layout="centered")

if 'page' not in st.session_state: st.session_state.page = "Register"
if 'user_data' not in st.session_state: st.session_state.user_data = None
if 'analysis' not in st.session_state: st.session_state.analysis = None

def go_to(p): st.session_state.page = p

# --- หน้าที่ 1: ลงทะเบียน (เพิ่มเลือกโรงพยาบาล) ---
if st.session_state.page == "Register":
    st.title("🩺 1. ข้อมูลผู้ป่วย")
    name = st.text_input("ชื่อ - นามสกุล:")
    hospital = st.selectbox("เลือกโรงพยาบาลที่ต้องการปรึกษา:", 
                           ["โรงพยาบาลพระนารายณ์", "โรงพยาบาลลพบุรี", "โรงพยาบาลอานันทมหิดล", "อื่นๆ"])
    weight = st.number_input("น้ำหนักตัว (kg):", value=60.0)
    height = st.number_input("ส่วนสูง (cm):", value=160.0)
    if st.button("ถัดไป >>"):
        st.session_state.user_data = {"name": name, "hospital": hospital}
        go_to("Scan")
        st.rerun()

# --- หน้าที่ 2: สแกน ---
elif st.session_state.page == "Scan":
    st.title("📷 2. วิเคราะห์ AI")
    file = st.file_uploader("อัปโหลด X-Ray:", type=["jpg", "png"])
    if file and st.button("วิเคราะห์มุมเข่า"):
        st.session_state.analysis = {"angle": 155.0}
        go_to("Result")
        st.rerun()

# --- หน้าที่ 3: ผลลัพธ์ (เพิ่มปุ่มค้นหาจริง) ---
elif st.session_state.page == "Result":
    st.title("📊 3. ผลการวิเคราะห์")
    angle = st.session_state.analysis['angle']
    st.metric("มุมข้อเข่า", f"{angle}°")
    
    st.subheader("คำแนะนำสำหรับคุณ")
    st.write(f"โรงพยาบาลที่แนะนำ: **{st.session_state.user_data['hospital']}**")
    
    if angle < 160:
        st.error("🚨 ระดับความรุนแรงสูง: ควรปรึกษาแพทย์และนักกายภาพบำบัด")
        # ใช้ปุ่มลิงก์ (link_button) จะกดแล้วเด้งไป Google Maps ให้ทันที
        st.link_button("📍 ค้นหาคลินิกกายภาพบำบัดใกล้ฉันบน Google Maps", 
                       "https://www.google.com/maps/search/คลินิกกายภาพบำบัดใกล้ฉัน")
    else:
        st.success("🟢 อยู่ในเกณฑ์ที่ดูแลตนเองได้")

    st.write("---")
    if st.button("<< เริ่มต้นใหม่"):
        go_to("Register")
        st.rerun()
