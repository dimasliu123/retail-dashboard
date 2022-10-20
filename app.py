from validation import HomeDataValidation
from flask import Flask, redirect, render_template, url_for, request
from models import *

DOLLAR_FORMAT = "$ {:0,.2f}"

app = Flask(__name__)

@app.route("/")
def home():
    top_country, top_country_sales = highestCountrySales()
    hot_product, product_quantity, product_sales = getHotProduct()

    home_data = HomeDataValidation(
                    total_sales = round(totalSales(), 2), 
                    top_country = top_country, 
                    top_country_sales = top_country_sales,
                    hot_product = hot_product,
                    product_quantity = product_quantity,
                    product_sales = product_sales
                    )

    return render_template("index.html",
                            total_sales = DOLLAR_FORMAT.format(home_data.total_sales), 
                            top_country = home_data.top_country, 
                            top_country_sales = DOLLAR_FORMAT.format(home_data.top_country_sales),
                            hot_product = home_data.hot_product,
                            product_quantity = home_data.product_quantity,
                            product_sales = DOLLAR_FORMAT.format(home_data.product_sales)
                        )

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
                            FSeg = FSeg
                            )

@app.route("/country/")
def country():
    date, country, sales = getCountrySales()
    for i in country :
        print(country, end="\t")
    total_sales = DOLLAR_FORMAT.format(sum(sales))
    return render_template("country.html", 
                            date = date,
                            country = country, 
                            sales = sales,
                            total_sales = total_sales
                            )

@app.route("/table/")
def table():
    NUM_LIMIT : int = 50
    data = getTable(NUM_LIMIT)
    return render_template("table.html", data = data)

if __name__ == "__main__":
    app.run(debug=True, port="5000")