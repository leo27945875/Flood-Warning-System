from flask import Flask
from flask import render_template, send_file
import os
import main
import args

app = Flask(__name__)


@app.route("/")
def ShowMap():
    return render_template("index.html")


@app.route("/height", methods=["GET"])
def DownLoadFloodData():
    return send_file(args.heightData,
                     mimetype="text/csv",
                     as_attachment=True,
                     attachment_filename="flood_height.csv")


# Start main program:
main.Main()


if __name__ == "__main__":
    app.run(port=3024, threaded=True)
