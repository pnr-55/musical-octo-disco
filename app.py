import sys
try: import cv2
except ImportError:
    st.error("ระบบกำลังติดตั้ง Library กรุณารอ 1 นาทีแล้วรีเฟรช")
# ตั้งค่า MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

st.set_page_config(page_title="Knee AI - Smart Scan", layout="wide")
st.title("🤖 Knee AI: ระบบวิเคราะห์เข่าอัจฉริยะ")

# ฟังก์ชันคำนวณมุม
def calculate_angle(a, b, c):
    a = np.array(a); b = np.array(b); c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0: angle = 360 - angle
    return angle

# จัดการข้อมูล
DB_FILE = "patient_data.csv"
if os.path.exists(DB_FILE): df = pd.read_csv(DB_FILE)
else: df = pd.DataFrame(columns=["id", "date", "angle"])

# 🔑 Sidebar
uid = st.sidebar.text_input("🔑 รหัสประจำตัวคนไข้ (4 หลัก):")

if uid:
    st.sidebar.success(f"ผู้ใช้งาน: {uid}")
    
    # 📷 ส่วนการอัปโหลดและวิเคราะห์
    st.header("📸 วิเคราะห์องศาเข่าด้วย AI")
    uploaded_file = st.file_uploader("อัปโหลดรูปขา (เห็นสะโพก-เข่า-ข้อเท้า):", type=["jpg", "png"])
    
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if results.pose_landmarks:
            lms = results.pose_landmarks.landmark
            hip = [lms[mp_pose.PoseLandmark.LEFT_HIP.value].x, lms[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [lms[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lms[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [lms[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lms[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            angle = calculate_angle(hip, knee, ankle)
            st.image(image, caption="รูปที่ AI วิเคราะห์", use_container_width=True)
            st.metric("องศาที่วิเคราะห์ได้", f"{round(angle, 2)}°")
            
            if st.button("บันทึกผลการวิเคราะห์"):
                new_data = pd.DataFrame([{"id": uid, "date": str(datetime.date.today()), "angle": round(angle, 2)}])
                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success("บันทึกข้อมูลเรียบร้อย!")
        else:
            st.error("AI หาข้อต่อไม่เจอค่ะ! ลองถ่ายรูปให้เห็นตัวเต็มตั้งแต่สะโพกถึงข้อเท้านะคะ")

    # 📈 ประวัติ
    st.header("📈 ประวัติพัฒนาการ")
    user_hist = df[df['id'] == uid]
    if not user_hist.empty:
        st.line_chart(user_hist.set_index('date')['angle'])
else:
    st.info("👈 กรุณากรอกรหัสประจำตัวในแถบด้านซ้าย")
