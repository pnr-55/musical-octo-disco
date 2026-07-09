import streamlit as st
import pandas as pd
import os

import db
from angle_model import estimate_knee_angle, AngleDetectionError

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Knee AI - Telemedicine Pro", layout="wide")
db.init_db()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploaded_images")
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.markdown(
    "<h1 style='text-align: center; color: #00f2fe;'>🤖 KNEE-AI: PRO GUIDED VERSION</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; color:#888;'>⚕️ เครื่องมือนี้เป็นต้นแบบเพื่อการสาธิตเท่านั้น "
    "ไม่ใช่เครื่องมือวินิจฉัยทางการแพทย์ และไม่ทดแทนการตรวจโดยแพทย์หรือนักกายภาพบำบัด</p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "current_id" not in st.session_state:
    st.session_state.current_id = None

menu = st.sidebar.radio(
    "SELECT MODE:",
    ["🧬 [01] ลงทะเบียน / เข้าสู่ระบบ", "📷 [02] สแกนเข่า",
     "📊 [03] ผลลัพธ์และท่ากายภาพ", "📈 [04] ประวัติพัฒนาการ"],
)

if st.session_state.current_id:
    st.sidebar.success(f"เข้าสู่ระบบ: {st.session_state.current_id}")
    if st.sidebar.button("ออกจากระบบ"):
        st.session_state.current_id = None
        st.rerun()

# ---------------------------------------------------------------------------
# [01] Register / Login
# ---------------------------------------------------------------------------
if menu == "🧬 [01] ลงทะเบียน / เข้าสู่ระบบ":
    st.subheader("📝 ระบบลงทะเบียนคนไข้")
    st.info("💡 ใช้รหัสประจำตัวและรหัสผ่านของคุณ หากยังไม่เคยลงทะเบียน ระบบจะสร้างบัญชีใหม่ให้อัตโนมัติ")

    tab_login, tab_register = st.tabs(["เข้าสู่ระบบ", "ลงทะเบียนใหม่"])

    with tab_login:
        pid = st.text_input("รหัสคนไข้:", key="login_pid")
        pw = st.text_input("รหัสผ่าน:", type="password", key="login_pw")
        if st.button("เข้าสู่ระบบ"):
            if not pid or not pw:
                st.error("กรุณากรอกรหัสคนไข้และรหัสผ่านให้ครบ")
            elif db.verify_patient(pid, pw):
                st.session_state.current_id = pid
                st.success(f"ยินดีต้อนรับกลับมาค่ะ รหัส: {pid}")
                st.rerun()
            else:
                st.error("รหัสคนไข้หรือรหัสผ่านไม่ถูกต้อง")

    with tab_register:
        new_pid = st.text_input("ตั้งรหัสคนไข้ (ตัวเลขหรือตัวอักษร 4 หลักขึ้นไป):", key="reg_pid")
        new_pw = st.text_input("ตั้งรหัสผ่าน (อย่างน้อย 6 ตัวอักษร):", type="password", key="reg_pw")
        province = st.text_input("จังหวัดที่อยู่ (สำหรับค้นหาคลินิกใกล้คุณ):", key="reg_province")
        if st.button("สร้างบัญชีใหม่"):
            if len(new_pid.strip()) < 4:
                st.error("รหัสคนไข้ต้องมีความยาวอย่างน้อย 4 ตัวอักษร")
            elif len(new_pw) < 6:
                st.error("รหัสผ่านต้องมีความยาวอย่างน้อย 6 ตัวอักษร")
            elif db.patient_exists(new_pid.strip()):
                st.error("รหัสคนไข้นี้มีผู้ใช้แล้ว กรุณาเลือกรหัสอื่น หรือไปที่แท็บ 'เข้าสู่ระบบ'")
            else:
                db.create_patient(new_pid.strip(), new_pw, province.strip())
                st.session_state.current_id = new_pid.strip()
                st.success(f"สร้างโปรไฟล์รหัส: {new_pid} สำเร็จ!")
                st.rerun()

# ---------------------------------------------------------------------------
# [02] Scan
# ---------------------------------------------------------------------------
elif menu == "📷 [02] สแกนเข่า":
    st.subheader("📷 ระบบสแกนเข่าด้วย AI")
    if not st.session_state.current_id:
        st.warning("⚠️ กรุณาไปที่เมนู [01] เพื่อลงทะเบียน/เข้าสู่ระบบก่อนค่ะ")
    else:
        st.info("💡 **ขั้นตอนการใช้:** ถ่ายภาพขาให้เห็นสะโพก เข่า และข้อเท้าชัดเจน -> อัปโหลด -> กด 'วิเคราะห์ผล'")
        file = st.file_uploader("อัปโหลดภาพเข่าของคุณ:", type=["jpg", "jpeg", "png"])
        if file and st.button("วิเคราะห์ผล"):
            image_bytes = file.getvalue()
            with st.spinner("AI กำลังตรวจจับตำแหน่งข้อต่อจากภาพ..."):
                try:
                    angle = estimate_knee_angle(image_bytes)
                except AngleDetectionError as e:
                    st.error(f"❌ {e}")
                    angle = None
                except Exception as e:
                    st.error(f"❌ เกิดข้อผิดพลาดขณะประมวลผลภาพ: {e}")
                    angle = None

            if angle is not None:
                # Save the image to disk (not just kept in memory)
                pid = st.session_state.current_id
                safe_name = f"{pid}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}_{file.name}"
                save_path = os.path.join(UPLOAD_DIR, safe_name)
                with open(save_path, "wb") as f:
                    f.write(image_bytes)

                db.add_scan(pid, angle, save_path)
                st.success(f"วิเคราะห์เสร็จสิ้น! มุมเข่าที่คำนวณได้คือ {angle}°")
                st.write("➡️ **กดไปที่เมนู [03] เพื่อดูผลลัพธ์และท่ากายภาพค่ะ**")

# ---------------------------------------------------------------------------
# [03] Results
# ---------------------------------------------------------------------------
elif menu == "📊 [03] ผลลัพธ์และท่ากายภาพ":
    st.subheader("📊 ผลลัพธ์และคำแนะนำ")
    if not st.session_state.current_id:
        st.warning("⚠️ กรุณาไปที่เมนู [01] เพื่อลงทะเบียน/เข้าสู่ระบบก่อนค่ะ")
    else:
        last = db.get_last_scan(st.session_state.current_id)
        if last:
            st.metric("องศาของข้อเข่าล่าสุด", f"{last['angle']}°")

            if last["angle"] < 150:
                st.error("⚠️ พบแนวเข่าที่อาจผิดปกติ! คำแนะนำเบื้องต้นด้านล่างนี้ไม่ทดแทนการวินิจฉัยของแพทย์")
                st.table(pd.DataFrame({
                    "ท่าบริหาร": ["ยืดกล้ามเนื้อต้นขา", "กระดกข้อเท้า", "ยกขาตรง"],
                    "ความถี่": ["3 รอบ/วัน", "2 รอบ/วัน", "3 รอบ/วัน"],
                }))
                province = db.get_province(st.session_state.current_id) or "ประเทศไทย"
                query = f"คลินิกกายภาพบำบัดใกล้ฉัน+ใน+{province}"
                st.markdown(f"🏥 [ค้นหาคลินิกกายภาพใกล้ฉันใน{province}](https://www.google.com/maps/search/{query})")
            else:
                st.success("✅ แนวเข่าของคุณอยู่ในเกณฑ์ปกติค่ะ")

            st.caption("ผลลัพธ์นี้คำนวณจากภาพถ่ายด้วยแบบจำลองตรวจจับท่าทางทั่วไป "
                       "ไม่ใช่อุปกรณ์การแพทย์ที่ผ่านการรับรอง หากมีอาการปวดหรือผิดปกติ กรุณาพบแพทย์")
        else:
            st.warning("ยังไม่มีข้อมูลผลการวิเคราะห์ค่ะ กรุณาสแกนเข่าในเมนู [02] ก่อน")

# ---------------------------------------------------------------------------
# [04] History
# ---------------------------------------------------------------------------
elif menu == "📈 [04] ประวัติพัฒนาการ":
    st.subheader("📈 ประวัติพัฒนาการของคุณ")
    if not st.session_state.current_id:
        st.warning("⚠️ กรุณาไปที่เมนู [01] เพื่อลงทะเบียน/เข้าสู่ระบบก่อนค่ะ")
    else:
        hist = db.get_history(st.session_state.current_id)
        if hist:
            df = pd.DataFrame(hist)
            st.line_chart(df.set_index("date"))
            st.download_button(
                "📥 ดาวน์โหลดประวัติ CSV",
                data=df.to_csv().encode("utf-8"),
                file_name="history.csv",
            )
        else:
            st.write("ยังไม่มีข้อมูลประวัติการรักษาค่ะ")
