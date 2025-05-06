# main.py
import time
import sys
from PyQt6.QtWidgets import QApplication
from ui import ModernHackerPDFConverterWindow # Import the main window class

# --- Application Entry Point ---
# This is the script you run to start the application.

# Create a QApplication instance. Every PyQt application must have one.
# sys.argv allows command line arguments to be passed to the application.
app = QApplication(sys.argv)

# Create an instance of our main window class
main_window = ModernHackerPDFConverterWindow()

# Show the main window on the screen
main_window.show()

# --- REMOVED/COMMENTED OUT the explicit call to _apply_background_image() ---
# This is now handled by the central widget's resizeEvent when show() is called
# main_window._apply_background_image() # <--- COMMENT THIS LINE OUT OR REMOVE

# Start the application's event loop.
# This call blocks and the application stays running until window is closed,
# or QApplication.quit() is called.
sys.exit(app.exec())

# The script finishes execution when sys.exit() is called.