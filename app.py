import pickle
import tkinter as tk
from tkinter import ttk
from os import startfile
from tkinter import messagebox

import customtkinter as ctk
import cv2
from face_recognition import face_encodings
from PIL import Image

from core import create_session
from database import Database


def show_attendance_records():
    """
    It opens the attendance records folder.
    """
    startfile("attendance-records")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.width = 980
        self.height = 680

        # Get screen width and height to center the window
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)

        self.title("FaceTrackr")
        self.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        self.minsize(700, 500)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.home_icon = ctk.CTkImage(
            light_image=Image.open("assets/home-dark.png"),
            dark_image=Image.open("assets/home-light.png"),
            size=(20, 20),
        )
        self.admin_icon = ctk.CTkImage(
            light_image=Image.open("assets/admin-dark.png"),
            dark_image=Image.open("assets/admin-light.png"),
            size=(20, 20),
        )
        self.student_img_placeholder = ctk.CTkImage(
            light_image=Image.open("assets/add-student-dark.png"),
            dark_image=Image.open("assets/add-student-light.png"),
            size=(180, 180),
        )

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(
            self.navigation_frame,
            text="  FaceTrackr",
            image=ctk.CTkImage(Image.open("assets/icon.png"), size=(26, 26)),
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Home",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.home_icon,
            anchor="w",
            command=self.home_button_event,
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.admin_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Admin Panel",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.admin_icon,
            anchor="w",
            command=self.admin_button_event,
        )
        self.admin_button.grid(row=2, column=0, sticky="ew")

        ctk.CTkLabel(self.navigation_frame, text="Appearance Mode:", anchor="s").grid(
            row=5, column=0, padx=20, pady=(5, 0)
        )

        ctk.CTkOptionMenu(
            self.navigation_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event,
        ).grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=20)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(
            self.home_frame,
            text="",
            image=ctk.CTkImage(Image.open("assets/icon.png"), size=(250, 250)),
        ).grid(row=0, column=0, padx=30, pady=30)

        ctk.CTkButton(
            self.home_frame,
            text="Start New Session",
            width=300,
            height=100,
            font=("Courier New", 20, "bold"),
            command=create_session,
        ).grid(row=3, column=0, padx=30)

        ctk.CTkButton(
            self.home_frame,
            text="Show Attendance Records",
            width=300,
            height=100,
            font=("Courier New", 20, "bold"),
            command=show_attendance_records,
        ).grid(row=4, column=0, padx=30, pady=30)

        # Create Admin frame
        self.admin_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.admin_frame.grid_columnconfigure(0, weight=1)
        self.admin_frame.grid_rowconfigure(0, weight=1)

        # Create Admin Tabview
        self.admin_tabview = ctk.CTkTabview(self.admin_frame)
        self.admin_tabview.grid(
            row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        self.add_student_tab = self.admin_tabview.add("Add Student")
        self.manage_students_tab = self.admin_tabview.add("Manage Students")

        # Create Student Tab
        self.add_student_tab.grid_columnconfigure(0, weight=1)
        self.add_student_tab.grid_rowconfigure(0, weight=1)

        # Image section
        self.student_image_frame = ctk.CTkFrame(
            self.add_student_tab, fg_color="transparent"
        )
        self.student_image_frame.grid(row=0, column=0, sticky="n")

        self.student_image = ctk.CTkLabel(
            self.student_image_frame, text="", image=self.student_img_placeholder
        )
        self.student_image.grid(row=0, column=0, ipadx=20, ipady=20)

        ctk.CTkButton(
            self.student_image_frame,
            text="Upload Image",
            width=150,
            height=40,
            command=self.upload_image_button_event,
        ).grid(row=1, column=0, padx=10, pady=10)

        # Details section
        self.add_details_frame = ctk.CTkFrame(
            self.add_student_tab, fg_color="transparent"
        )
        self.add_details_frame.grid(
            row=0, column=3, rowspan=5, columnspan=2, sticky="nsew", padx=(20, 0)
        )
        self.add_details_frame.grid_columnconfigure(0, weight=1)
        self.add_details_frame.grid_columnconfigure(1, weight=3)

        ctk.CTkLabel(self.add_details_frame, text="Student ID:", font=("", 16)).grid(
            row=0, column=0, padx=(15, 2), pady=(70, 10)
        )
        self.student_id_text = tk.StringVar()
        ctk.CTkEntry(
            self.add_details_frame, width=400, textvariable=self.student_id_text
        ).grid(row=0, column=1, padx=(10, 10), pady=(70, 10))

        ctk.CTkLabel(self.add_details_frame, text="Full Name:", font=("", 16)).grid(
            row=1, column=0, padx=(15, 2), pady=10
        )
        self.student_name_text = tk.StringVar()
        ctk.CTkEntry(
            self.add_details_frame, width=400, textvariable=self.student_name_text
        ).grid(row=1, column=1, padx=(10, 10), pady=10)

        self.student_image_filepath = ""
        ctk.CTkButton(
            self.add_student_tab,
            text="Add Student",
            width=160,
            height=50,
            command=self.add_student_button_event,
        ).grid(row=9, column=0, columnspan=6, padx=(0, 20), pady=20)

        # Create Manage Students Tab
        self.manage_students_tab.grid_columnconfigure(0, weight=1)
        self.manage_students_tab.grid_columnconfigure(1, weight=1)
        self.manage_students_tab.grid_rowconfigure(0, weight=1)

        # Create Treeview
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure(
            "Treeview",
            background="#212121",
            foreground="#cee5e5",
            rowheight=50,
            fieldbackground="#212121",
            font=("Helvetica", 13),
        )
        self.style.map(
            "Treeview",
            background=[("selected", "gray70")],
            foreground=[("selected", "black")],
        )

        self.tree_frame = ctk.CTkFrame(self.manage_students_tab)
        self.tree_frame.grid(
            row=0, column=0, columnspan=2, sticky="nsew", padx=(20, 20), pady=(20, 0)
        )
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)

        self.style.configure(
            "Vertical.TScrollbar",
            troughcolor="#303030",
            gripcount=0,
            background="#505050",
            darkcolor="#303030",
            lightcolor="#505050",
            troughrelief="flat",
            arrowcolor="white",
        )

        self.style.map(
            "Vertical.TScrollbar",
            background=[
                ("active", "#424242"),
                ("disabled", "#424242"),
            ],
            darkcolor=[
                ("disabled", "#424242"),
            ],
            lightcolor=[
                ("disabled", "#424242"),
            ],
            troughcolor=[
                ("disabled", "#212121"),
            ],
            arrowcolor=[
                ("active", "white"),
                ("disabled", "white"),
            ],
        )
        self.tree_scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical")
        self.tree_scrollbar.grid(row=0, column=1, sticky="ns")

        self.student_treeview = ttk.Treeview(
            self.tree_frame,
            yscrollcommand=self.tree_scrollbar.set,
            selectmode="extended",
        )
        self.student_treeview.grid(row=0, column=0, sticky="nsew")
        self.tree_scrollbar.config(command=self.student_treeview.yview)

        self.student_treeview["columns"] = ("Student ID", "Name")
        self.student_treeview.column("#0", width=0, stretch="no")
        self.student_treeview.column("Student ID", anchor="center", stretch=True)
        self.student_treeview.column("Name", anchor="w", stretch=True)

        self.style.configure(
            "Treeview.Heading",
            font=("Helvetica", 16),
            padding=(10, 10),
            background="#505050",
            foreground="white",
        )
        self.style.map(
            "Treeview.Heading",
            background=[("hover", "#505050")],
        )
        self.student_treeview.heading("#0", text="", anchor="w")
        self.student_treeview.heading("Student ID", text="Student ID", anchor="center")
        self.student_treeview.heading("Name", text="Name", anchor="w")

        self.student_treeview.tag_configure("oddrow", background="#212121")
        self.student_treeview.tag_configure("evenrow", background="gray10")

        self.populate_treeview()

        # Add buttons to update and delete student
        ctk.CTkButton(
            self.manage_students_tab,
            text="Update Student Record",
            width=160,
            height=50,
            command=self.update_student_record,
        ).grid(row=2, column=0, padx=(20, 20), pady=20)

        ctk.CTkButton(
            self.manage_students_tab,
            text="Delete Student Record",
            width=160,
            height=50,
            command=self.delete_student_record,
        ).grid(row=2, column=1, padx=(20, 20), pady=20)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent"
        )
        self.admin_button.configure(
            fg_color=("gray75", "gray25") if name == "admin" else "transparent"
        )

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        else:
            self.home_frame.grid_forget()
        if name == "admin":
            self.admin_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.admin_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def admin_button_event(self):
        self.select_frame_by_name("admin")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def upload_image_button_event(self):
        self.student_image_filepath = tk.filedialog.askopenfilename(
            initialdir="~/",
            title="Select image",
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")],
        )
        new_student_image = ctk.CTkImage(
            light_image=Image.open(self.student_image_filepath), size=(180, 180)
        )
        self.student_image.configure(image=new_student_image)

    def add_student_button_event(self):
        # Check if all fields are filled
        if (
            self.student_id_text.get() == ""
            or self.student_name_text.get() == ""
            or self.student_image_filepath == ""
        ):
            messagebox.showerror("Error", "Please fill all the fields")
            return

        img = cv2.imread(self.student_image_filepath, cv2.COLOR_BGR2RGB)
        face_encoding = face_encodings(img)[0]
        img = cv2.resize(img, (216, 216))

        # Convert img and face_encoding to bytes
        img_bytes = cv2.imencode(".jpg", img)[1].tobytes()
        face_encoding_bytes = pickle.dumps(face_encoding)

        # Insert student into database
        db = Database("student.db")
        db.insert(
            self.student_id_text.get(),
            self.student_name_text.get(),
            img_bytes,
            face_encoding_bytes,
        )
        del db

        # Show success message
        messagebox.showinfo("Success", "Student added successfully")

        # Reset fields
        self.student_id_text.set("")
        self.student_name_text.set("")
        self.student_image.configure(image=self.student_img_placeholder)

        # Update treeview
        self.populate_treeview()

    def populate_treeview(self):
        # Clear treeview
        self.student_treeview.delete(*self.student_treeview.get_children())

        # Get all students from database
        db = Database("student.db")
        for count, student in enumerate(db.fetch_id_and_name()):
            if not count % 2:
                self.student_treeview.insert(
                    parent="",
                    index="end",
                    iid=count,
                    text="",
                    values=student,
                    tags=("evenrow",),
                )
            else:
                self.student_treeview.insert(
                    parent="",
                    index="end",
                    iid=count,
                    text="",
                    values=student,
                    tags=("oddrow",),
                )
        del db

    def update_student_record(self):  # sourcery skip: use-named-expression
        selection = self.student_treeview.focus()
        if selection:
            id, name = self.student_treeview.item(selection, "values")

            self.update_window = ctk.CTkToplevel(self)

            self.update_window.title("Update Student")
            update_win_x = (self.screen_width / 2) - (400 / 2)
            update_win_y = (self.screen_height / 2) - (150 / 2)

            self.update_window.geometry(
                f"400x150+{int(update_win_x)}+{int(update_win_y)}"
            )
            self.update_window.grid_columnconfigure(0, weight=1)
            self.update_window.grid_columnconfigure(1, weight=5)
            self.update_window.grid_rowconfigure(3, weight=1)

            # Student ID
            student_id_label = ctk.CTkLabel(self.update_window, text="Student ID:")
            student_id_label.grid(row=0, column=0, padx=10, pady=10)

            student_id_entry = ctk.CTkEntry(
                self.update_window,
                textvariable=tk.StringVar(value=id),
                state="disabled",
            )
            student_id_entry.grid(row=0, column=1, padx=10, pady=10)

            # Student Name
            student_name_label = ctk.CTkLabel(self.update_window, text="Student Name:")
            student_name_label.grid(row=1, column=0, padx=10, pady=10)
            student_name_entry = ctk.CTkEntry(
                self.update_window, textvariable=tk.StringVar(value=name)
            )
            student_name_entry.grid(row=1, column=1, padx=10, pady=10)

            # Update Button
            update_student_button = ctk.CTkButton(
                self.update_window,
                text="Update Record",
                command=lambda: self.update_database_record(
                    id, student_name_entry.get()
                ),
            )
            update_student_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def update_database_record(self, id, name):
        db = Database("student.db")
        db.update_name(id, name)
        del db
        self.populate_treeview()
        self.update_window.destroy()

    def delete_student_record(self):  # sourcery skip: use-named-expression
        selection = self.student_treeview.focus()
        if selection:
            id, name = self.student_treeview.item(selection, "values")
            if messagebox.askyesno(
                "Delete Student", f"Are you sure you want to delete {name} ({id})?"
            ):
                db = Database("student.db")
                db.remove(id)
                del db
                self.populate_treeview()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = App()
    app.wm_iconbitmap(default="assets/icon.ico")
    app.mainloop()
