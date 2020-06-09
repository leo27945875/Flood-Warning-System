from flask import Flask
from flask import render_template, send_file
import os
import main
import args

app = Flask(__name__)


@app.route("/")
def ShowMap():
    return render_template("index.html")


# @app.route("/height", method=["GET"])
# def DownLoadFloodData():
#     return send_file(args.heightData)


main.Main()

if __name__ == "__main__":
    app.run(host="example.com", port=3015, threaded=True)
