import tkinter as tk
from tkinter import messagebox
import psycopg2

class DangnhapGUI:
    def __init__(self, root):        
        self.root = root
        
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.nguoidungdangnhap(username, password):
            messagebox.showinfo("Login", "Đăng nhập thành công")
            self.root.quit()  # Thoát khỏi giao diện đăng nhập
        else:
            messagebox.showerror("Login", "Đăng nhập thất bại.")

    def nguoidungdangnhap(self, username, password):
        try:
            connection = psycopg2.connect(
                dbname="students",
                user=username,
                password=password,
                host="localhost",
                port="5432"
            )
            connection.close()
            return True
        except Exception as e:
            return False
