import tkinter as tk
from tkinter import messagebox
#from database import get_connection

class EditStudentWindow:
    def __init__(self, parent, student, refresh_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Edit Student")
        self.window.geometry("400x350")
        self.window.resizable(False, False)
        self.student = student
        self.refresh_callback = refresh_callback
        self.build_ui()
        self.fill_data()

    def build_ui(self):
        tk.Label(self.window, text="Edit Student",
                 font=("Arial", 14, "bold")).pack(pady=15)

        tk.Label(self.window, text="Full Name:",
                 font=("Arial", 11)).pack()
        self.name_entry = tk.Entry(self.window, font=("Arial", 11), width=30)
        self.name_entry.pack(pady=5)

        tk.Label(self.window, text="Student ID:",
                 font=("Arial", 11)).pack()
        self.id_entry = tk.Entry(self.window, font=("Arial", 11), width=30)
        self.id_entry.pack(pady=5)

        tk.Label(self.window, text="Major:",
                 font=("Arial", 11)).pack()
        self.major_entry = tk.Entry(self.window, font=("Arial", 11), width=30)
        self.major_entry.pack(pady=5)

        tk.Button(self.window, text="Save Changes", bg="green", fg="white",
                  font=("Arial", 11), command=self.save).pack(pady=20)

    def fill_data(self):
        self.name_entry.insert(0, self.student[1])
        self.id_entry.insert(0, self.student[2])
        self.major_entry.insert(0, self.student[3])

    def save(self):
        name = self.name_entry.get().strip()
        student_id = self.id_entry.get().strip()
        major = self.major_entry.get().strip()

        if not name or not student_id or not major:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return
'''
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE students SET name=?, student_id=?, major=?
                WHERE id=?
            """, (name, student_id, major, self.student[0]))
            conn.commit()
            messagebox.showinfo("Success", "Student updated successfully!")
            self.refresh_callback()
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong!\n{e}")
        finally:
            conn.close()
            '''