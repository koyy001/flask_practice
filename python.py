from ctypes import resize
from email import message_from_string
from flask import Flask, render_template, request, redirect, url_for
import sys
app = Flask(__name__)
import database


@app.route("/")
def goto_a_page():
    return render_template("hello.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/upload_photo")
def upload_photo():
	keyword = request.args.get("keyword")
	add_margin = request.args.get("add_margin")
	merge = request.args.get("merge")
	built = request.args.get("built")
	if add_margin == None:
		add_margin = False
	else:
		add_margin = True
	if merge == None:
		merge = False
	else:
		merge=True
	database.save(keyword, add_margin, merge, built)
	return render_template('upload_photo.html')

@app.route("/upload_done", methods=["POST"])
def upload_done():
	uploaded_files = request.files["file"]
	uploaded_files.save("static/img/{}.jpeg".format(database.now_index()))
	return redirect(url_for("goto_a_page"))

@app.route("/list")
def list():
	house_list = database.load_list()
	length = len(house_list)
	return render_template("list.html", house_list=house_list, length=length)

@app.route("/house_info/<int:index>/")
def house_info(index):
	house_info = database.load_house(index)
	keyword = house_info["keyword"]
	add_margin = house_info["add_margin"]
	merge = house_info["merge"]
	built = house_info["built"]
	photo = f"img/{index}.jpeg"
	return render_template("house_info.html", keyword=keyword, add_margin=add_margin, merge=merge, built=built, photo=photo)

# @app.route("/add")
# def add():
#     return render_template("add.html")


if __name__ == "__main__":
    app.run()