# FormatAI PDF

> AI-powered text formatting and PDF generation tool with a hacker-themed interface.

## Overview

FormatAI PDF is a desktop application built with Python and PyQt6 that allows users to load text from various file formats (.txt, .docx, .pptx), process the text using a Large Language Model (LLM) via a local LM Studio API endpoint for advanced formatting and rewriting based on user instructions, and finally generate a formatted PDF document.

The application features a distinct "hacker" visual theme and includes optimizations for a smoother user experience.

## Features

*   **AI-Powered Formatting:** Utilizes a local LLM (via LM Studio) to rewrite and format text based on predefined or custom prompts.
*   **PDF Generation:** Creates PDF documents from the processed text using ReportLab, supporting:
    *   Headings (H1, H2, H3 via `#`, `##`, `###`)
    *   Bulleted Lists (via `* `)
    *   Inline Formatting (`<b>`, `<i>`, `<u>`)
*   **File Loading:** Supports loading input text from:
    *   Plain Text (`.txt`)
    *   Microsoft Word (`.docx`) - Attempts to preserve basic structure and inline formatting (bold, italic, underline).
    *   Microsoft PowerPoint (`.pptx`) - Extracts text from slides, titles, and notes, attempting basic formatting preservation.
*   **Customizable Prompts:** Provides a dropdown of predefined AI prompt templates and allows users to edit prompts directly.
*   **PDF Settings:** Allows configuration of page size (Letter/A4) and base font size for PDF output.
*   **Token Counting:** Estimates input text token count (using Hugging Face `transformers` tokenizer) and provides visual feedback relative to a configurable context window limit.
*   **Background Processing:** Both AI processing and PDF generation run in background threads to keep the UI responsive.
*   **UI Optimizations:**
    *   Debounced token counting updates for smoother typing.
    *   Lazy loading for the tokenizer model.
    *   Refined cancellation handling for AI tasks.
*   **Themed Interface:** Modern "hacker" aesthetic with custom styling.
*   **Status & Logging:** Provides real-time status updates and a detailed activity log.

## Screenshots

![Screenshot_163](https://github.com/user-attachments/assets/5bc669ed-43db-4fc0-bb01-b62d5106b637)


![Screenshot_164](https://github.com/user-attachments/assets/8b7476a4-5119-4521-9d34-c131901346af)


![Screenshot_165](https://github.com/user-attachments/assets/810dd0e5-984b-4e42-8378-a2c0f9400699)




## Technology Stack

*   **Language:** Python 3
*   **GUI:** PyQt6
*   **AI Backend:** Local LLM served via LM Studio (API compatible with OpenAI format)
*   **API Interaction:** `requests`
*   **PDF Generation:** `reportlab`
*   **DOCX Reading:** `python-docx`
*   **PPTX Reading:** `python-pptx`
*   **Tokenization:** Hugging Face `transformers` (using `gpt2` tokenizer as default estimate)

## Architecture Overview

The application is structured into several Python files:

*   **`main.py`:** Entry point of the application. Initializes the QApplication and the main window.
*   **`ui.py`:** Defines the main application window (`ModernHackerPDFConverterWindow`), UI elements (widgets, layouts), styling, signal/slot connections, and methods for handling user interactions like loading files and starting processes. Contains the text extraction logic for DOCX and PPTX.
*   **`config.py`:** Stores configuration variables such as API endpoints, model names, timeouts, file paths, UI colors, dimensions, and PDF default settings.
*   **`prompts.py`:** Contains predefined AI prompt templates and formatting rules used to instruct the LLM.
*   **`ai_processor.py`:** Handles communication with the LM Studio API. Constructs the request payload (including system and user prompts) and processes the AI's response. Includes post-processing logic to ensure formatting consistency.
*   **`worker.py` (`AIWorker`):** A `QThread` subclass responsible for running the potentially long-running AI processing task (`process_text_with_ai`) in the background to prevent freezing the UI. Communicates results back via signals. Includes cancellation logic.
*   **`pdf_generator.py`:** Takes the processed text and generates a formatted PDF document using the `reportlab` library. Parses basic markdown/HTML tags specified in `ai_processor.py`.
*   **`pdf_worker.py` (`PDFWorker`):** A `QThread` subclass responsible for running the PDF generation task (`generate_pdf`) in the background, ensuring UI responsiveness, especially for larger documents.

**Basic Workflow:**

1.  User interacts with `ui.py` (loads file, edits prompt, sets settings).
2.  User clicks "Process with AI & Generate PDF".
3.  `ui.py` validates input and starts `AIWorker` (`worker.py`).
4.  `AIWorker` calls `process_text_with_ai` (`ai_processor.py`).
5.  `ai_processor.py` sends request to LM Studio API, gets response, performs post-processing.
6.  `AIWorker` receives result and emits `finished` signal (including success/failure and cancellation status).
7.  `ui.py` (`handle_ai_response`) receives the signal. If successful and not cancelled:
8.  `ui.py` prompts user for save location and starts `PDFWorker` (`pdf_worker.py`).
9.  `PDFWorker` calls `generate_pdf` (`pdf_generator.py`).
10. `pdf_generator.py` creates the PDF file using `reportlab`.
11. `PDFWorker` emits `finished` signal.
12. `ui.py` (`handle_pdf_result`) receives signal and updates status/log.

## Setup and Installation

### Prerequisites

*   **Python 3:** Ensure you have Python 3 installed (version 3.8 or later recommended).
*   **pip:** Python's package installer, usually included with Python.
*   **LM Studio:** Download, install, and run LM Studio ([https://lmstudio.ai/](https://lmstudio.ai/)).
    *   Download a compatible LLM within LM Studio (e.g., a Qwen model, Mistral, Llama, etc.).
    *   Start the LM Studio **API Server** using the downloaded model. Note the server address (usually `http://localhost:1234/v1`).

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone <https://github.com/DevilsWolf/FormatAI-PDF.git>
    cd <FormatAI-PDF> 
    ```
2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # Activate the environment:
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate 
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(This installs PyQt6, requests, transformers[torch], python-docx, python-pptx, reportlab).*

### Configuration (LM Studio)

1.  Open the `config.py` file in a text editor.
2.  Verify the following settings match your LM Studio setup:
    *   `LM_STUDIO_API_URL`: Should typically be `"http://localhost:1234/v1/chat/completions"`. Adjust the port if your LM Studio server uses a different one.
    *   `LM_STUDIO_MODEL_NAME`: **Crucially, this needs to match the identifier/path of the model you have loaded and are serving in LM Studio.** You can usually find this in the LM Studio interface when selecting the model for the server. It might look something like `NousResearch/Hermes-2-Pro-Mistral-7B-GGUF/Hermes-2-Pro-Mistral-7B.Q4_K_M.gguf` or similar, depending on the model provider and quantization. The exact format needed depends on how LM Studio exposes it via the API endpoint – check the LM Studio server logs if unsure. *The default value in the code might need changing.*
    *   `LLM_CONTEXT_WINDOW`: Update this value based on the *actual* context window size of the specific LLM you are using in LM Studio. Check the model's documentation.
3.  (Optional) Adjust other settings in `config.py` like timeouts, PDF defaults, or UI colors if desired.

## Running the Application

1.  Ensure your Python virtual environment is activated (if you created one).
2.  Make sure the LM Studio API server is running with your chosen model loaded.
3.  Run the main script from the project's root directory:
    ```bash
    python main.py
    ```

## Usage

1.  **Load Text:**
    *   Paste text directly into the "Original Text" area.
    *   Click "Load File" to load text from `.txt`, `.docx`, or `.pptx` files. The extracted text will appear in the input area.
2.  **Choose Prompt:** Select a predefined formatting task from the "Choose Prompt Template" dropdown.
3.  **Edit Prompt (Optional):** Modify the instructions in the "Editable Prompt Instructions" box for more specific AI guidance. Remember the AI is instructed (via system prompt and formatting rules) to prioritize specific HTML tags (`<b>, <i>, <u>`) and line prefixes (`#`, `*`) for formatting.
4.  **Set PDF Options:** Adjust the "Page Size" and "Font Size" using the controls.
5.  **Process & Generate:** Click the "Process with AI & Generate PDF" button.
6.  **Monitor Progress:** An AI processing dialog will appear. You can cancel the AI step here. The application's status bar and activity log (on the second page/tab) will show progress updates.
7.  **Save PDF:** If AI processing is successful (and not cancelled), a "Save As" dialog will appear. Choose a location and filename for your output PDF. PDF generation will then run in the background.
8.  **View Status:** Check the status bar and activity log for confirmation of PDF creation or any errors during generation.
9.  **Navigate:** Use the "Back to Input" button on the status page to return to the main input screen. Use the "Exit" button on the input page to close the application.

## Configuration (`config.py`)

The `config.py` file allows customization of various application settings:

*   `LM_STUDIO_API_URL`: URL for the LM Studio chat completions endpoint.
*   `LM_STUDIO_MODEL_NAME`: Identifier for the model served by LM Studio. **Must match your server setup.**
*   `AI_REQUEST_TIMEOUT_SECONDS`: How long to wait for a response from the AI API.
*   `LLM_CONTEXT_WINDOW`: Estimated token limit for the input text area warning. **Set according to your model.**
*   `BASE_DIR`, `BACKGROUND_IMAGE_PATH`, `APP_ICON_PATH`: File paths.
*   `COLOR_...`: Hex color codes for UI styling.
*   `TOKEN_...`: Settings for the token counter display colors and threshold.
*   `DEFAULT_PROMPT`: The default instruction loaded for the AI.
*   `PDF_...`: Default settings for PDF page size, font size, font name, and spacing used by `pdf_generator.py`.
*   `WINDOW_...`, `LAYOUT_...`, etc.: Dimensions and spacing for UI elements.

## Development History / Changes Made

This application evolved through several stages:

1.  **Foundation:** Initial setup with basic PyQt6 UI, AI interaction via `requests` to LM Studio, and PDF generation using `reportlab`.
2.  **Direct PDF Mode (Experiment):** Added an option to bypass AI and directly format input using `pdf_generator.py`. (This feature was later removed).
3.  **PDF Generator Enhancements:** Improved `pdf_generator.py` to handle H3 headings and basic numbered/bullet lists based on markdown-like prefixes.
4.  **AI Formatting Refinement:** Addressed issues where the AI output literal markdown (e.g., `**bold**`). This involved:
    *   Refining individual prompts (`prompts.py`) to explicitly request specific HTML tags (`<b>`, `<i>`, `<u>`) and line prefixes (`#`, `*`).
    *   Strengthening the system prompt (`ai_processor.py`) with strict formatting rules.
    *   Adding post-processing (`re.sub`) in `ai_processor.py` to convert any remaining `**text**` to `<b>text</b>` as a fallback.
5.  **File Loading:**
    *   Added support for loading `.docx` files using `python-docx`.
    *   Enhanced `.docx` extraction (`_extract_text_from_docx` in `ui.py`) to handle inline formatting (bold, italic, underline using paragraph runs) and attempt conversion of basic list/heading styles to the app's markdown format.
    *   Added support for loading `.pptx` files using `python-pptx`, including extraction of titles, notes, and shape text with basic formatting preservation.
6.  **Optimizations:**
    *   Moved PDF generation to a background thread (`PDFWorker` in `pdf_worker.py`) to prevent UI freezing.
    *   Implemented debounced token counting using `QTimer` in `ui.py` for smoother typing.
    *   Implemented lazy loading for the Hugging Face tokenizer (`_get_tokenizer` in `ui.py`).
7.  **UX & Stability:**
    *   Added an "Exit" button to the main UI.
    *   Refined the AI cancellation logic (`worker.py` and `ui.py`) to handle cancellation signals more robustly and prevent unwanted PDF generation after cancellation.
    *   Improved error reporting in `pdf_generator.py` and `pdf_worker.py` using `traceback`.
    *   Removed the "Direct PDF" mode to simplify the workflow back to always using AI processing.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs or feature requests. (Add more specific guidelines if desired).

## License

This project is licensed under the MIT License - see the `LICENSE` file for details (or choose another license).

*(You should create a `LICENSE` file in your repository, e.g., containing the text of the MIT license if you choose that one).*
