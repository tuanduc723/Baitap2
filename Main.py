import tkinter as tk
from tkinter import ttk
import psycopg2
from GUI_Dangnhap import DangnhapGUI
from GUI_Quanlysinhvien import QuanlysinhvienGUI
from GUI_Quanlykhoa import QuanlykhoaGUI  # Import tab mới

class MainApp:
    def __init__(self):
        self.db_connection = None

    def run(self):
        # Đăng nhập
        self.root = tk.Tk()
        self.root.title("Đăng nhập")
        login_gui = DangnhapGUI(self.root)
        self.root.mainloop()

        if login_gui.nguoidungdangnhap(login_gui.username_entry.get(), login_gui.password_entry.get()):
            self.db_connection = psycopg2.connect(
                dbname="students",
                user=login_gui.username_entry.get(),
                password=login_gui.password_entry.get(),
                host="localhost",
                port="5432"
            )
            # Chuyển sang giao diện chính
            self.root = tk.Tk()
            self.root.title("Hệ thống quản lý")
            
            # Sử dụng Notebook cho các tab
            notebook = ttk.Notebook(self.root)
            notebook.pack(fill="both", expand=True)

            # Tab quản lý sinh viên
            QuanlysinhvienGUI(notebook, self.db_connection)

            # Tab quản lý khoa và chuyên ngành
            QuanlykhoaGUI(notebook, self.db_connection)

            self.root.mainloop()

        if self.db_connection:
            self.db_connection.close()

if __name__ == "__main__":
    app = MainApp()
    app.run()
