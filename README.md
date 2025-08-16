🎭 Robust Real-Time Face Recognition System

This project is a modern facial recognition system built with Python, OpenCV, and PyQt5, designed to provide a seamless, user-friendly experience with advanced customization features. Unlike basic face recognition scripts, this application includes a complete graphical user interface (GUI) that makes it easy to manage users and run recognition in real time.

🚀 Key Features

Face Registration → Add new users by entering a unique ID and name, along with the option to select the number of face samples for improved accuracy.

Real-Time Recognition → Detect and recognize registered faces live from your webcam with smooth performance.

Dynamic User Management → Delete existing users or add new ones anytime, with automatic retraining of the model.

Threaded Recognition → Recognition runs in a separate thread, ensuring the GUI remains responsive and can be closed properly without freezing.

Modern GUI → A clean, dark-themed interface with styled buttons, icons, and smooth layout for a professional look.

Personal Branding → Includes a footer credit: “Developed by Shahzaib Khan” at the bottom right corner.

🛠️ Tech Stack

Python 3

OpenCV → For face detection & recognition (LBPH algorithm).

PyQt5 → For a modern, responsive desktop GUI.

JSON → To store user details (ID ↔ Name mapping).

📌 Why This Project?

This project was built to provide a robust, easy-to-use face recognition tool that goes beyond simple console-based scripts. It’s ideal for learning how to combine computer vision with desktop app development, and it can serve as a base for larger projects such as attendance systems, access control, or security applications.

✅ Future Improvements

Add database integration (SQLite/MySQL) for user management.

Support for multiple recognition models.

More customizable GUI themes.

📌 Project Setup
1. Create project folder
mkdir face_recognition_app
cd face_recognition_app

2. Create virtual environment
python -m venv venv
source venv/bin/activate    # On Linux/Mac
venv\Scripts\activate       # On Windows

3. Install dependencies
pip install opencv-python opencv-contrib-python PyQt5 numpy

📌 Project Structure
face_recognition_app/
│── app.py              # Main GUI
│── face_recognition_engine.py  # Handles training & recognition
│── data/               # Stored face images
│── trainer/            # Stored trained models

Copy and Paste app.py & face_recognition_engine.py and in terminal run python app.py the rest of the files be created automatically.
