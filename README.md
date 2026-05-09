# 🎓 AI Attendance System Using Face Recognition

> Hệ thống điểm danh học sinh tự động bằng AI nhận diện khuôn mặt sử dụng Python, Flask và OpenCV.

---

# 📌 Giới thiệu đề tài

Trong môi trường giáo dục hiện nay, việc điểm danh học sinh vẫn chủ yếu được thực hiện thủ công bằng cách gọi tên hoặc ký giấy, gây mất nhiều thời gian và dễ xảy ra sai sót.

Đề tài **“Hệ thống điểm danh học sinh tự động bằng AI nhận diện khuôn mặt”** được xây dựng nhằm ứng dụng công nghệ trí tuệ nhân tạo (AI) vào giáo dục để tự động hóa quá trình điểm danh thông qua camera USB.

Hệ thống cho phép nhận diện khuôn mặt học sinh đã đăng ký trước đó để thực hiện điểm danh theo thời gian thực, đồng thời lưu dữ liệu vào cơ sở dữ liệu và xuất file Excel phục vụ công tác quản lý.

Ngoài ra, hệ thống còn được xây dựng với giao diện Web GUI trực quan, thân thiện và dễ sử dụng cho giáo viên.

---

# 🎯 Mục tiêu của đề tài

✅ Ứng dụng AI vào giáo dục  
✅ Tự động hóa quá trình điểm danh  
✅ Giảm thời gian quản lý lớp học  
✅ Hạn chế gian lận điểm danh hộ  
✅ Nâng cao tính hiện đại trong quản lý học sinh  
✅ Xây dựng hệ thống thông minh dễ sử dụng  

---

# 🚀 Chức năng chính của hệ thống

## 👤 1. Đăng ký khuôn mặt học sinh

- Nhập tên học sinh
- Camera tự động chụp nhiều ảnh khuôn mặt
- Tạo dataset phục vụ AI recognition
- Lưu dữ liệu học sinh vào database

---

## 🎥 2. Nhận diện khuôn mặt thời gian thực

- Sử dụng camera USB realtime
- Nhận diện khuôn mặt bằng AI
- Hiển thị tên trực tiếp trên camera
- Giảm nhận diện sai bằng AI threshold

---

## ✅ 3. Điểm danh tự động

Khi học sinh đứng trước camera:

- Hệ thống tự động nhận diện
- Ghi nhận điểm danh
- Phát giọng nói tiếng Việt

Ví dụ:

```text
Đỗ Đức Hùng điểm danh thành công
Nguyễn Tuấn Hoàng đã điểm danh rồi nhé

Ngoài ra hệ thống còn:

Chống spam điểm danh
Không cho phép điểm danh liên tục
Tự động kiểm tra trùng lặp
🗂️ 4. Quản lý dữ liệu điểm danh
Lưu dữ liệu bằng SQLite Database
Quản lý lịch sử điểm danh
Xuất file Excel tự động
Hỗ trợ thống kê:
Theo ngày
Theo tuần
Theo tháng
🌐 5. Web GUI quản lý hệ thống

Hệ thống được xây dựng bằng Flask Web Framework với giao diện trực quan gồm:

🏠 Trang chủ
👥 Quản lý học sinh
📸 Trang đăng ký khuôn mặt
🎥 Trang điểm danh realtime
📊 Dashboard thống kê
📁 Xuất file Excel
🛠️ Công nghệ sử dụng
Công nghệ	Mục đích
🐍 Python	Ngôn ngữ chính
🌐 Flask	Web Framework
🎥 OpenCV	Xử lý camera
🤖 face_recognition	AI nhận diện khuôn mặt
🗄️ SQLite	Cơ sở dữ liệu
📊 Pandas	Xuất file Excel
🔊 gTTS	Giọng nói tiếng Việt
🎨 HTML/CSS	Thiết kế giao diện
📈 Ý nghĩa thực tiễn

Hệ thống giúp:

✅ Tiết kiệm thời gian điểm danh
✅ Giảm áp lực quản lý cho giáo viên
✅ Hạn chế tình trạng điểm danh hộ
✅ Nâng cao độ chính xác
✅ Ứng dụng AI vào thực tế giáo dục
✅ Hướng tới mô hình Smart School

🔥 Các tính năng nổi bật
🎯 Nhận diện khuôn mặt realtime
🔊 Voice tiếng Việt tự động
📊 Dashboard thống kê
📁 Export Excel
⚡ Tối ưu chống lag camera
🧠 AI chống nhận diện nhầm
🌐 Web GUI hiện đại
🗃️ Database quản lý dữ liệu
📂 Cấu trúc thư mục
AI_Attendance_System/
│
├── dataset/
├── static/
├── templates/
│
├── attendance/
├── app.py
├── database.py
├── attendance.db
├── requirements.txt
└── README.md
🔮 Hướng phát triển trong tương lai

Hệ thống có thể phát triển thêm:

👨‍🏫 Đăng nhập giáo viên
☁️ Lưu dữ liệu Cloud
📱 Mobile App
📧 Gửi email phụ huynh
🎯 Nhận diện nhiều khuôn mặt cùng lúc
🧠 Deep Learning nâng cao
📹 Hỗ trợ camera IP/CCTV
📊 AI phân tích dữ liệu học sinh
🎓 Kết luận

Đề tài “AI Attendance System Using Face Recognition” là giải pháp ứng dụng trí tuệ nhân tạo mang tính thực tiễn cao trong giáo dục hiện đại.

Hệ thống giúp tự động hóa việc điểm danh, nâng cao hiệu quả quản lý lớp học và tạo nền tảng cho các mô hình trường học thông minh trong tương lai.

👨‍💻 Author

Developed by:
DO Hung
