import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

# ---------- DATABASE ----------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()

# ---------- PASSWORD HASH ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- REGISTER ----------
def register():
    username = user_entry.get().strip()
    password = pass_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Fill all fields")
        return

    hashed = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, hashed)
        )
        conn.commit()
        messagebox.showinfo("Success", "Account Created!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

# ---------- LOGIN ----------
def login():
    username = user_entry.get().strip()
    password = hash_password(pass_entry.get())

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    if cursor.fetchone():
        messagebox.showinfo("Welcome", f"Hello {username}!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# ---------- GUI ----------
root = tk.Tk()
root.title("Modern Login System")
root.geometry("420x520")
root.configure(bg="#1e1e2e")
root.resizable(False, False)

# Card Frame
frame = tk.Frame(root, bg="#2a2a40", padx=25, pady=25)
frame.place(relx=0.5, rely=0.5, anchor="center")

title = tk.Label(
    frame,
    text="LOGIN SYSTEM",
    font=("Segoe UI", 22, "bold"),
    fg="white",
    bg="#2a2a40"
)
title.pack(pady=20)

# Username
tk.Label(
    frame,
    text="Username",
    bg="#2a2a40",
    fg="white",
    font=("Segoe UI", 11)
).pack(anchor="w")

user_entry = tk.Entry(
    frame,
    font=("Segoe UI", 12),
    width=25,
    relief="flat",
    bg="#3a3a5a",
    fg="white",
    insertbackground="white"
)
user_entry.pack(ipady=8, pady=10)

# Password
tk.Label(
    frame,
    text="Password",
    bg="#2a2a40",
    fg="white",
    font=("Segoe UI", 11)
).pack(anchor="w")

pass_entry = tk.Entry(
    frame,
    show="*",
    font=("Segoe UI", 12),
    width=25,
    relief="flat",
    bg="#3a3a5a",
    fg="white",
    insertbackground="white"
)
pass_entry.pack(ipady=8, pady=10)

# Login Button
login_btn = tk.Button(
    frame,
    text="Login",
    font=("Segoe UI", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    relief="flat",
    width=20,
    command=login
)
login_btn.pack(pady=15)

# Register Button
register_btn = tk.Button(
    frame,
    text="Create Account",
    font=("Segoe UI", 11),
    bg="#2196F3",
    fg="white",
    relief="flat",
    width=20,
    command=register
)
register_btn.pack()

footer = tk.Label(
    frame,
    text="Python • Tkinter • SQLite",
    bg="#2a2a40",
    fg="gray",
    font=("Segoe UI", 9)
)
footer.pack(pady=20)

root.mainloop()
