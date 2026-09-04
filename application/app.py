'''import os
from flask import Flask

app = Flask(__name__)
VERSION = os.getenv("VERSION", "unknown")

@app.route("/")
def home():
	return f"Running version :{VERSION}"
	return "Hello from blue gree deployment project \n This is the home page"

@app.route("/health")
def health():
	return "This page is halthy"

if __name__ == "__main__" :
	app.run("0.0.0.0", port=5000)'''
