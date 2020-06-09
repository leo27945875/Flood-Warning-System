from flask import Flask
from flask import render_template
import os
import main

app = Flask(__name__)


@app.route("/")
def ShowMap():
    return render_template("index.html")


if __name__ == "__main__":
    main.Main()
    app.run(host="example.com", port=3005, threaded=True)
