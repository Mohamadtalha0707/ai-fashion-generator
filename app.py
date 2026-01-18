from flask import Flask, render_template, request
import os
import google.genai as genai
from google.genai.types import GenerateContentConfig

app = Flask(__name__)

# Configure with Client - use environment variable for API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY environment variable not set. Set it before running the app.")
client = genai.Client(api_key=api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            idea = request.form.get("idea", "").strip()
            category = request.form.get("category", "").strip()
            occasion = request.form.get("occasion", "").strip()

            # Validation
            if not idea:
                error = "Please enter a fashion idea"
            elif not category or category == "Select Category":
                error = "Please select a category"
            elif not occasion or occasion == "Select Occasion":
                error = "Please select an occasion"
            else:
                prompt = f"""Create a detailed fashion design concept with the following specifications:

Design Idea: {idea}
Category: {category}
Occasion: {occasion}

Please provide the output in this EXACT format with clear headings:

**OUTFIT DESCRIPTION**
[Provide a detailed description of the complete outfit here]

**FABRIC SUGGESTIONS**
[List 3-5 suitable fabric choices here with brief explanations]

**COLOR PALETTE**
[Provide 4-6 color combinations that would work well]

**STYLING TIPS**
[Give practical styling advice and accessory suggestions]

Keep the description creative, practical, and fashion-forward."""

                # Configuration for the AI
                config = GenerateContentConfig(
                    temperature=0.9,
                    top_p=0.8,
                    max_output_tokens=1024,
                )

                # Generate content
                response = client.models.generate_content(
                    model="models/gemini-flash-lite-latest",  # Model with higher free limit
                    contents=prompt,
                    config=config
                )

                # Access the text
                if response.text:
                    result = response.text
                else:
                    error = "The API returned an empty response."

        except Exception as e:
            # Friendly error handling for quota issues
            if "429" in str(e) or "quota" in str(e).lower():
                error = "AI service limit reached. Please try again in a minute."
            else:
                error = f"An error occurred: {str(e)}"

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=5000)