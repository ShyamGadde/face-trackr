import os

import customtkinter as ctk
from PIL import Image

from core import create_session

ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.width = 1080
        self.height = 720

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
        self.add_student_image = ctk.CTkImage(
            light_image=Image.open("assets/add-student-dark.png"),
            dark_image=Image.open("assets/add-student-light.png"),
            size=(20, 20),
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
            self.navigation_frame, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(5, 0))

        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.start_new_session_button = ctk.CTkButton(
            self.home_frame,
            text="Start New Session",
            width=300,
            height=100,
            font=("Courier New", 20, "bold"),

        )
        self.start_new_session_button.grid(row=3, column=0, padx=30, pady=20)
        self.start_new_session_button.place(relx=0.5, rely=0.5, anchor="center")

        self.show_attendance_records_button = ctk.CTkButton(
            self.home_frame,
            text="Show Attendance Records",
            width=300,
            height=100,
            font=("Courier New", 20, "bold"),
        )
        self.show_attendance_records_button.grid(row=4, column=0, padx=30, pady=20)
        self.show_attendance_records_button.place(relx=0.5, rely=0.7, anchor="center")

        # create second frame
        self.admin_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
    # create_session()
