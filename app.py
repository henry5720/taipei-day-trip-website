from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["DEBUG"]=True

# 引入藍圖
from api.attractions.scenery import scenery_bp
app.register_blueprint(scenery_bp)
from api.attractions.search_id import search_bp
app.register_blueprint(search_bp)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

# host > 允許外源訪問
app.run(host='0.0.0.0',port=3000)