import streamlit as st

# ตั้งค่าหน้าเว็บให้สวยงาม
st.set_page_config(page_title="Knee AI Pro", page_icon="🩺", layout="centered")

# CSS ตกแต่งให้ดูเป็นทางการและทันสมัย
st.markdown("""
    <style>
    .stApp {background-color: #f8f9fa;}
    .report-box {background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #dee2e6;}
    </style>
    """, unsafe_allow_html=True)

# ระบบจำข้อมูลไม่ให้หาย (Session State)
if 'page' not in st.session_state: st.session_state.page = "Register"
if 'name' not in st.session_state: st.session_state.name = ""
if 'hospital' not in st.session_state: st.session_state.hospital = "โรงพยาบาลพระนารายณ์"
if 'angle' not in st.session_state: st.session_state.angle = None

# --- หน้าที่ 1: ลงทะเบียน ---
if st.session_state.page == "Register":
    st.title("🩺 Knee AI: ประเมินสุขภาพเข่า")
    st.session_state.name = st.text_input("ชื่อ - นามสกุล:", value=st.session_state.name)
    st.session_state.hospital = st.selectbox("เลือกโรงพยาบาล:", 
                                            ["โรงพยาบาลพระนารายณ์", "โรงพยาบาลลพบุรี", "โรงพยาบาลอานันทมหิดล", "อื่นๆ"])
    if st.button("เข้าสู่การวิเคราะห์ >>"):
        st.session_state.page = "Scan"
        st.rerun()

# --- หน้าที่ 2: สแกน ---
elif st.session_state.page == "Scan":
    st.title("📷 วิเคราะห์ด้วย AI")
    file = st.file_uploader("อัปโหลดภาพ X-Ray เข่า:", type=["jpg", "png"])
    if file and st.button("เริ่มประมวลผล"):
        st.session_state.angle = 155.0 # ค่าจำลอง
        st.session_state.page = "Result"
        st.rerun()

# --- หน้าที่ 3: ผลลัพธ์และคำแนะนำ ---
elif st.session_state.page == "Result":
    st.title("📊 สรุปผลการวิเคราะห์")
    
    with st.container():
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.metric("องศาข้อเข่า", f"{st.session_state.angle}°")
        st.write(f"**ผู้ป่วย:** {st.session_state.name}")
        st.write(f"**โรงพยาบาลที่แนะนำ:** {st.session_state.hospital}")
        
        if st.session_state.angle < 160:
            st.error("🚨 ตรวจพบภาวะขาโก่ง: จำเป็นต้องได้รับการดูแลจากผู้เชี่ยวชาญ")
            st.link_button("📍 ค้นหาคลินิกกายภาพบำบัดใกล้ฉัน", "https://www.google.com/maps/search/คลินิกกายภาพบำบัดใกล้ฉัน")
        else:
            st.success("🟢 สภาพเข่าปกติ")
        st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("🏠 คำแนะนำการบริหารกล้ามเนื้อที่บ้าน")
    with st.expander("ดูท่าบริหารกล้ามเนื้อรอบเข่า"):
        st.write("1. **Straight Leg Raise:** นอนหงาย เหยียดขาตรง ยกขาขึ้นช้าๆ ค้างไว้ 5 วินาที (ทำ 10 ครั้ง)")
        st.write("2. **Hamstring Stretch:** นั่งเก้าอี้ ยืดขาข้างหนึ่งไปข้างหน้า แล้วค่อยๆ โน้มตัวลง (ทำ 10 ครั้ง)")
        st.write("3. **Wall Squat:** พิงกำแพง ย่อเข่าลงเล็กน้อย ค้างไว้ 10 วินาที")
    
    st.info("💡 คำแนะนำ: หากมีอาการปวดรุนแรง ห้ามฝืนทำท่าบริหาร ให้รีบไปพบแพทย์ตามโรงพยาบาลที่เลือกไว้ทันทีครับ")

    if st.button("เริ่มใหม่"):
        st.session_state.name = ""
        st.session_state.page = "Register"
        st.rerun()
