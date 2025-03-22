import google.generativeai as genai
import markdown
from flask import Flask, render_template, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Configure Google API key
GOOGLE_API_KEY = "AIzaSyAE1SJzY69Ap4aOcTSmTVPqBAnVSXPvfAU"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model (using the gemini-1.5-flash model)
flash = genai.GenerativeModel('gemini-1.5-flash')

# Create a chat instance (initialize with an empty history)
chat = flash.start_chat(history=[])

# System instruction to guide the conversation
system_instruction = (
    "Imitate Donald Trump’s bold, confident, and casual speaking style, keeping responses short, energetic, and direct."
)

# Set up home page
@app.route('/')
def home():
    return render_template('index.html')

# Handle user input and generate response from Gemini
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message')

    try:
        # Send the user message with the system instruction to Gemini
        chat.send_message(system_instruction)  # Set system instruction once
        response = chat.send_message(user_message)  # Send user message
        markdown_content = response.text

        # Convert markdown response to HTML
        html_content = markdown.markdown(markdown_content)
        return jsonify({'response': html_content})

    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)