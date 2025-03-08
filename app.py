from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
app = Flask(__name__)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found in environment variables.")

GEMINI_MODEL_NAME = "gemini-2.0-flash"  

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/about")
def about():
    return render_template("about_us.html")



@app.route("/get_response", methods=["POST"])
def get_response():
    user_query = request.form["user_query"]
    gemini_response = get_gemini_response(user_query)
    return jsonify({"response": gemini_response})


def get_gemini_response(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL_NAME}:generateContent?key={GOOGLE_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  

        json_response = response.json()
        
        if "candidates" in json_response and len(json_response["candidates"]) > 0:
            content = json_response["candidates"][0].get("content")
            if content and "parts" in content and len(content["parts"]) > 0:
                text_response = content["parts"][0].get("text", "I'm Lily, and the model had no text in it's parts element")
                return text_response
            else:
                return "I'm Lily, and there was no content in the results."
        else:
            return "I'm Lily, and I encountered issues parsing the response."

    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return f"I'm Lily, and I encountered a request error. Please try again later. Error Details {e}"
    except (KeyError, TypeError) as e:
        print(f"Parsing Exception: {e}")
        return "I'm Lily, and I encountered an issue processing the response."


if __name__ == "__main__":
    app.run(debug=True)