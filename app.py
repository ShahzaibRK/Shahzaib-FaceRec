import sys, threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QInputDialog, QMessageBox, QLabel
from PyQt5.QtCore import Qt
from face_recognition_engine import FaceRecognitionEngine

class FaceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.engine = FaceRecognitionEngine()
        self.recognition_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("🎭 Face Recognition System")
        self.setGeometry(400, 200, 400, 300)

        # Dark theme style
        self.setStyleSheet("""
            QWidget { background-color: #1e1e2f; color: #f0f0f0; font-family: Arial; }
            QPushButton {
                background-color: #4CAF50; color: white;
                padding: 10px; border-radius: 8px; font-size: 14px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)

        layout = QVBoxLayout()

        btn_register = QPushButton("➕ Register New Face")
        btn_register.clicked.connect(self.register_face)
        layout.addWidget(btn_register)

        btn_recognize = QPushButton("👁 Start Recognition")
        btn_recognize.clicked.connect(self.start_recognition)
        layout.addWidget(btn_recognize)

        btn_stop = QPushButton("✖ Stop Recognition")
        btn_stop.clicked.connect(self.stop_recognition)
        layout.addWidget(btn_stop)

        btn_delete = QPushButton("🗑 Delete User Face")
        btn_delete.clicked.connect(self.delete_user)
        layout.addWidget(btn_delete)

        # Footer with your name
        footer = QLabel("Developed by Shahzaib Khan")
        footer.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        footer.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(footer)

        self.setLayout(layout)

    def register_face(self):
        user_id, ok = QInputDialog.getInt(self, "Register Face", "Enter User ID:")
        if ok:
            user_name, ok2 = QInputDialog.getText(self, "User Name", "Enter User Name:")
            if ok2:
                num_samples, ok3 = QInputDialog.getInt(self, "Samples", "Enter number of face samples:", 50, 10, 200, 10)
                if ok3:
                    self.engine.register_face(user_id, user_name, num_samples)
                    QMessageBox.information(self, "Success", f"Face registered for {user_name} (ID: {user_id})")

    def start_recognition(self):
        if not self.recognition_thread or not self.recognition_thread.is_alive():
            self.recognition_thread = threading.Thread(target=self.engine.recognize_faces, daemon=True)
            self.recognition_thread.start()

    def stop_recognition(self):
        self.engine.stop_recognition()

    def delete_user(self):
        user_id, ok = QInputDialog.getInt(self, "Delete Face", "Enter User ID to delete:")
        if ok:
            self.engine.delete_user(user_id)
            QMessageBox.information(self, "Deleted", f"User {user_id} deleted successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceApp()
    window.show()
    sys.exit(app.exec_())
