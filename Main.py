import tkinter as tk
import psycopg2
from GUI_Dangnhap import DangnhapGUI
from GUI_Quanlysinhvien import QuanlysinhvienGUI

class MainApp:
    def __init__(self):
        self.db_connection = None

    def run(self):
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
            self.root = tk.Tk()
            self.root.title("Quản lý sinh viên")
            
            QuanlysinhvienGUI(self.root, self.db_connection)
            self.root.mainloop()

        if self.db_connection:
            self.db_connection.close()

if __name__ == "__main__":
    app = MainApp()
    app.run()
