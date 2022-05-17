from flask import Flask, redirect, render_template, url_for, request 
from flask_sqlalchemy import SQLAlchemy
from models import * 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

class Retail(db.Model):
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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/")
def return_home():
    return redirect("index.html")

@app.route("/sales", methods=["GET", "POST"])
def sales():
    return render_template("sales.html")

@app.route("/customer", methods=["GET", "POST"])
def customer():
    return render_template("cust.html")

if __name__ == "__main__":
    app.run(debug=True, port="8080")
