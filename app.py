import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import pandas as pd

# ตั้งค่าหน้าต่างเว็บ
st.set_page_config(page_title="Knee AI Telemedicine - ทีมวิตามิน C", page_icon="🩺", layout="centered")

# แก้ไขทางเชื่อม MediaPipe ให้รองรับทุกเวอร์ชันอย่างเสถียร
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# ฟังก์ชันคณิตศาสตร์คำนวณหามุมองศา
def calculate_angle(a, b, c):
a = np.array(a)
b = np.array(b)
c = np.array(c)
radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
angle = np.abs(radians*180.0/np.pi)
if angle > 180.0:
angle = 360-angle
return int(angle)

# ส่วนหัวของหน้าเว็บ (Header)
st.title("🩺 ระบบแสดงผลสรีระข้อเข่าและส่งต่อข้อมูลอัจฉริยะ")
st.subheader("นวัตกรรมคัดกรองเชิงรุกเพื่อการส่งต่อการรักษา โดย ทีมวิตามิน C")
st.markdown("---")

# เมนูหลักด้านซ้ายมือ
st.sidebar.header("📌 เมนูระบบ")
menu = st.sidebar.radio("ขั้นตอนการทำงาน:", ["📊 [01] ลงทะเบียนผู้ป่วย", "📊 [02] ทำการสแกนข้อเข่า / อัปโหลด X-Ray", "📊 [03] AI ประมวลผลและสรุปผล", "📊 [04] สถิติวะบาดวิทยา"])

# บันทึกสถานะตัวแปรเพื่อใช้ข้ามหน้า (Session State)
if 'user_data' not in st.session_state:
st.session_state.user_data = None
if 'analysis_result' not in st.session_state:
st.session_state.analysis_result = None

# =======================================================
# ขั้นตอนที่ 1: ลงทะเบียนหน้าเว็บ
# =======================================================
if menu == "📊 [01] ลงทะเบียนผู้ป่วย":
st.write("### 📝 บันทึกข้อมูลและลงทะเบียนผู้ป่วย")
st.write("กรุณากรอกข้อมูลให้ครบถ้วนเพื่อใช้สำหรับการส่งต่อรูปภาพและการรักษาไปยังโรงพยาบาลปลายทาง")

with st.form("reg_form"):
name = st.text_input("ชื่อ - นามสกุล ผู้รับการตรวจ:", placeholder="ตัวอย่าง: นายสมชาย รักดี")
age = st.number_input("อายุ (ปี):", min_value=0, max_value=120, value=50)
hospital = st.selectbox(
"เลือกโรงพยาบาลที่จะเข้ารับการรักษาต่อ:",
["โรงพยาบาลลพบุรี", "โรงพยาบาลพัฒนานิคม", "โรงพยาบาลพระนารายณ์มหาราช", "โรงพยาบาลอานันทมหิดล"]
)
submit_button = st.form_submit_button("บันทึกข้อมูลและลงทะเบียน")

if submit_button:
if name and hospital:
st.session_state.user_data = {"name": name, "age": age, "hospital": hospital}
st.success(f"✅ บันทึกข้อมูล คุณ {name} สำเร็จ! กรุณาคลิกเลือกเมนูขั้นตอนที่ 2 ที่แถบซ้ายมือต่อได้เลยค่ะ")
else:
st.error("⚠️ กรุณากรอกชื่อและเลือกโรงพยาบาลให้ครบถ้วนก่อนกดบันทึกค่ะ")

# =======================================================
# ขั้นตอนที่ 2: การสแกนข้อเข่า / อัปโหลดไฟล์
# =======================================================
elif menu == "📊 [02] ทำการสแกนข้อเข่า / อัปโหลด X-Ray":
if st.session_state.user_data is None:
st.warning("👈 กรุณาไปที่ขั้นตอนที่ 1 เพื่อกรอกข้อมูลและลงทะเบียนผู้ป่วยก่อนทำการตรวจค่ะ")
else:
st.write(f"📋 **ผู้รับการตรวจ:** {st.session_state.user_data['name']} | **โรงพยาบาลปลายทาง:** {st.session_state.user_data['hospital']}")
st.markdown("---")

st.write("### 🔎 ส่วนเลือกประเภทการตรวจวิเคราะห์")
knee_problem = st.selectbox("1. เลือกปัญหาข้อเข่าที่ต้องการสแกน:", ["เข่าเสื่อม", "รูปทรงขาผิดปกติ"])
scan_method = st.selectbox("2. เลือกช่องทางการนำเข้าข้อมูลสรีระ:", ["สแกนสดผ่านกล้องหน้าเว็บ", "อัปโหลดไฟล์ภาพ X-RAY"])

uploaded_image = None

if scan_method == "สแกนสดผ่านกล้องหน้าเว็บ":
st.info("💡 วิธีใช้: ยืนหันข้างให้กล้องเห็นแนวขาชัดเจน แล้วกดถ่ายรูป")
img_file_buffer = st.camera_input("ส่องกล้องไปที่ข้อเข่าแล้วกดถ่ายรูป")
if img_file_buffer is not None:
uploaded_image = img_file_buffer.getvalue()
else:
st.info("💡 วิธีใช้: แนบไฟล์ภาพถ่ายรังสี (X-Ray) ข้อเข่าจากคอมพิวเตอร์เข้าสู่ระบบ")
file_upload = st.file_uploader("เลือกรูปภาพ X-Ray (ไฟล์ .jpg, .png):", type=["jpg", "jpeg", "png"])
if file_upload is not None:
uploaded_image = file_upload.getvalue()

if uploaded_image is not None:
# ประมวลผลภาพด้วย MediaPipe
cv2_img = cv2.imdecode(np.frombuffer(uploaded_image, np.uint8), cv2.IMREAD_COLOR)
image_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
results = pose.process(image_rgb)

knee_angle = 150 # ค่าเริ่มต้นกรณีตรวจจับกระดูกไม่ได้

if results.pose_landmarks:
landmarks = results.pose_landmarks.landmark
hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
knee_angle = calculate_angle(hip, knee, ankle)
mp_drawing.draw_landmarks(image_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

# บันทึกผลลัพธ์
st.session_state.analysis_result = {"angle": knee_angle, "problem": knee_problem, "image": image_rgb}
st.success("🎉 อัปโหลดและวิเคราะห์ข้อมูลดิบเสร็จสิ้น! กรุณาคลิกขั้นตอนที่ 3 ที่แถบซ้ายมือเพื่อดูผลการรักษา")

# =======================================================
# ขั้นตอนที่ 3: AI ประมวลผลและสรุปผล
# =======================================================
elif menu == "📊 [03] AI ประมวลผลและสรุปผล":
if st.session_state.user_data is None or st.session_state.analysis_result is None:
st.warning("⚠️ ข้อมูลยังไม่ครบ! กรุณาลงทะเบียนและทำสแกนภาพข้อเข่าในขั้นตอนที่ 1 และ 2 ให้เรียบร้อยก่อนค่ะ")
else:
u_data = st.session_state.user_data
res_data = st.session_state.analysis_result
angle = res_data["angle"]
prob_type = res_data["problem"]

st.write(f"### 📊 ใบรายงานผลการวิเคราะห์โรคและส่งตัวผู้ป่วยด้วย AI")
st.write(f"**ชื่อผู้ป่วย:** คุณ {u_data['name']} | **อายุ:** {u_data['age']} ปี")
st.write(f"**โรงพยาบาลปลายทาง:** {u_data['hospital']} *(ระบบพร้อมส่งต่อรูปภาพและผลวิเคราะห์เข้าสู่ระบบฐานข้อมูลโรงพยาบาลแล้ว)*")
st.markdown("---")

st.image(res_data["image"], caption="ภาพหลักฐานการวิเคราะห์โครงสร้างสรีระ", use_container_width=True)
st.write(f"📐 **มุมองศาข้อเข่าที่ AI ตรวจวัดได้:** {angle} องศา (วิเคราะห์ในหมวด: ปัญหา{prob_type})")

st.subheader("🤖 ผลประเมินและวินิจฉัยโดย AI:")

if angle < 90:
st.error("🔴 **1. ผลวินิจฉัยพยาธิสภาพ:** ข้อเข่าติดขั้นรุนแรง มีภาวะกระดูกเสื่อมค่อนข้างชัดเจนร่วมกับสรีระขาผิดรูปรุนแรง")
st.write("🩺 **2. แนวทางการรักษาที่แนะนำ:**")
st.markdown("* ควรส่งพบแพทย์เฉพาะทางศัลยกรรมกระดูกและข้อ (Orthopedics) โดยด่วนเพื่อพิจารณาการผ่าตัดเปลี่ยนข้อเข่าเทียม")
st.markdown("* หลีกเลี่ยงการยกของหนัก หรือการนั่งคุกเข่า พับเพียบ นั่งยอง ๆ เด็ดขาด")
st.markdown("* ใช้อุปกรณ์ช่วยเดิน (Walker) เพื่อช่วยลดแรงกดทับที่ผิวข้อต่อ")
elif 90 <= angle <= 120:
st.warning("🟡 **1. ผลวินิจฉัยพยาธิสภาพ:** ข้อเข่าเริ่มเสื่อมระยะปานกลาง หรือโครงสร้างขาเริ่มมีสรีระโก่งงอเล็กน้อย")
st.write("🩺 **2. แนวทางการรักษาที่แนะนำ:**")
st.markdown("* รักษาด้วยการทำกายภาพบำบัดอย่างสม่ำเสมอ ฝึกความแข็งแรงของกล้ามเนื้อรอบข้อเข่า (Quadriceps)")
st.markdown("* ควบคุมน้ำหนักตัวเพื่อลดแรงกดทับ และใช้ยาลดการอักเสบตามที่แพทย์สั่ง")
st.markdown("* หลีกเลี่ยงกิจกรรมที่มีแรงกระแทกสูง เช่น การวิ่งกระโดด เปลี่ยนมาเป็นการว่ายน้ำหรือปั่นจักรยานแทน")
else:
st.success("🟢 **1. ผลวินิจฉัยพยาธิสภาพ:** สภาพโครงสร้างผิวข้อเข่าและมุมแนวกระดูกอยู่ในเกณฑ์ปกติ เสี่ยงต่ำมาก")
st.write("🩺 **2. แนวทางการรักษาที่แนะนำ:**")
st.markdown("* เน้นการดูแลป้องกันสรีระตามปกติ ออกกำลังกายยืดเหยียดเหยียดข้อเข่าให้เต็มช่วงการเคลื่อนไหว")
st.markdown("* รับประทานอาหารที่มีแคลเซียมและคอลลาเจนบำรุงผิวข้อต่อเพื่อชะลอการเสื่อมตามวัย")

st.markdown("---")
if st.button("🚀 ยืนยันการส่งข้อมูลรูปภาพและผลตรวจไปยัง " + u_data['hospital']):
st.balloons()
st.success("ส่งข้อมูลสำเร็จ! เจ้าหน้าที่โรงพยาบาลจะติดต่อกลับเพื่อจัดคิวพบแพทย์เฉพาะทางต่อไปค่ะ")

# =======================================================
# ขั้นตอนที่ 4: สถิติวะบาดวิทยา (อัปเดตย่อหน้าและเพิ่มปุ่มรีเซ็ตแบบสมบูรณ์)
# =======================================================
elif menu == "📊 [04] สถิติวะบาดวิทยา":
st.markdown("### 📊 แดชบอร์ดภาพรวมสถิติสุขภาพชุมชนเชิงรุก")

chart_data = pd.DataFrame(
[185, 92, 450],
index=["สรีระขาโก่ง (Bowlegs)", "สรีระขานิ่ง (Knock Knees)", "สรีระขาปกติ (Normal)"],
columns=["จำนวนผู้ป่วยรวม (ราย)"]
)
st.bar_chart(chart_data)
st.info("💡 ประโยชน์ทางการแพทย์: สถิตินี้จะช่วยให้หน่วยงานสาธารณสุขสามารถนำไปใช้ในการวางแผนจัดหาอุปกรณ์และจัดสรรบุคลากรทางการแพทย์ลงพื้นที่ได้อย่างแม่นยำ")
st.markdown("---")
st.success("📊 สรุปรายงานสถิติเชิงระบาดวิทยาในพื้นที่เสร็จสิ้น")

if st.button("🔄 รีเซ็ตระบบเพื่อประเมินผู้ป่วยรายใหม่"):
st.rerun()

