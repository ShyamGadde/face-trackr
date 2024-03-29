# FaceTrackr - Real Time Attendance Management System

FaceTrackr is a real-time attendance management system written in Python using OpenCV and face recognition libraries. It was designed to streamline attendance taking, eliminating the need for manual attendance records and ensuring touch-free attendance taking during the COVID-19 pandemic.

## Features

- Real-time face detection and recognition for attendance marking
- User-friendly GUI for easy management of student data with different appearance modes(dark, light or system default).
- CRUD operations (create, read, update, delete) available for managing student database.
- Multi-processing and multi-threading implemented to optimize performance and ensure real-time processing
- Automatic generation of attendance reports in Excel format with student ID, name, and timestamp at which their attendance was marked.
- Executable file provided for easy and efficient usage

## Installation

### Option 1

To install the FaceTrackr application, simply download the executable file from the repository's [release page](https://github.com/ShyamGadde/face-trackr/releases/tag/v2.0.0-alpha) and run the program without any additional installation.

Note: The application requires a webcam to capture images for facial recognition. Make sure that your system has a working webcam before running the application.

### Option 2

1. Clone the repository to your local machine:

```bash
git clone https://github.com/ShyamGadde/face-trackr.git
```

2. Install the required libraries (requires Python 3.7.9+)

```bash
pip install -r requirements.txt
```

3. Run the application

```bash
python app.py
```

## Usage

1. Launch the application by running the executable file.
2. Use the GUI to manage your student database by adding, updating, or deleting student information.
   - Add student information in the form under the 'Add Student' tab in the 'Admin panel'.
   - The student records can also be updated and deleted in the 'Manage Students' tab under the 'Admin panel'.
3. Start attendance tracking by clicking the 'Start New Session' button.
4. The application will automatically detect and record attendance based on facial recognition.
   - Attendees' names and timestamps will be automatically added to the attendance sheet in real time.
   - The attendance sheet will be automatically saved in the "attendance-records" folder with a timestamped filename after every session.
5. To view the generated attendance records (excel files) click the 'Show Attendance Records' button.

## Screenshots/GIFs

### Homepage (Light and Dark Themes)

<div>
   <img src="docs/Homepage(Dark).png" width=49%>
   <img src="docs/Homepage(Light).png" width=49%>
</div>

### Admin Panel

<img src="docs/Admin-Panel.png" width=60%>

<img src="docs/Manage-Students-Tab.png" width=60%>

<img src="docs/Update-Record.png" width=60%>

### Demo

<img src="docs/Demo.gif">

## Contributing

Contributions are always welcome! If you find any bugs or have suggestions for improvement, feel free to submit an issue or pull request on the GitHub repository.

## License

This project is licensed under the [MIT license](https://github.com/ShyamGadde/real-time-attendance-management-system/blob/main/LICENSE).
