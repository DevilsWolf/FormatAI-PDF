# pdf_worker.py

from PyQt6.QtCore import QThread, pyqtSignal
import os
import traceback # Import traceback

# Import the PDF generation function
from pdf_generator import generate_pdf

class PDFWorker(QThread):
    """
    Worker thread for running PDF generation in the background.
    """
    finished = pyqtSignal(bool, str)

    def __init__(self, text_to_convert, filename, page_size_name, font_size):
        super().__init__()
        self.text_to_convert = text_to_convert
        self.filename = filename
        self.page_size_name = page_size_name
        self.font_size = font_size
        self._is_running = True 

    def run(self):
        """
        The main entry point for the thread. Calls the PDF generator.
        """
        print(f"DEBUG (PDFWorker): run() started for '{self.filename}'.") # DEBUG
        if not self._is_running:
            print("DEBUG (PDFWorker): cancelled before starting.") # DEBUG
            self.finished.emit(False, "PDF generation cancelled before starting.")
            return

        try:
            print(f"DEBUG (PDFWorker): Calling generate_pdf...") # DEBUG
            # Perform the PDF generation
            success, message = generate_pdf(
                self.text_to_convert,
                self.filename,
                page_size_name=self.page_size_name,
                font_size=self.font_size
            )
            print(f"DEBUG (PDFWorker): generate_pdf returned: success={success}, message='{message[:100]}...'") # DEBUG
            self.finished.emit(success, message)
            print(f"DEBUG (PDFWorker): finished signal emitted (success={success}).") # DEBUG

        except Exception as e:
            # Catch any unexpected errors DURING the generate_pdf call or thread execution
            error_details = traceback.format_exc()
            error_msg = f"Unexpected error during PDF generation thread: {e}\nDetails:\n{error_details}"
            print(f"ERROR (PDFWorker): {error_msg}") # DEBUG
            # Emit failure signal with detailed error for logging
            self.finished.emit(False, f"Unexpected thread error: {e}") 