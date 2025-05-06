# worker.py

from PyQt6.QtCore import QThread, pyqtSignal, QMutex 
import time
import sys
from PyQt6.QtWidgets import QApplication 
from ai_processor import process_text_with_ai

class AIWorker(QThread):
    """
    Worker thread for running the AI processing in the background.
    Communicates with the main GUI thread using signals.
    """
    # Signal emitted when processing is completely finished
    # Arguments: success (bool), result_or_message (str), was_cancelled (bool) <--- ADDED was_cancelled
    finished = pyqtSignal(bool, str, bool) 
                                    
    # Signal emitted to report progress or current status
    # Argument: message (str)
    progress = pyqtSignal(str)

    def __init__(self, text_to_process, prompt_instruction):
        """Initializes the AIWorker with text and prompt."""
        super().__init__()
        self.text_to_process = text_to_process
        self.prompt_instruction = prompt_instruction
        self._mutex = QMutex() # Mutex for safe access to _is_running flag
        self._is_running = True # Flag to signal thread to continue, protected by mutex

    def stop(self):
        """Safely signals the worker thread to stop processing."""
        self._mutex.lock()
        self._is_running = False
        self._mutex.unlock()
        # Optional: print for debugging
        # print("DEBUG Worker: stop() called, _is_running set to False") 

    def is_running(self):
        """Check if the thread is supposed to be running (thread-safe)."""
        self._mutex.lock()
        running = self._is_running
        self._mutex.unlock()
        return running

    def run(self):
        """
        The main entry point for the thread.
        This method is executed when QThread.start() is called.
        """
        # Optional: print for debugging
        # print("DEBUG Worker: run() started.")
        
        # Check for immediate cancellation before doing any work
        if not self.is_running():
            self.progress.emit("Worker cancelled before starting.")
            # Emit finished with success=False, appropriate message, and was_cancelled=True
            self.finished.emit(False, "AI processing cancelled before starting.", True) 
            # print("DEBUG Worker: cancelled before API call, finished emitted.")
            return # Exit the run method

        # --- Perform the AI processing ---
        # Pass the self.progress.emit method as the callback
        success, result = process_text_with_ai(
            self.text_to_process,
            self.prompt_instruction,
            progress_callback=self.progress.emit 
        )
        # Optional: print for debugging
        # print(f"DEBUG Worker: process_text_with_ai returned: success={success}")

        # --- Check for cancellation *after* processing call returns ---
        # Use the thread-safe getter method
        was_cancelled = not self.is_running() 
        # Optional: print for debugging
        # print(f"DEBUG Worker: check after API call: was_cancelled={was_cancelled}")

        if was_cancelled:
             # If stop() was called, always report as cancelled, regardless of API success
             final_message = "AI processing was cancelled by user."
             # Emit finished with success=False, cancellation message, and was_cancelled=True
             self.finished.emit(False, final_message, True) 
             # Optional: print for debugging
             # print(f"DEBUG Worker: emitting finished (cancelled): success=False, cancelled=True, msg='{final_message}'")
        else:
             # If not cancelled, emit the result from process_text_with_ai
             # Emit finished with API success/failure, API result/error, and was_cancelled=False
             self.finished.emit(success, result, False) 
             # Optional: print for debugging
             # print(f"DEBUG Worker: emitting finished (normal): success={success}, cancelled=False, msg='{result[:50]}...'")
        
        # Optional: print for debugging
        # print("DEBUG Worker: run() finished.")


# --- Standalone Test Block ---
# (Adjusted lambda to accept the new argument)
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    test_worker = AIWorker("Tell me a joke.", "Generate a single short joke.")
    # Adjust lambda for the finished signal
    test_worker.finished.connect(lambda s, m, c: print(f"Worker Finished: Success={s}, Cancelled={c}, Message={m}"))
    test_worker.progress.connect(lambda msg: print(f"Worker Progress: {msg}"))
    print("Starting worker thread...")
    test_worker.start() 
    test_worker.wait()
    print("Worker thread finished execution.")
    # sys.exit(app.exec()) # Uncomment to keep app open if needed for testing signals