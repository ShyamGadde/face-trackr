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

![img](docs\Homepage(Dark).png "Homepage (Dark)")



![img](docs\Homepage(Light).png "Homepage (Light))")


![img](docs\Admin-Panel.png "Admin Panel")


![img](docs\Manage-Students-Tab.png "Manage Students Tab")


![img](docs\Update-Record.png "Update Records Tab")


![img](docs\Demo.gif "Demo")

## Acknowledgements

Special thanks to the following resources and libraries that were used in the development of this project:

- [OpenCV](https://opencv.org/) for computer vision functionalities.
- [`face-recognition`](https://github.com/ageitgey/face_recognition) library by Adam Geitgey
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) for generating Excel reports
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for GUI development
- [Python multiprocessing](https://docs.python.org/3/library/multiprocessing.html) and [multithreading](https://docs.python.org/3/library/threading.html) libraries for optimizing performance
- [PyInstaller](https://docs.python.org/3/library/multiprocessing.html) for creating the executable file
- <a target="_blank" href="https://icons8.com/icon/2969/settings">Settings</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
- <a href="https://www.flaticon.com/free-icons/face" title="face icons">Face icons created by juicy_fish - Flaticon</a>

## Contributing

Contributions are always welcome! If you find any bugs or have suggestions for improvement, feel free to submit an issue or pull request on the GitHub repository.

## License

This project is licensed under the [MIT license](https://github.com/ShyamGadde/real-time-attendance-management-system/blob/main/LICENSE).
