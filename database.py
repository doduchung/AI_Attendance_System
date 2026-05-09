import sqlite3

# =========================
# CONNECT DATABASE
# =========================

conn = sqlite3.connect(
    'attendance.db'
)

cursor = conn.cursor()

# =========================
# TABLE STUDENTS
# =========================

cursor.execute("""

CREATE TABLE IF NOT EXISTS students(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    folder_name TEXT

)

""")

# =========================
# TABLE ATTENDANCE
# =========================

cursor.execute("""

CREATE TABLE IF NOT EXISTS attendance(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_name TEXT,

    attendance_time TEXT,

    attendance_date TEXT

)

""")

conn.commit()

conn.close()

print("Database created successfully")