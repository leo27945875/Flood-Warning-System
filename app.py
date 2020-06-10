from flask import Flask
from flask import render_template, send_file
import os
import main
import args

app = Flask(__name__)
app.config["DEBUG"] = False


@app.route("/")
def ShowMap():
    return render_template("index.html")


@app.route("/height", methods=["GET"])
def DownLoadFloodData():
    return send_file(args.heightData,
                     mimetype="text/csv",
                     as_attachment=True,
                     attachment_filename="flood_height.csv")


if os.environ.get("WERKZEUG_RUN_MAIN") == "true" and not app.debug:
    main.Main()


if __name__ == "__main__":
    app.run(host="example.com", port=5000, threaded=True)
