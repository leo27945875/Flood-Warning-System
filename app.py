from flask import Flask
from flask import render_template
import os
import main

app = Flask(__name__)


@app.route("/")
def ShowMap():
    return render_template("index.html")


main.Main()

if __name__ == "__main__":
    app.run(host="example.com", port=3014, threaded=True)
