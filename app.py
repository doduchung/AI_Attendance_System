from flask import Flask
from flask import render_template
from flask import Response
from flask import request

import face_recognition
import cv2
import os
import shutil
import sqlite3
import numpy as np
import pandas as pd

from datetime import datetime

from gtts import gTTS
from playsound import playsound

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from unidecode import unidecode

# =========================
# FLASK
# =========================

app = Flask(__name__)

# =========================
# FONT TIẾNG VIỆT
# =========================

font_path = "C:/Windows/Fonts/arial.ttf"

font = ImageFont.truetype(
    font_path,
    32
)

# =========================
# HÀM PHÁT GIỌNG NÓI
# =========================

def speak_vietnamese(text):

    tts = gTTS(
        text=text,
        lang='vi'
    )

    tts.save("voice.mp3")

    playsound("voice.mp3")

    os.remove("voice.mp3")

# =========================
# MAPPING TÊN THẬT
# =========================

name_mapping = {
    "do_duc_hung": "Đỗ Đức Hùng"
}

# =========================
# LOAD DATASET
# =========================

known_face_encodings = []
known_face_names = []

attendance_list = []

dataset_path = "dataset"

for person_name in os.listdir(dataset_path):

    person_folder = os.path.join(
        dataset_path,
        person_name
    )

    for image_name in os.listdir(person_folder):

        image_path = os.path.join(
            person_folder,
            image_name
        )

        try:

            image = face_recognition.load_image_file(
                image_path
            )

            image = cv2.resize(
                image,
                (300, 300)
            )

            encodings = (
                face_recognition.face_encodings(
                    image
                )
            )

            if len(encodings) > 0:

                face_encoding = encodings[0]

                known_face_encodings.append(
                    face_encoding
                )

                known_face_names.append(
                    person_name
                )

                print(f"Loaded: {person_name}")

        except Exception as e:
            print(e)

print("Hoàn tất load dataset")

# =========================
# FILE ĐIỂM DANH
# =========================

today_date = datetime.now().strftime(
    "%Y-%m-%d"
)

attendance_file = (
    f'attendance/{today_date}.xlsx'
)

# =========================
# CAMERA
# =========================

video_capture = cv2.VideoCapture(1)

video_capture.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    640
)

video_capture.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    480
)

process_this_frame = True

face_locations = []
face_encodings = []

# =========================
# CAMERA GENERATOR
# =========================

def generate_frames():

    global process_this_frame
    global face_locations
    global face_encodings

    while True:

        success, frame = video_capture.read()

        if not success:
            break

        small_frame = cv2.resize(
            frame,
            (0, 0),
            fx=0.20,
            fy=0.20
        )

        rgb_small_frame = cv2.cvtColor(
            small_frame,
            cv2.COLOR_BGR2RGB
        )

        if process_this_frame:

            face_locations = (
                face_recognition.face_locations(
                    rgb_small_frame
                )
            )

            face_encodings = (
                face_recognition.face_encodings(
                    rgb_small_frame,
                    face_locations
                )
            )

        process_this_frame = (
            not process_this_frame
        )

        for face_encoding, face_location in zip(
            face_encodings,
            face_locations
        ):

            matches = (
                face_recognition.compare_faces(
                    known_face_encodings,
                    face_encoding
                )
            )

            name = "Unknown"

            face_distances = (
                face_recognition.face_distance(
                    known_face_encodings,
                    face_encoding
                )
            )

            name = "Unknown"

if len(known_face_encodings) > 0:

    matches = (
        face_recognition.compare_faces(
            known_face_encodings,
            face_encoding
        )
    )

    face_distances = (
        face_recognition.face_distance(
            known_face_encodings,
            face_encoding
        )
    )

    best_match_index = np.argmin(
        face_distances
    )

    if matches[best_match_index]:

        folder_name = known_face_names[
            best_match_index
        ]

        if folder_name in name_mapping:

            name = name_mapping[
                folder_name
            ]

        else:

            name = folder_name

            if matches[best_match_index]:

                folder_name = known_face_names[
                    best_match_index
                ]

                if folder_name in name_mapping:

                    name = name_mapping[
                        folder_name
                    ]

                else:

                    name = folder_name

                # =========================
                # ĐIỂM DANH
                # =========================

                if name not in attendance_list:

                    attendance_list.append(name)

                    current_time = (
                        datetime.now().strftime(
                            "%H:%M:%S"
                        )
                    )

                    df = pd.DataFrame({
                        "HoTen": attendance_list,
                        "ThoiGian":
                            [current_time]
                            * len(attendance_list)
                    })

                    df.to_excel(
                        attendance_file,
                        index=False
                    )
                    conn = sqlite3.connect(
                        'attendance.db'
                    )

                    cursor = conn.cursor()

                    cursor.execute("""

                    INSERT INTO attendance(

                        student_name,
                        attendance_time,
                        attendance_date

                    )

                    VALUES(?,?,?)

                    """, (

                        name,
                        current_time,
                        today_date

                    ))

                    conn.commit()

                    conn.close()
                    print(
                        f"{name} điểm danh thành công"
                    )

                    speak_vietnamese(
                        f"{name} điểm danh thành công"
                    )

                else:

                    print(
                        f"{name} đã điểm danh rồi"
                    )

            # =========================
            # VẼ KHUNG MẶT
            # =========================

            top, right, bottom, left = (
                face_location
            )

            top *= 5
            right *= 5
            bottom *= 5
            left *= 5

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2
            )

            cv2.rectangle(
                frame,
                (left, bottom - 40),
                (right, bottom),
                (0, 255, 0),
                cv2.FILLED
            )

            # =========================
            # TEXT TIẾNG VIỆT
            # =========================

            pil_image = Image.fromarray(
                cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )
            )

            draw = ImageDraw.Draw(
                pil_image
            )

            draw.text(
                (left + 10, bottom - 38),
                name,
                font=font,
                fill=(255, 255, 255)
            )

            frame = cv2.cvtColor(
                np.array(pil_image),
                cv2.COLOR_RGB2BGR
            )

        # Encode frame
        ret, buffer = cv2.imencode(
            '.jpg',
            frame
        )

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )

# =========================
# ROUTES
# =========================

@app.route('/')

def index():

    return dashboard()

@app.route('/attendance')

def attendance():

    return render_template(
        'attendance.html',
        attendance_list=attendance_list,
        total=len(attendance_list)
    )

@app.route('/video_feed')

def video_feed():

    return Response(
        generate_frames(),
        mimetype=(
            'multipart/x-mixed-replace; '
            'boundary=frame'
        )
    )

# =========================
# REGISTER STUDENT
# =========================

@app.route('/register', methods=['GET', 'POST'])

def register():

    message = ""

    if request.method == 'POST':

        student_name = request.form[
            'student_name'
        ]

        # đổi tên folder
        folder_name = (
            unidecode(student_name)
            .lower()
            .replace(" ", "_")
        )

        save_path = os.path.join(
            "dataset",
            folder_name
        )

        os.makedirs(
            save_path,
            exist_ok=True
        )

        cap = video_capture

        count = 0

        while count < 20:

            ret, frame = cap.read()

            if not ret:
                break

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            faces = (
                face_recognition.face_locations(
                    rgb_frame
                )
            )

            for face in faces:

                top, right, bottom, left = face

                face_image = frame[
                    top:bottom,
                    left:right
                ]

                file_name = os.path.join(
                    save_path,
                    f"{count}.jpg"
                )

                cv2.imwrite(
                    file_name,
                    face_image
                )

                count += 1

                cv2.rectangle(
                    frame,
                    (left, top),
                    (right, bottom),
                    (0,255,0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Image: {count}/20",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )

            cv2.imshow(
                "Register Face",
                frame
            )

            if cv2.waitKey(1) == 27:
                break

        

            cv2.destroyAllWindows()
            conn = sqlite3.connect(
                'attendance.db'
            )

            cursor = conn.cursor()

            cursor.execute("""

            INSERT INTO students(
                name,
                folder_name
            )

            VALUES(?,?)

            """, (

                student_name,
                folder_name

            ))

            conn.commit()

            conn.close()
            
            message = (
                f"Đăng ký thành công "
                f"cho {student_name}"
            )

    return render_template(
        'register.html',
        message=message
    )

# =========================
# MAIN
# =========================
@app.route('/students')

def students():

    students_data = []

    dataset_path = "dataset"

    for folder in os.listdir(dataset_path):

        folder_path = os.path.join(
            dataset_path,
            folder
        )

        if os.path.isdir(folder_path):

            total_images = len(
                os.listdir(folder_path)
            )

            display_name = (
                folder
                .replace("_", " ")
                .title()
            )

            students_data.append({

                "name": display_name,

                "folder": folder,

                "total_images":
                    total_images

            })

    return render_template(
        'students.html',
        students=students_data
    )

@app.route('/dashboard')

def dashboard():

    conn = sqlite3.connect(
        'attendance.db'
    )

    cursor = conn.cursor()

    # =========================
    # TOTAL STUDENTS
    # =========================

    cursor.execute(
        "SELECT COUNT(*) FROM students"
    )

    total_students = cursor.fetchone()[0]

    # =========================
    # TODAY ATTENDANCE
    # =========================

    today_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    cursor.execute("""

    SELECT COUNT(*)

    FROM attendance

    WHERE attendance_date=?

    """, (today_date,))

    today_attendance = (
        cursor.fetchone()[0]
    )

    # =========================
    # TOTAL DATASET
    # =========================

    dataset_path = "dataset"

    total_dataset = len(
        os.listdir(dataset_path)
    )

    # =========================
    # RECENT ATTENDANCE
    # =========================

    cursor.execute("""

    SELECT
        student_name,
        attendance_time,
        attendance_date

    FROM attendance

    ORDER BY id DESC

    LIMIT 10

    """)

    recent_attendance = (
        cursor.fetchall()
    )

    conn.close()

    return render_template(

        'dashboard.html',

        total_students=
            total_students,

        today_attendance=
            today_attendance,

        total_dataset=
            total_dataset,

        recent_attendance=
            recent_attendance

    )

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )