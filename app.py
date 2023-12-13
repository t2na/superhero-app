from dotenv import load_dotenv
load_dotenv()  # This loads the variables from the .env file

import os
import openai
import re
from flask import Flask, render_template, request

# Load the API key from an environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("No OPENAI_API_KEY found in environment variables")

openai.api_key = openai_api_key

# Create a Flask app
app = Flask(__name__, template_folder='templates')

# Define the home page route
@app.route("/")
def home():
    return render_template("home.html")

# Define the results page route
@app.route("/results", methods=["POST"])
def results():
    # Get the user input for superhero name
    hero_name = request.form["hero_name"]
    synopsis = ''

    try:
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
        
    except openai.RateLimitError as e:
        print("Rate limit exceeded: ", e)
        synopsis = "Error: Rate limit exceeded. Please try again later."
        # You might want to implement additional logic here, such as a retry mechanism or logging

    # Render the results page with the generated synopsis or error message
    return render_template("results.html", hero_name=hero_name, synopsis=synopsis)


if __name__ == "__main__":
    app.run(debug=True)
