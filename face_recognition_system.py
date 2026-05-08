import face_recognition
import cv2
import os
import numpy as np
import pandas as pd

from datetime import datetime

from gtts import gTTS
from playsound import playsound

from PIL import Image, ImageDraw, ImageFont

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

while True:

    ret, frame = video_capture.read()

    if not ret:
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

                speak_vietnamese(
                    f"{name} đã điểm danh rồi nhé"
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
        # HIỂN THỊ TIẾNG VIỆT
        # =========================

        pil_image = Image.fromarray(
            cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )
        )

        draw = ImageDraw.Draw(pil_image)

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

    cv2.imshow(
        "AI Face Recognition Attendance System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()

cv2.destroyAllWindows()