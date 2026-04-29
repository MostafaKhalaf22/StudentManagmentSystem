import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

def open_dashboard():
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard - Student Management System")
        self.root.geometry("700x500")
        self.build_ui()
        self.load_students()

    def build_ui(self):
        tk.Label(self.root, text="Student Management System",
                 font=("Arial", 16, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Student", bg="green", fg="white",
                  font=("Arial", 10),
                  command=self.open_add_student).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Grades", bg="blue", fg="white",
                  font=("Arial", 10),
                  command=self.open_grades).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="Reports", bg="orange", fg="white",
                  font=("Arial", 10),
                  command=self.open_reports).grid(row=0, column=2, padx=5)

        tk.Button(btn_frame, text="Delete Student", bg="red", fg="white",
                  font=("Arial", 10),
                  command=self.delete_student).grid(row=0, column=3, padx=5)

        tk.Button(btn_frame, text="Search", bg="purple", fg="white",
                  font=("Arial", 10),
                  command=self.open_search).grid(row=0, column=4, padx=5)

        columns = ("ID", "Name", "Student ID", "Major")
        self.tree = ttk.Treeview(self.root, columns=columns,
                                  show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def load_students(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()

    def open_add_student(self):
        from student_form import StudentForm
        StudentForm(self.root, self.load_students)

    def open_grades(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student first!")
            return
        student = self.tree.item(selected[0])["values"]
        from grades import GradesWindow
        GradesWindow(self.root, student[2])

    def open_reports(self):
        from reports import ReportsWindow
        ReportsWindow(self.root)

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student first!")
            return
        student = self.tree.item(selected[0])["values"]
        confirm = messagebox.askyesno("Confirm", f"Delete {student[1]}?")
        if confirm:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE student_id=?",
                           (student[2],))
            cursor.execute("DELETE FROM grades WHERE student_id=?",
                           (student[2],))
            conn.commit()
            conn.close()
            self.load_students()

    def open_search(self):
        from search import SearchWindow
        SearchWindow(self.root, self.load_students)