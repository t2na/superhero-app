import os
import openai
import re
from flask import Flask, render_template, request

# Import the os module
import os

# Load the API key from an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create a Flask app
app = Flask(__name__, template_folder='superheroapp/templates')

# Define the home page route
@app.route("/")
def home():
    return render_template("home.html")

# Define the results page route
@app.route("/results", methods=["POST"])
def results():
    # Get the user input for superhero name
    hero_name = request.form["hero_name"]

    # Generate prompt for OpenAI API
    prompt = f"Generate a brief synopsis about the origin story of a superhero named {hero_name}."
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the generated synopsis from the OpenAI API response
    synopsis = response.choices[0].text
    synopsis = re.sub('[^0-9a-zA-Z\n\.\?!,]+', ' ', synopsis)
    synopsis = synopsis.strip()

    # Render the results page with the generated synopsis
    return render_template("results.html", hero_name=hero_name, synopsis=synopsis)

if __name__ == "__main__":
    app.run(debug=True)

