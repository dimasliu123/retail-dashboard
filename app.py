from validation import HomeDataValidation
from flask import Flask, redirect, render_template, url_for, request
from models import *
import json

DOLLAR_FORMAT = "$ {:0,.2f}"

app = Flask(__name__)

@app.route("/")
def home():
    top_country, top_country_sales = highestCountrySales()
    hot_product, product_quantity, product_sales = getHotProduct()
    total_debt = getDebt()
    total_sales = round(totalSales(), 2)

    return render_template("index.html",
                            total_debt = DOLLAR_FORMAT.format(total_debt),
                            total_sales = DOLLAR_FORMAT.format(total_sales), 
                            top_country = top_country, 
                            top_country_sales = DOLLAR_FORMAT.format(top_country_sales),
                            hot_product = hot_product,
                            product_quantity = product_quantity,
                            product_sales = DOLLAR_FORMAT.format(product_sales)
                        )

@app.route("/sales/")
def sales():
    total, member, non_member = DailySales()
    return render_template("sales.html", total=total, member=member, non_member=non_member) 

@app.route("/customer/")
def customer():
    score_key, score_val, class_key, class_val, R_Quant, F_Quant, M_Quant, class_segment = calcRFM()
    return render_template("cust.html",  
                            score_key = score_key, 
                            score_val = score_val,
                            class_key = class_key,
                            class_val = class_val,
                            R_Quant = R_Quant,
                            F_Quant = F_Quant,
                            M_Quant = M_Quant,
                            class_segment = class_segment,
                            )

@app.route("/country/")
def country():
    query_date, query_country, query_sales = getCountrySales()
    return render_template("country.html", 
                            query_date = query_date,
                            query_country = query_country, 
                            query_sales = query_sales
                            )

@app.route("/table/")
def table():
    NUM_LIMIT : int = 50
    data = getTable(NUM_LIMIT)
    return render_template("table.html", data = data)

if __name__ == "__main__":
    app.run(debug=True, port="5000")
