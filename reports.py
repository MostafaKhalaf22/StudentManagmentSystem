import tkinter as tk
from tkinter import ttk
from database import get_connection

class ReportsWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Reports - Student Management System")
        self.window.geometry("600x500")
        self.build_ui()
        self.load_reports()

    def build_ui(self):
        tk.Label(self.window, text="Reports & Statistics",
                 font=("Arial", 14, "bold")).pack(pady=10)

        # إحصائيات عامة
        self.stats_frame = tk.Frame(self.window, bd=2, relief=tk.GROOVE)
        self.stats_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(self.stats_frame, text="General Statistics",
                 font=("Arial", 12, "bold")).pack(pady=5)

        self.total_label = tk.Label(self.stats_frame, text="Total Students: -",
                                     font=("Arial", 11))
        self.total_label.pack()

        self.highest_label = tk.Label(self.stats_frame, text="Highest Grade: -",
                                       font=("Arial", 11))
        self.highest_label.pack()

        self.lowest_label = tk.Label(self.stats_frame, text="Lowest Grade: -",
                                      font=("Arial", 11))
        self.lowest_label.pack()

        self.avg_label = tk.Label(self.stats_frame, text="Overall Average: -",
                                   font=("Arial", 11))
        self.avg_label.pack(pady=5)

        tk.Label(self.window, text="Failed Students (Below 50)",
                 font=("Arial", 12, "bold"), fg="red").pack(pady=10)

        columns = ("Name", "Student ID", "Subject", "Grade")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                  show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        self.tree.pack(padx=20, fill=tk.BOTH, expand=True)

    def load_reports(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM students")
        total = cursor.fetchone()[0]
        self.total_label.config(text=f"Total Students: {total}")

        cursor.execute("SELECT MAX(grade) FROM grades")
        highest = cursor.fetchone()[0]
        self.highest_label.config(text=f"Highest Grade: {highest if highest else '-'}")

        cursor.execute("SELECT MIN(grade) FROM grades")
        lowest = cursor.fetchone()[0]
        self.lowest_label.config(text=f"Lowest Grade: {lowest if lowest else '-'}")

        cursor.execute("SELECT AVG(grade) FROM grades")
        avg = cursor.fetchone()[0]
        self.avg_label.config(text=f"Overall Average: {f'{avg:.2f}' if avg else '-'}")

        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor.execute("""
            SELECT s.name, s.student_id, g.subject, g.grade
            FROM students s
            JOIN grades g ON s.student_id = g.student_id
            WHERE g.grade < 50
            ORDER BY g.grade ASC
        """)
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

        conn.close()