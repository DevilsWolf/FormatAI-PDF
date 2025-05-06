# prompts.py

# Common formatting instruction snippet to ensure consistency and reduce redundancy
# This defines the ONLY allowed formatting methods.
FORMATTING_RULES = (
    "Follow these formatting rules strictly for your entire output:\n"
    # --- MODIFIED LINE BELOW ---
    "- Inline Emphasis: ONLY use HTML-like tags: <b>text</b> for bold, <i>text</i> for italics, and <u>text</u> for underline. You MUST NOT use markdown like **text** or *text* for inline emphasis. Using **text** is incorrect and will fail processing.\n" 
    # --- END MODIFIED LINE ---
    "- Headings: Start a new line ONLY with '# ' (H1), '## ' (H2), or '### ' (H3).\n"
    "- Bullet Lists: Start each item on a new line ONLY with '* '.\n"
    "- Numbered Lists: Start each item on a new line ONLY with '1. '.\n"
    "- Paragraphs: Separate paragraphs with a single blank line.\n"
    "- Prohibited Formatting: Use NO other Markdown, HTML tags (other than <b>,<i>,<u>), or formatting conventions."
)


PREDEFINED_PROMPTS = {
    "Default (Clarity & Flow)": (
        "Rewrite the following text to improve clarity, flow, and sentence structure. "
        "Ensure the output is well-organized into paragraphs. Apply emphasis where appropriate using the allowed tags. "
        f"{FORMATTING_RULES}"
    ),
    "Formal Report Summary": (
        "Summarize the provided text into a concise, formal report summary. Focus on key findings, conclusions, and any recommendations present in the text. "
        "Use clear, professional language and well-formed paragraphs. Emphasize critical terms or data points using the allowed tags. "
        f"{FORMATTING_RULES}"
    ),
    "Blog Post Style": (
        "Transform the following text into an engaging blog post. Adopt a friendly and accessible tone. "
        "Break down complex information into short, easy-to-read paragraphs. Use headings and lists to structure the content effectively for readability using the allowed methods. "
        f"{FORMATTING_RULES}"
    ),
    "Technical Documentation Snippet": (
        "Format the given text as a clear and accurate technical documentation snippet. "
        "Use lists for steps, features, or parameters using the allowed methods. Emphasize important function names, file paths, or commands using the allowed tags. "
        f"{FORMATTING_RULES}"
    ),
     "Creative Story Expansion": (
        "Expand on the provided text to create a more descriptive and imaginative story segment. "
        "Incorporate sensory details, character thoughts (if appropriate for the original text's context), and evocative language. Maintain smooth transitions. Apply emphasis using the allowed tags. "
        f"{FORMATTING_RULES}"
     ),
     "Simple List Creation": (
         "From the text provided, extract the main items and format them as a simple list. "
         "If the items imply an order, use a numbered list; otherwise, use a bulleted list, following the allowed methods. "
         f"{FORMATTING_RULES}"
     ),
     "Concise Email Draft": (
         "Based on the following points or notes, draft a concise and polite email. "
         "Include a professional greeting and closing. Structure the email into logical paragraphs. Apply emphasis using the allowed tags. "
         f"{FORMATTING_RULES}"
     ),
     "Marketing Ad Copy": (
         "Rewrite the provided text as persuasive marketing ad copy. Focus on benefits and aim to capture attention immediately. "
         "Use strong action verbs. Keep the copy relatively short and impactful. Emphasize key benefits using the allowed tags. "
         f"{FORMATTING_RULES}"
     ),
     "Product Description": (
         "Generate a detailed product description from the information given. Clearly highlight product features and their benefits to the user. "
         "Organize the information logically, using lists for key features following the allowed methods. Emphasize product names or key features using the allowed tags. "
         f"{FORMATTING_RULES}"
     ),
     "Meeting Minutes Summary": (
         "Summarize the provided meeting notes into concise meeting minutes. "
         "If attendees are mentioned, list them. Detail key discussion points, decisions made, and action items, preferably using lists (following the allowed methods) for clarity. "
         "Maintain a clear and objective tone. Emphasize action item owners or critical dates using the allowed tags. "
         f"{FORMATTING_RULES}"
     ),
     "Troubleshooting Steps": (
         "Convert the following text into clear, step-by-step troubleshooting instructions. "
         "Each step should be a distinct item in a numbered list (following the allowed method). Emphasize actions, commands, or specific text the user should see or enter using the allowed tags. "
         f"{FORMATTING_RULES}"
     ),
     "Historical Event Description": (
         "Based on the text, describe the historical event in detail. If the source text includes dates, key figures, causes, event sequences, and outcomes, incorporate them. "
         "Structure the description in well-formed paragraphs. Emphasize important names and dates using the allowed tags. "
         f"{FORMATTING_RULES}"
     ),
     "Scientific Concept Explanation": (
         "Explain the scientific concept from the provided text in simple, accessible terms. "
         "Break down complex ideas into understandable parts, using analogies if they are present in the source or if you can infer a simple one. "
         "Structure the explanation with paragraphs and appropriate headings (using the allowed methods) for different aspects of the concept. "
         f"{FORMATTING_RULES}"
     ),
     "Restaurant Review": (
         "Compose a restaurant review based on the given notes. "
         "Include comments on food (mentioning specific dishes if noted), service, atmosphere, and the overall experience. Use descriptive language. Emphasize dish names or atmosphere descriptors using the allowed tags. "
         f"{FORMATTING_RULES}"
     ),
     "Code Explanation": (
         "Explain the provided code snippet. Describe its purpose, what key functions or classes do, and the overall logic of how it works. "
         "Structure the explanation using paragraphs. Emphasize key terms or code elements using the allowed tags. "
         f"{FORMATTING_RULES}"
     )
}

PROMPT_NAMES = list(PREDEFINED_PROMPTS.keys())
DEFAULT_PROMPT_TEXT = PREDEFINED_PROMPTS.get(PROMPT_NAMES[0], "") if PROMPT_NAMES else ""