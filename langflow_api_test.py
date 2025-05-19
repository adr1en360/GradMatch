import requests

url = "http://127.0.0.1:7860/api/v1/run/49f4fc8b-9d52-4ade-9261-7cdb390228ec"

# Replace these variables with user-provided values
gre_input = "320"
program_input = "Computer Science"
gpa_input = "3.9"
research_input = "AI"

payload = {
    "output_type": "chat",
    "input_type": "text",
    # The 'tweaks' object with correct node IDs from the AI flow
    "tweaks": {
        "TextInput-uLle1": {"input_value": gre_input},      # GRE Score
        "TextInput-HApJP": {"input_value": program_input},  # Program
        "TextInput-nCOg3": {"input_value": gpa_input},      # GPA
        "TextInput-p00DX": {"input_value": research_input}  # Research Experience
    }
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    print("API Response:", response.text)
except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")