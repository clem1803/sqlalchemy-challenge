from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    print(f"Server received request for Home page...")
    return("Welcome to the home page")

@app.route("")


if __name__ == "__main__":
    app.run(debug=True)