# config.py

import os
from prompts import PROMPT_NAMES, DEFAULT_PROMPT_TEXT

# --- Configuration for LM Studio API ---
LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"
LM_STUDIO_MODEL_NAME = "qwen2.5-7b-instruct-1m" # Verify with your LM Studio setup
AI_REQUEST_TIMEOUT_SECONDS = 180

# --- LLM Context Window (Estimate) ---
# You need to find the actual context window size for the specific Qwen 2.5 7B model you are using.
# Common sizes are 4096, 8192, 32768, or even larger.
# Check the model's page on Hugging Face or documentation.
LLM_CONTEXT_WINDOW = 8192 # <-- UPDATE THIS VALUE based on your model

# --- File Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND_IMAGE_PATH = os.path.join(BASE_DIR, "background.png")

# --- Styling Colors ---
COLOR_BACKGROUND_DARK = "#1a1a1a"
COLOR_TEXT_NEON_GREEN = "#00ff00"
COLOR_HIGHLIGHT_CYAN = "#00ffff"
COLOR_BUTTON_GREEN_DARK = "#008800"
COLOR_BUTTON_GREEN_HOVER = "#00aa00"
COLOR_BUTTON_GREEN_PRESSED = "#006600"
COLOR_DISABLED_BG = "#333333"
COLOR_DISABLED_TEXT = "#999999"
COLOR_DISABLED_BORDER = "#555555"
COLOR_ERROR_RED = "#ff0000"
COLOR_WARNING_YELLOW = "#ffff00"
COLOR_INPUT_BACKGROUND = "#0a0a0a"
COLOR_STATUS_DEFAULT = COLOR_HIGHLIGHT_CYAN
COLOR_LOG_BACKGROUND = "#050505"

# --- Token Count Colors ---
COLOR_TOKEN_NORMAL = COLOR_TEXT_NEON_GREEN # Green when well within limit
COLOR_TOKEN_WARNING = COLOR_WARNING_YELLOW # Yellow when approaching limit
COLOR_TOKEN_EXCEEDED = COLOR_ERROR_RED # Red when exceeding limit
TOKEN_WARNING_THRESHOLD_PERCENT = 80 # Show warning color when exceeding this percentage of context window

# --- Default Prompt ---
DEFAULT_PROMPT = DEFAULT_PROMPT_TEXT

# --- PDF Generation Defaults (ReportLab) ---
PDF_PAGE_SIZE_OPTIONS = ["Letter", "A4"]
PDF_PAGE_SIZE_DEFAULT = "Letter"

PDF_FONT_SIZE_OPTIONS = [10, 11, 12, 14, 16]
PDF_FONT_SIZE_DEFAULT = 12

PDF_FONT_NAME_DEFAULT = "Helvetica"

PDF_PARAGRAPH_SPACE_INCHES = 0.1
PDF_HEADING_SPACE_AFTER_INCHES = 0.15
PDF_BULLET_INDENT_POINTS = 20

# --- UI Dimensions and Spacing ---
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 650
LAYOUT_MARGIN = 20
LAYOUT_SPACING = 15
PROMPT_INPUT_MIN_HEIGHT = 80
ORIGINAL_TEXT_INPUT_MIN_HEIGHT = 200
BUTTON_MIN_HEIGHT = 35
PROCESS_BUTTON_MIN_WIDTH = 250
LOAD_FILE_BUTTON_MIN_WIDTH = 140
SETTINGS_FRAME_HEIGHT = 60
LOG_AREA_MIN_HEIGHT = 100

# --- Separator Style ---
SEPARATOR_COLOR = COLOR_HIGHLIGHT_CYAN
SEPARATOR_HEIGHT_PX = 1
SEPARATOR_MARGIN_V = 8