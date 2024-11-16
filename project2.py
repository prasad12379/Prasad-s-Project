import streamlit as st
import json
from typing import List

# File where student data will be stored
STUDENT_DATA_FILE = 'students.json'

class Student:
    def __init__(self, roll_no, name, age, marks):
        self.roll_no = roll_no
        self.name = name
        self.age = age
        self.marks = marks

    def __str__(self):
        return f"Roll No: {self.roll_no}, Name: {self.name}, Age: {self.age}, Marks: {self.marks}"

    def update_details(self, name=None, age=None, marks=None):
        if name:
            self.name = name
        if age:
            self.age = age
        if marks:
            self.marks = marks

# Helper function to load students from the file
def load_students():
    try:
        with open(STUDENT_DATA_FILE, 'r') as file:
            students_data = json.load(file)
            students = [Student(student['roll_no'], student['name'], student['age'], student['marks']) for student in students_data]
            return students
    except FileNotFoundError:
        return []

# Helper function to save students to the file
def save_students(students):
    with open(STUDENT_DATA_FILE, 'w') as file:
        students_data = [{'roll_no': student.roll_no, 'name': student.name, 'age': student.age, 'marks': student.marks} for student in students]
        json.dump(students_data, file)

# Database class (now using file storage)
class StudentDatabase:
    def __init__(self):
        self.students = load_students()

    def add_student(self, student: Student):
        self.students.append(student)
        save_students(self.students)

    def delete_student(self, roll_no: int):
        for student in self.students:
            if student.roll_no == roll_no:
                self.students.remove(student)
                save_students(self.students)
                return f"Student with Roll No {roll_no} deleted."
        return "Student not found."

    def search_student(self, roll_no: int):
        for student in self.students:
            if student.roll_no == roll_no:
                return str(student)
        return "Student not found."

    def update_student(self, roll_no: int, name=None, age=None, marks=None):
        for student in self.students:
            if student.roll_no == roll_no:
                student.update_details(name, age, marks)
                save_students(self.students)
                return f"Student with Roll No {roll_no} updated."
        return "Student not found."

    def display_students(self):
        if not self.students:
            return "No students in database."
        
        student_display = ""
        for student in self.students:
            student_display += f"Roll No: {student.roll_no}, Name: {student.name}, Age: {student.age}, Marks: {student.marks}<br>"  # Add <br> for line breaks
        
        return student_display

    def sort_students_by_name(self):
        self.students.sort(key=lambda student: student.name)
        save_students(self.students)
        return self.get_sorted_students_display()

    def sort_students_by_age(self):
        self.students.sort(key=lambda student: student.age)
        save_students(self.students)
        return self.get_sorted_students_display()

    def sort_students_by_marks(self):
        self.students.sort(key=lambda student: student.marks, reverse=True)
        save_students(self.students)
        return self.get_sorted_students_display()

    def sort_students_by_roll_no(self):
        self.students.sort(key=lambda student: student.roll_no)
        save_students(self.students)
        return self.get_sorted_students_display()

    def get_sorted_students_display(self):
        if not self.students:
            return "No students to display."

        sorted_students_display = ""
        for student in self.students:
            sorted_students_display += f"Roll No: {student.roll_no}, Name: {student.name}, Age: {student.age}, Marks: {student.marks}<br>"  # Add <br> for line breaks

        return sorted_students_display

# Initialize database
db = StudentDatabase()

# Streamlit UI with enhanced styles
st.markdown("""
    <style>
        /* Main Background Gradient */
        body {
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* Title Styling - Larger font size */
        .css-1v0mbdj {
            font-size: 48px; /* Increased font size for title */
            font-weight: bold;
            color: black;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);  /* Slight shadow for contrast */
        }

        /* Header Styling - Reduced font size */
        h1, h2, h3 {
            color: black;
            font-size: 32px;  /* Reduced font size for headers */
            font-family: 'Segoe UI', sans-serif;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);  /* Slight shadow for contrast */
            text-align: center;
            text-transform: uppercase;
        }

        /* Sidebar Background */
        .css-1d391kg {
            background-color: #292b2c;
        }

        /* Sidebar Text Color */
        .css-1d391kg .css-1rsu4hm {
            color: #fff;
            font-size: 18px;
        }

        /* Button Styling */
        .stButton>button {
            background-color: #ff7e5f;
            color: white;
            border-radius: 10px;
            padding: 15px 30px;
            font-weight: bold;
            font-size: 16px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #feb47b;
        }

        /* Input Fields Styling */
        .stTextInput>div>input, .stNumberInput>div>input {
            background-color: #ffffff;
            border: 2px solid #ff7e5f;
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
        }

        /* Enhanced Div Containers */
        .css-1h6q7u6 {
            padding: 15px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.8);
            margin-bottom: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Add Emoji to Buttons and Text */
        .emoji {
            font-size: 24px;
            padding-right: 10px;
        }

        /* Add Graphics and Effects */
        .stImage img {
            border-radius: 12px;
            border: 5px solid #feb47b;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
        }

    </style>
""", unsafe_allow_html=True)

# Title (st.title) will use custom CSS styling
st.markdown("<h1 class='css-1v0mbdj'>Student Database Management System </h1>", unsafe_allow_html=True)

# Sidebar options with emojis
option = st.sidebar.selectbox("Select Operation", [
    "📝 Add Student", 
    "✏️ Update Student", 
    "❌ Delete Student", 
    "🔍 Search Student", 
    "👥 Display Students", 
    "🔄 Sort Students"
])

# Add Student
if option == "📝 Add Student":
    st.header("Add a New Student ")
    roll_no = st.number_input("🎫 Roll No", min_value=1, step=1)
    name = st.text_input("👤 Name")
    age = st.number_input("🎂 Age", min_value=1, step=1)
    marks = st.number_input("📊 Marks", min_value=0, max_value=100, step=1)

    if st.button("Add Student 🚀"):
        if name and roll_no and age and marks is not None:
            student = Student(roll_no, name, age, marks)
            db.add_student(student)
            st.success(f"Student with Roll No {roll_no} added successfully! 🎉")
        else:
            st.error("❗ Please fill all the details.")

# Update Student
elif option == "✏️ Update Student":
    st.header("Update Student Details ✏️")
    roll_no = st.number_input("Enter Roll No to Update", min_value=1, step=1)
    
    student_details = db.search_student(roll_no)
    if student_details == "Student not found.":
        st.error(student_details)
    else:
        st.write(student_details)
        name = st.text_input("New Name (leave blank to keep the same)")
        age = st.number_input("New Age (leave blank to keep the same)", min_value=1, step=1)
        marks = st.number_input("New Marks (leave blank to keep the same)", min_value=0, max_value=100, step=1)

        if st.button("Update Student 🛠️"):
            updated = db.update_student(roll_no, name or None, age or None, marks or None)
            st.success(updated)

# Delete Student
elif option == "❌ Delete Student":
    st.header("Delete Student 🗑️")
    roll_no = st.number_input("Enter Roll No to Delete", min_value=1, step=1)

    if st.button("Delete Student 🔥"):
        result = db.delete_student(roll_no)
        st.write(result)

# Search Student
elif option == "🔍 Search Student":
    st.header("Search Student by Roll No 🔍")
    roll_no = st.number_input("Enter Roll No to Search", min_value=1, step=1)
    
    student_details = db.search_student(roll_no)
    st.write(student_details)

# Display Students
elif option == "👥 Display Students":
    st.header("All Students 📜")
    students_display = db.display_students()
    st.markdown(students_display, unsafe_allow_html=True)

# Sort Students
elif option == "🔄 Sort Students":
    st.header("Sort Students by Criteria 🔄")
    sort_option = st.selectbox("Select Sorting Criteria", ["By Name", "By Age", "By Marks", "By Roll No"])

    if sort_option == "By Name":
        sorted_students = db.sort_students_by_name()
        st.markdown(sorted_students, unsafe_allow_html=True)
    elif sort_option == "By Age":
        sorted_students = db.sort_students_by_age()
        st.markdown(sorted_students, unsafe_allow_html=True)
    elif sort_option == "By Marks":
        sorted_students = db.sort_students_by_marks()
        st.markdown(sorted_students, unsafe_allow_html=True)
    elif sort_option == "By Roll No":
        sorted_students = db.sort_students_by_roll_no()
        st.markdown(sorted_students, unsafe_allow_html=True)
