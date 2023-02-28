import pickle
import tkinter as tk
from os import startfile
from tkinter import messagebox

import customtkinter as ctk
import cv2
from face_recognition import face_encodings
from PIL import Image

from core import create_session
from database import Database


def show_attendance_records():
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

        # load images with light and dark mode image
        self.logo_image = ctk.CTkImage(
            Image.open("assets/CustomTkinter_logo_single.png"),
            size=(26, 26),
        )
        self.home_image = ctk.CTkImage(
            light_image=Image.open("assets/home-dark.png"),
            dark_image=Image.open("assets/home-light.png"),
            size=(20, 20),
        )
        self.admin_image = ctk.CTkImage(
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

        self.navigation_frame_label = ctk.CTkLabel(
            self.navigation_frame,
            text="  FaceTrackr",
            image=self.logo_image,
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Home",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.home_image,
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
            image=self.admin_image,
            anchor="w",
            command=self.admin_button_event,
        )
        self.admin_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_label = ctk.CTkLabel(
            self.navigation_frame, text="Appearance Mode:", anchor="s"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(5, 0))

        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)

        self.start_new_session_button = ctk.CTkButton(
            self.home_frame,
            text="Start New Session",
            width=300,
            height=100,
            font=("Courier New", 20, "bold"),
            command=create_session,
        )
        self.start_new_session_button.grid(row=3, column=0, padx=30)

        self.show_attendance_records_button = ctk.CTkButton(
            self.home_frame,
            text="Show Attendance Records",
            width=300,
            height=100,
            font=("Courier New", 20, "bold"),
            command=show_attendance_records,
        )
        self.show_attendance_records_button.grid(row=4, column=0, padx=30, pady=30)

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
        self.admin_tabview.add("View Students")

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
            self.student_image_frame, text="Upload Image", width=150, height=40, command=self.upload_image_button_event
        ).grid(row=1, column=0, padx=10, pady=10)

        # Details section
        self.add_details_frame = ctk.CTkFrame(self.add_student_tab, fg_color="transparent")
        self.add_details_frame.grid(
            row=0, column=3, rowspan=5, columnspan=2, sticky="nsew", padx=(20, 0)
        )
        self.add_details_frame.grid_columnconfigure(0, weight=1)
        self.add_details_frame.grid_columnconfigure(1, weight=3)

        ctk.CTkLabel(self.add_details_frame, text="Student ID:", font=("", 18)).grid(row=0, column=0, padx=(15, 2), pady=(70, 10))
        self.student_id_text = tk.StringVar()
        self.student_id_entry = ctk.CTkEntry(self.add_details_frame, width=400, textvariable=self.student_id_text).grid(row=0, column=1, padx=(10, 10), pady=(70, 10))

        ctk.CTkLabel(self.add_details_frame, text="Full Name:", font=("", 18)).grid(row=1, column=0, padx=(15, 2), pady=10)
        self.student_name_text = tk.StringVar()
        self.student_name_entry = ctk.CTkEntry(self.add_details_frame, width=400, textvariable=self.student_name_text).grid(row=1, column=1, padx=(10, 10), pady=10)

        self.student_image_filepath = ''
        self.add_student_button = ctk.CTkButton(self.add_student_tab, text="Add Student", width=160, height=50, command=self.add_student_button_event)
        self.add_student_button.grid(row=9, column=0, columnspan=6, padx=(0, 20), pady=20)

        # select default frame
        # self.select_frame_by_name("home")
        self.select_frame_by_name("admin")

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
            self.home_frame.grid(row=0, column=1, sticky="nsew")
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
            initialdir="./Student_DB", title="Select image", filetypes=[("Image Files", "*.jpg *.png *.jpeg")],
        )
        new_student_image = ctk.CTkImage(light_image=Image.open(self.student_image_filepath), size=(180, 180))
        self.student_image.configure(image=new_student_image)

    def add_student_button_event(self):
        # Check if all fields are filled
        if self.student_id_text.get() == '' or self.student_name_text.get() == '' or self.student_image_filepath == '':
            messagebox.showerror("Error", "Please fill all the fields")
            return
        
        img = cv2.imread(self.student_image_filepath, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (216, 216))
        face_encoding = face_encodings(img)[0]

        # Convert img and face_encoding to bytes
        img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
        face_encoding_bytes = pickle.dumps(face_encoding)

        # Insert student into database
        db = Database("student.db")
        db.insert(self.student_id_text.get(), self.student_name_text.get(), img_bytes, face_encoding_bytes)
        del db
        
        # Show success message
        messagebox.showinfo("Success", "Student added successfully")

        # Reset fields
        self.student_id_text.set('')
        self.student_name_text.set('')
        self.student_image.configure(image=self.student_img_placeholder)


if __name__ == "__main__":
    ctk.set_default_color_theme("dark-blue")
    app = App()
    app.mainloop()
