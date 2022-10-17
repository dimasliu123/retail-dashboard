from flask import Flask, redirect, render_template, url_for, request
from models import *

app = Flask(__name__)

@app.route("/")
def home():
    sales = round(totalSales(), 2)
    return render_template("index.html", sales = "$ {:0,.2f}".format(sales))

@app.route("/sales/")
def sales():
    total, member, non_member = DailySales()
    return render_template("sales.html", total=total, member=member, non_member=non_member) 

@app.route("/customer/")
def customer():
    score_key, score_val, class_key, class_val, R_Quant, F_Quant, M_Quant, class_segment, RSeg, FSeg = calcRFM()
    return render_template("cust.html",  
                            score_key = score_key, 
                            score_val = score_val,
                            class_key = class_key,
                            class_val = class_val,
                            R_Quant = R_Quant,
                            F_Quant = F_Quant,
                            M_Quant = M_Quant,
                            class_segment = class_segment,
                            RSeg = RSeg,
                            FSeg = FSeg)

@app.route("/country/", methods=["GET", "POST"])
def country():
    country_sales = CountrySales("2010-12")
    if request.method == "POST":
        country_sales = request.form["submit-btn"]
        print(country_sales)
    elif request.method == "GET":
        return render_template("country.html", country_sales = country_sales)

@app.route("/product/")
def product():
    return render_template("product.html")

if __name__ == "__main__":
    app.run(debug=True, port="8080")
