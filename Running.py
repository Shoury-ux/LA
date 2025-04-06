import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QIcon  # Import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView


class WebWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("Console AI")
        self.setGeometry(100, 100, 1000, 600)  # Wider to fit sidebar + browser

        # Set the window icon
        self.setWindowIcon(QIcon(r"C:\Users\wrbre\OneDrive\Desktop\Documents\LA\static\logo.png"))  # ✅ Replace with your actual image path

        # Set up the web engine view
        self.browser = QWebEngineView()
        # Update to load Flask server URL
        self.browser.setUrl(QUrl("http://127.0.0.1:5000/"))

        # Create sidebar logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(r"C:\Users\wrbre\OneDrive\Desktop\Documents\LA\static\logo.png")  # ✅ Replace with your actual image path
        logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Sidebar layout
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(logo_label)
        sidebar_layout.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setFixedWidth(120)  # Adjust width as needed

        # Main layout (horizontal: sidebar + browser)
        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.browser)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = WebWindow()
    window.show()

    sys.exit(app.exec_())