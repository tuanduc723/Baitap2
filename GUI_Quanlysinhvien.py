import tkinter as tk
from tkinter import messagebox, ttk

class QuanlysinhvienGUI:
    def __init__(self, root, db_connection):
        self.root = root
        self.db_connection = db_connection
    
        # Các nhãn và ô nhập liệu
        tk.Label(root, text="Tên:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_name = tk.Entry(root)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Tuổi:").grid(row=0, column=2, padx=10, pady=5)
        self.entry_age = tk.Entry(root)
        self.entry_age.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(root, text="Giới tính:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_gender = tk.Entry(root)
        self.entry_gender.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Ngành học:").grid(row=1, column=2, padx=10, pady=5)
        self.entry_major = tk.Entry(root)
        self.entry_major.grid(row=1, column=3, padx=10, pady=5)

        # Các nút hành động
        self.btn_add = tk.Button(root, text="Thêm sinh viên", command=self.add_student)
        self.btn_add.grid(row=2, column=0, padx=10, pady=5)

        self.btn_update = tk.Button(root, text="Cập nhật thông tin", command=self.update_student)
        self.btn_update.grid(row=2, column=1, padx=10, pady=5)

        self.btn_delete = tk.Button(root, text="Xóa sinh viên", command=self.delete_student)
        self.btn_delete.grid(row=2, column=2, padx=10, pady=5)

        self.btn_reload = tk.Button(root, text="Tải lại danh sách", command=self.load_students)
        self.btn_reload.grid(row=2, column=3, padx=10, pady=5)

        # Treeview để hiển thị danh sách sinh viên
        self.tree = ttk.Treeview(root, columns=("ID", "Tên", "Tuổi", "Giới tính", "Ngành"), show="headings")
        self.tree.grid(row=3, column=0, columnspan=4, padx=10, pady=5)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Tuổi", text="Tuổi")
        self.tree.heading("Giới tính", text="Giới tính")
        self.tree.heading("Ngành", text="Ngành")

        # Tải danh sách sinh viên khi ứng dụng bắt đầu
        self.load_students()

    def load_students(self):
        conn = self.db_connection
        if conn is None:
            return
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)  # Xóa các dòng hiện có trong treeview
            cur = conn.cursor()
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    def add_student(self):
        name = self.entry_name.get()
        age = self.entry_age.get()
        gender = self.entry_gender.get()
        major = self.entry_major.get()

        if not all([name, age, gender, major]):
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng điền đầy đủ thông tin!")
            return

        conn = self.db_connection
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)",
                (name, age, gender, major)
            )
            conn.commit()
            self.load_students()
            messagebox.showinfo("Thành công", "Sinh viên đã được thêm!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm sinh viên: {e}")

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Lỗi chọn", "Vui lòng chọn sinh viên để cập nhật!")
            return

        student_id = self.tree.item(selected[0], 'values')[0]
        name = self.entry_name.get()
        age = self.entry_age.get()
        gender = self.entry_gender.get()
        major = self.entry_major.get()

        if not all([name, age, gender, major]):
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng điền đầy đủ thông tin!")
            return

        conn = self.db_connection
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE students SET name=%s, age=%s, gender=%s, major=%s WHERE id=%s",
                (name, age, gender, major, student_id)
            )
            conn.commit()
            self.load_students()
            messagebox.showinfo("Thành công", "Thông tin sinh viên đã được cập nhật!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật sinh viên: {e}")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Lỗi chọn", "Vui lòng chọn sinh viên để xóa!")
            return

        student_id = self.tree.item(selected[0], 'values')[0]
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này?")
        if not confirm:
            return

        conn = self.db_connection
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
            conn.commit()
            self.load_students()
            messagebox.showinfo("Thành công", "Sinh viên đã được xóa!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa sinh viên: {e}")
