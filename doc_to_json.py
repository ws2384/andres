import json
from docx import Document

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    dialogues = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return dialogues

def structure_dialogues(dialogue_list):
    """Convert extracted dialogues into a structured JSON format with each line as a separate entry."""
    structured_data = []

    for line in dialogue_list:
        if ":" in line:  # Ensure it's a dialogue line
            speaker, text = line.split(":", 1)
            structured_data.append({"speaker": speaker.strip(), "text": text.strip()})

    # Debug: Print structured data preview
    print("Structured Data Preview:", json.dumps(structured_data[:5], indent=4, ensure_ascii=False))
    
    return structured_data

# Set file paths
input_file_path = "/Users/williamsavage/Desktop/Chino/2024/SP/FINAL/dialogues/Un paciente con dolores de cabeza y mareos.docx"
output_file_path = "/Users/williamsavage/Desktop/Chino/2024/SP/FINAL/dialogues/Un paciente con dolores de cabeza y mareos.json"

# Extract and process dialogues
dialogues = extract_text_from_docx(input_file_path)
json_data = structure_dialogues(dialogues)

# Save JSON to a specific location
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(json_data, json_file, indent=4, ensure_ascii=False)

print(f"JSON file created successfully at: {output_file_path}")

