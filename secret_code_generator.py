# Create the working Python script and a PDF with code + explanations + sample outputs.
# We'll try to use reportlab to build the PDF. If reportlab isn't available, we'll fall back to a plain text file.

import os
from datetime import datetime

code = r'''"""
Secret Code Generator (Caesar Cipher)
------------------------------------
Features:
- Encode and decode messages with a user-specified shift.
- Handles uppercase and lowercase correctly.
- Ignores non-letter characters (spaces, numbers, punctuation).
- Wraps around the alphabet (e.g., Z with shift 2 -> B).
- Robust input handling for invalid choices and shifts.

How to run:
    python secret_code_generator.py
"""

import string

ALPHABET_LOWER = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
ALPHABET_UPPER = string.ascii_uppercase  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET_SIZE = 26

def _shift_char(ch: str, shift: int) -> str:
    """
    Shift a single character by 'shift' places if it's a letter.
    Preserve case. Non-letters are returned unchanged.
    """
    if ch.islower():
        idx = ALPHABET_LOWER.find(ch)
        if idx != -1:
            return ALPHABET_LOWER[(idx + shift) % ALPHABET_SIZE]
        return ch
    elif ch.isupper():
        idx = ALPHABET_UPPER.find(ch)
        if idx != -1:
            return ALPHABET_UPPER[(idx + shift) % ALPHABET_SIZE]
        return ch
    else:
        # Non-letter: leave it as-is
        return ch

def encode_message(message: str, shift: int) -> str:
    """Return the encoded message using a positive shift."""
    return ''.join(_shift_char(ch, shift) for ch in message)

def decode_message(message: str, shift: int) -> str:
    """Return the decoded message by shifting backwards."""
    return ''.join(_shift_char(ch, -shift) for ch in message)

def _read_int(prompt: str) -> int:
    """Read an integer from input with validation."""
    while True:
        raw = input(prompt).strip()
        try:
            # Support values like "26", "-3", "  10  "
            val = int(raw)
            return val
        except ValueError:
            print("Invalid number. Please enter an integer (e.g., 3 or -1).")

def _menu_choice() -> str:
    """Show the menu and return a valid choice (E/D/X)."""
    print("\n=== Secret Code Generator ===")
    print("[E] Encode a message")
    print("[D] Decode a message")
    print("[X] Exit")
    while True:
        choice = input("Choose an option (E/D/X): ").strip().lower()
        if choice in {"e", "d", "x"}:
            return choice
        print("Invalid choice. Please enter E, D, or X.")

def main():
    while True:
        choice = _menu_choice()
        if choice == "x":
            print("Goodbye!")
            break

        message = input("Enter your message: ")
        shift = _read_int("Enter shift (integer, e.g., 3 or -2): ")

        if choice == "e":
            result = encode_message(message, shift)
            print(f"Encoded message: {result}")
        elif choice == "d":
            result = decode_message(message, shift)
            print(f"Decoded message: {result}")

if __name__ == "__main__":
    main()
'''

# Save the Python script
py_path = "/mnt/data/secret_code_generator.py"
with open(py_path, "w", encoding="utf-8") as f:
    f.write(code)

# Prepare sample outputs for embedding
def encode_message(message: str, shift: int) -> str:
    import string
    ALPHABET_LOWER = string.ascii_lowercase
    ALPHABET_UPPER = string.ascii_uppercase
    ALPHABET_SIZE = 26
    def _shift_char(ch: str, shift: int) -> str:
        if ch.islower():
            idx = ALPHABET_LOWER.find(ch)
            if idx != -1:
                return ALPHABET_LOWER[(idx + shift) % ALPHABET_SIZE]
            return ch
        elif ch.isupper():
            idx = ALPHABET_UPPER.find(ch)
            if idx != -1:
                return ALPHABET_UPPER[(idx + shift) % ALPHABET_SIZE]
            return ch
        else:
            return ch
    return ''.join(_shift_char(ch, shift) for ch in message)

def decode_message(message: str, shift: int) -> str:
    return encode_message(message, -shift)

samples = [
    ("Hello, World!", 3),
    ("Zebra-493", 2),
    ("attack AT DAWN!", 5),
]

sample_text = []
for msg, s in samples:
    enc = encode_message(msg, s)
    dec = decode_message(enc, s)
    block = f"Message: {msg}\nShift: {s}\nEncoded: {enc}\nDecoded: {dec}\n"
    sample_text.append(block)

sample_output = "\n".join(sample_text)

# Try to create a PDF using reportlab
pdf_path = "/mnt/data/Secret_Code_Generator_Report.pdf"
created_pdf = False
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
    from reportlab.lib.units import inch
    from reportlab.lib import colors

    doc = SimpleDocTemplate(pdf_path, pagesize=A4, title="Secret Code Generator Report")
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph("Secret Code Generator (Caesar Cipher) – Python", styles["Title"])
    story.append(title)
    story.append(Spacer(1, 0.2*inch))

    meta = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"])
    story.append(meta)
    story.append(Spacer(1, 0.2*inch))

    desc = Paragraph(
        "This document includes the fully working Python code, explanation, and sample outputs for the Secret Code Generator. "
        "The program can encode and decode messages using a Caesar cipher, preserves case, ignores non-letters, and wraps around the alphabet.",
        styles["BodyText"]
    )
    story.append(desc)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("How It Works", styles["Heading2"]))
    logic = (
        "- Each letter is shifted by a user-provided integer (positive or negative).<br/>"
        "- Uppercase and lowercase letters are handled separately to preserve case.<br/>"
        "- Non-letter characters (spaces, punctuation, digits) are left unchanged.<br/>"
        "- Wrap-around uses modulo arithmetic to stay within 26 letters.<br/>"
        "- Robust input validation ensures valid menu choices and integer shifts."
    )
    story.append(Paragraph(logic, styles["BodyText"]))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Python Source Code", styles["Heading2"]))
    story.append(Preformatted(code, styles["Code"]))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Sample Outputs (Screenshots Substitute)", styles["Heading2"]))
    story.append(Preformatted(sample_output, styles["Code"]))

    doc.build(story)
    created_pdf = True
except Exception as e:
    created_pdf = False
    fallback_txt = "/mnt/data/Secret_Code_Generator_Report.txt"
    with open(fallback_txt, "w", encoding="utf-8") as f:
        f.write("Secret Code Generator (Caesar Cipher) – Python\n")
        f.write("="*60 + "\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("Description:\n")
        f.write("Fully working Python code with explanation and sample outputs. "
                "Encodes/decodes using a Caesar cipher, preserves case, ignores non-letters, and wraps around the alphabet.\n\n")
        f.write("How It Works:\n")
        f.write("- Shift letters by an integer (positive/negative).\n")
        f.write("- Preserve uppercase/lowercase; ignore non-letters.\n")
        f.write("- Wrap with modulo 26.\n")
        f.write("- Input validation for menu and integer shift.\n\n")
        f.write("Python Source Code:\n\n")
        f.write(code)
        f.write("\n\nSample Outputs:\n\n")
        f.write(sample_output)

(py_path, pdf_path if created_pdf else fallback_txt, created_pdf)
