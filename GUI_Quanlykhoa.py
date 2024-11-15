import tkinter as tk
from tkinter import messagebox, ttk

class QuanlykhoaGUI:
    def __init__(self, parent, db_connection):
        self.db_connection = db_connection

        # Frame gắn vào tab chính
        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Quản lý Khoa và Chuyên ngành")

        # Các nhãn và ô nhập liệu
        tk.Label(self.frame, text="Tên Khoa:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_department_name = tk.Entry(self.frame)
        self.entry_department_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.frame, text="Tên Chuyên ngành:").grid(row=0, column=2, padx=10, pady=5)
        self.entry_major_name = tk.Entry(self.frame)
        self.entry_major_name.grid(row=0, column=3, padx=10, pady=5)

        # Các nút hành động
        tk.Button(self.frame, text="Thêm Khoa", command=self.add_department).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(self.frame, text="Thêm Chuyên ngành", command=self.add_major).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.frame, text="Tải lại danh sách", command=self.load_departments).grid(row=1, column=2, padx=10, pady=5)

        # Treeview
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Khoa", "Chuyên ngành"), show="headings")
        self.tree.grid(row=2, column=0, columnspan=4, padx=10, pady=5)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Khoa", text="Khoa")
        self.tree.heading("Chuyên ngành", text="Chuyên ngành")

        # Tải dữ liệu khi khởi động
        self.load_departments()

    def load_departments(self):
        conn = self.db_connection
        if conn is None:
            return
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)  # Xóa dữ liệu cũ
            cur = conn.cursor()
            cur.execute("""
                SELECT majors.id, departments.name, majors.name 
                FROM majors 
                JOIN departments ON majors.department_id = departments.id
            """)
            rows = cur.fetchall()
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    def add_department(self):
        department_name = self.entry_department_name.get()
        if not department_name:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập tên Khoa!")
            return

        conn = self.db_connection
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO departments (name) VALUES (%s)", (department_name,))
            conn.commit()
            self.load_departments()
            messagebox.showinfo("Thành công", "Khoa đã được thêm!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm Khoa: {e}")

    def add_major(self):
        major_name = self.entry_major_name.get()
        department_name = self.entry_department_name.get()
        if not all([major_name, department_name]):
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng điền đầy đủ thông tin!")
            return

        conn = self.db_connection
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT id FROM departments WHERE name=%s", (department_name,))
            department_id = cur.fetchone()
            if not department_id:
                messagebox.showerror("Lỗi", "Khoa không tồn tại!")
                return
            cur.execute("INSERT INTO majors (name, department_id) VALUES (%s, %s)", (major_name, department_id[0]))
            conn.commit()
            self.load_departments()
            messagebox.showinfo("Thành công", "Chuyên ngành đã được thêm!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm Chuyên ngành: {e}")
