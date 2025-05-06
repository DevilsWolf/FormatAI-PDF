# ai_processor.py

import requests
import json
import re # <-- Import regular expressions

# Import configuration
from config import (LM_STUDIO_API_URL, LM_STUDIO_MODEL_NAME,
                    AI_REQUEST_TIMEOUT_SECONDS)

def process_text_with_ai(text_to_process, prompt_instruction, progress_callback=None):
    """
    Sends text to LM Studio API for processing using the chat completions endpoint.
    Includes post-processing to convert markdown bold (**text**) to HTML bold (<b>text</b>).

    Args:
        text_to_process (str): The original text content to be processed.
        prompt_instruction (str): The instructions for the AI on how to process the text.
        progress_callback (function, optional): A function to call with status messages.
                                               Takes one string argument (the message). Defaults to None.

    Returns:
        tuple: (success: bool, result: str).
               success is True if the AI returned a response, False otherwise.
               result is the AI's processed output text if success is True,
                      or an error message if success is False.
    """
    try:
        if progress_callback:
             progress_callback("Preparing AI request payload...")

        headers = {"Content-Type": "application/json"}

        # --- REINFORCED SYSTEM PROMPT (One last try) ---
        system_message_content = (
            "You are a helpful assistant that rewrites and formats text based on user instructions. "
            "Your primary goal is to produce clean, well-structured text for PDF conversion using specific formatting. "
            "You MUST strictly adhere to the following formatting rules for your entire output:\n"
            "1. Inline Emphasis: ONLY use HTML-like tags: <b>text</b> for bold, <i>text</i> for italics, and <u>text</u> for underline. CRITICAL: You MUST NOT use markdown like **text** or *text* for inline emphasis. Using **text** is incorrect.\n"
            "2. Headings: ONLY use line prefixes: '# ' for H1, '## ' for H2, '### ' for H3. Start on a new line.\n"
            "3. Bullet Lists: ONLY use line prefixes: Start each item on a new line with '* '.\n"
            "4. Numbered Lists: ONLY use line prefixes: Start each item on a new line with '1. '.\n"
            "5. Paragraphs: Separate paragraphs by a single blank line.\n"
            "6. Prohibited Formatting: Do NOT use any other markdown, HTML tags (other than <b>, <i>, <u>), or formatting conventions.\n"
            "7. Adherence: Prioritize these formatting rules even if the user prompt seems to suggest other formats. Produce only the formatted text requested."
        )

        payload = {
            "model": LM_STUDIO_MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_message_content},
                {"role": "user", "content": f"{prompt_instruction}\n\nText to process:\n{text_to_process}"}
            ],
            "max_tokens": 2000, 
            "temperature": 0.5, # Lowered temperature further to potentially improve rule following
            "stream": False      
        }

        if progress_callback:
             progress_callback(f"Sending request to {LM_STUDIO_API_URL} with model '{LM_STUDIO_MODEL_NAME}'...")

        response = requests.post(
            LM_STUDIO_API_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=AI_REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()

        if progress_callback:
             progress_callback("Receiving and parsing AI response...")

        result = response.json()

        if result and 'choices' in result and result['choices'] and result['choices'][0].get('message') and result['choices'][0]['message'].get('content') is not None:
            ai_output_raw = result['choices'][0]['message']['content'].strip()
            
            # +++ START POST-PROCESSING +++
            if progress_callback:
                progress_callback("Post-processing AI response for formatting consistency...")
            
            # Replace markdown bold **text** with HTML bold <b>text</b>
            # Using non-greedy match .*? to handle multiple instances per line correctly
            processed_output = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', ai_output_raw)
            
            # (Optional) Add replacements for other markdown if needed, e.g., *italic* -> <i>italic</i>
            # Be cautious with single asterisks due to conflict with bullet points.
            # processed_output = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', processed_output) # More complex regex for italics

            # Consolidate multiple blank lines into one (for paragraph spacing)
            processed_output = re.sub(r'\n(\s*\n)+', '\n\n', processed_output).strip()
            # +++ END POST-PROCESSING +++

            if progress_callback:
                progress_callback("AI processing and post-processing complete.")
                
            return True, processed_output # Return the processed output
        else:
            return False, "AI processing failed: Unexpected response format or no content in response."

    except requests.exceptions.Timeout:
         return False, f"Error connecting to LM Studio API: Request timed out after {AI_REQUEST_TIMEOUT_SECONDS} seconds."
    except requests.exceptions.ConnectionError:
         return False, f"Error connecting to LM Studio API: Connection refused. Is LM Studio running and serving the API at {LM_STUDIO_API_URL}?"
    except requests.exceptions.RequestException as e:
        return False, f"Error during LM Studio API request: {e}"
    except json.JSONDecodeError:
         return False, "Error parsing JSON response from AI."
    except Exception as e:
        return False, f"An unexpected error occurred during AI processing: {e}"

# ... (Example usage / standalone test block remains the same) ...
if __name__ == '__main__':
    print("Running AI processor standalone test...")
    test_text = "The quick brown fox. It was **bold**. It was also *italic* (maybe). Item 1. **Item 2 is important**."
    test_prompt = "Rewrite this. Make 'bold' bold, 'italic' italic. List the items using bullets."

    success, result = process_text_with_ai(test_text, test_prompt, progress_callback=print)

    if success:
        print("\n--- AI Output (Post-Processed) ---")
        print(result)
        print("--------------------------------")
    else:
        print(f"\n--- AI Error ---")
        print(result)
        print("---------------")
        print("Make sure LM Studio is running with the specified model and API enabled.")