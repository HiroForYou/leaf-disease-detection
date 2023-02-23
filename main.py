from flask import Flask, render_template, request
from inference import ObjectDetection
import os
import base64
from io import BytesIO

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def home():
    return render_template("start.html")


@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    errors = []
    allowed_extensions = set(["png", "jpg", "jpeg", "gif"])
    try:
        if request.method == "POST":
            currentfile = request.files.get("file", "")
    except:
        errors.append("Unable to read file. Please make sure it's valid and try again.")
    # prediction of model
    class_name = ObjectDetection()
    image_result, type = class_name.__call__(currentfile)

    buffered = BytesIO()
    image_result = image_result.resize((400, 400))
    image_result.save(buffered, format="JPEG")
    image_memory = base64.b64encode(buffered.getvalue())

    return render_template(
        "result.html", type=type, img_data=image_memory.decode("utf-8")
    )


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
