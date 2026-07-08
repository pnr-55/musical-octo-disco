import streamlit as st

st.set_page_config(page_title="Knee AI Innovation", layout="centered")

# กำหนดสถานะหน้าปัจจุบัน
if 'page' not in st.session_state: st.session_state.page = "Register"

def go_to(page_name): st.session_state.page = page_name

# --- หน้าที่ 1: ลงทะเบียน ---
if st.session_state.page == "Register":
    st.title("🩺 ขั้นตอนที่ 1: ข้อมูลผู้ป่วย")
    name = st.text_input("ชื่อ - นามสกุล:")
    if st.button("ถัดไป >>"):
        st.session_state.user_data = {"name": name}
        go_to("Scan")
        st.rerun()

# --- หน้าที่ 2: สแกนและวิเคราะห์คณิตศาสตร์ ---
elif st.session_state.page == "Scan":
    st.title("📷 ขั้นตอนที่ 2: วิเคราะห์ AI")
    st.write(f"สวัสดีคุณ {st.session_state.user_data['name']} อัปโหลดภาพเพื่อคำนวณมุมเข่า")
    file = st.file_uploader("X-Ray Image:", type=["jpg", "png"])
    
    if file and st.button("เริ่มวิเคราะห์ด้วย AI"):
        # จำลองการคำนวณทางคณิตศาสตร์
        angle = 168.5  # มุมที่คำนวณได้
        st.session_state.analysis = {"angle": angle}
        go_to("Result")
        st.rerun()

# --- หน้าที่ 3: ผลลัพธ์เชิงสถิติ ---
elif st.session_state.page == "Result":
    st.title("📊 ผลการวิเคราะห์")
    angle = st.session_state.analysis['angle']
    st.metric("มุมข้อเข่า", f"{angle}°")
    
    # วิเคราะห์ด้วยเงื่อนไขคณิตศาสตร์
    if angle < 170:
        st.error("ความเสี่ยง: ขาโก่ง (Bowlegs) มีความเสี่ยงข้อเข่าเสื่อมสูง")
    else:
        st.success("สภาพเข่าปกติ")
    
    if st.button("<< เริ่มต้นใหม่"):
        go_to("Register")
        st.rerun()
