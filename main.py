from colorthief import ColorThief

from flask_bootstrap import Bootstrap
from flask import Flask, render_template, redirect, flash, request
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("secret_key")

app = Flask(__name__)
UPLOAD_FOLDER = "static/images/"
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGHT"] = 16 * 1024 * 1024
Bootstrap(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@app.route("/")
def home():
	return render_template("index.html")


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["POST", "GET"])
def upload_file():
	if request.method == "POST":
		if 'file' not in request.files:
			flash('No file')
			return redirect(request.url)

		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash("Image successfully uploaded and displayed below")

			image_path = f"static/images/{filename}"
			ct = ColorThief(image_path)
			palette = ct.get_palette(color_count=11)
			colors = {
			}
			hex_colors = []
			rgb_colors = []
			for color in palette:
				hex = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
				hex_colors.append(hex)
				rgb_colors.append(color)

			for i in range(len(hex_colors)):
				colors[hex_colors[i]] = rgb_colors[i]

			return render_template("colors.html", image=image_path, colors=colors)

		else:
			flash("Allowed image types are png - jpg- jpeg - gif")
			return redirect(request.url)


if __name__ == "__main__":
	app.run(port=5000, debug=True, host="localhost")
