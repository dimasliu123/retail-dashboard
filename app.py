from flask import Flask, redirect, render_template, url_for, request
import sqlalchemy as db
from sqlalchemy import func as F
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
engine = db.create_engine("sqlite:///data.db", echo=True)
Base = declarative_base()

class Retail(Base):
    __tablename__ = "RetailSales"
    InvoiceNo = db.Column(db.Integer, primary_key=True)
    StockCode = db.Column(db.Text)
    Description = db.Column(db.Text)
    Quantity = db.Column(db.Integer)
    InvoiceDate = db.Column(db.DateTime)
    UnitPrice = db.Column(db.Float)
    CustomerID = db.Column(db.Float)
    Country = db.Column(db.Text)
    TotalPrice = db.Column(db.Float)

def DailySales():
    query = db.select([
        F.strftime("%Y-%m-%d", Retail.InvoiceDate).label("Date"), F.sum(Retail.UnitPrice).label("Sales")
    ]).group_by(F.strftime("%Y-%m-%d", Retail.InvoiceDate)).order_by(Retail.InvoiceDate)
    res = engine.execute(query).fetchall()
    date, sales = [i[0] for i in res], [i[1] for i in res]
    return date, sales 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/")
def return_home():
    return redirect("index.html")

@app.route("/sales/")
def sales():
    date, sales = DailySales()
    return render_template("sales.html", date=date, sales=sales)

@app.route("/customer/", methods=["GET", "POST"])
def customer():
    return render_template("cust.html")

if __name__ == "__main__":
    app.run(debug=True, port="8080")
