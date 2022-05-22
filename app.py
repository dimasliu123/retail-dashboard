import statistics
import numpy as np
from datetime import date, datetime, timedelta
from flask import Flask, redirect, render_template, url_for, request
import json
import sqlalchemy as db
from sqlalchemy import func as F
from sqlalchemy.sql import column
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
end_date = datetime(2011, 12, 10)
engine = db.create_engine("sqlite:///data.db", echo=True)
Base = declarative_base()

class Retail(Base):
    __tablename__ = "RetailSales"
    InvoiceNo = db.Column(db.Integer, primary_key=True)
    StockCode = db.Column(db.Text)
    Description = db.Column(db.Text)
    Quantity = db.Column(db.Integer)
    InvoiceDate = db.Column(db.Date)
    UnitPrice = db.Column(db.Float)
    CustomerID = db.Column(db.Float)
    Country = db.Column(db.Text)
    TotalPrice = db.Column(db.Float)

    @staticmethod
    def get_recent_days(timestamp):
        pass

def timeSeriesData(data):
    ts = []
    for i in data :
        d = { 
            "x" : str(datetime.strptime(i.Date, "%Y-%m-%d")), "y" :  i.Sales
        }
        ts.append(d)
    return ts

def DailySales():
    query = db.select([
        F.strftime("%Y-%m-%d", Retail.InvoiceDate).label("Date"), Retail.CustomerID, F.sum(Retail.TotalPrice).label("Sales")
    ]).group_by(F.strftime("%Y-%m-%d", Retail.InvoiceDate)).order_by(Retail.InvoiceDate)

    query_member = query.filter(Retail.CustomerID.isnot(None))
    query_non_member = query.filter(Retail.CustomerID.is_(None))

    total = engine.execute(query).fetchall()
    member = engine.execute(query_member).fetchall()
    non_member = engine.execute(query_non_member).fetchall() 
    TOTAL = timeSeriesData(total)
    MEMBER = timeSeriesData(member)
    NON_MEMBER = timeSeriesData(non_member)

#    TOTAL = {"Dates" :[str(datetime.strptime(i.Date, "%Y-%m-%d")) for i in total],
#             "Sales" : [i.Sales for i in total]}
#
#    MEMBER = {"Dates" : [str(datetime.strptime(i.Date, "%Y-%m-%d")) for i in member],
#              "Sales" : [i.Sales for i in member]}
#
#    NON_MEMBER = {"Dates" : [str(datetime.strptime(i.Date, "%Y-%m-%d")) for i in non_member],
#                  "Sales" : [i.Sales for i in non_member]}
    return TOTAL, MEMBER, NON_MEMBER

def segR(R, R_Quant):
    RSeg = []
    r_25, r_50, r_75 = R_Quant
    for r in R:
        if r <= r_25:
            RSeg.append(1)
        elif r <= r_50:
            RSeg.append(2)
        elif r <= r_75:
            RSeg.append(3)
        else :
            RSeg.append(4)
    return RSeg

def segFM(FM, FM_Quant):
    FMSeg = []
    fm_25, fm_50, fm_75 = FM_Quant
    for fm in FM:
        if fm <= fm_25:
            FMSeg.append(4)
        elif fm <= fm_50:
            FMSeg.append(3)
        elif fm <= fm_75:
            FMSeg.append(2)
        else : 
            FMSeg.append(1)
    return FMSeg

def calcRFM(sq_func = F): 
    query = db.select([
        Retail.CustomerID, sq_func.max(sq_func.strftime("%Y-%m-%d", Retail.InvoiceDate)).label("Recency"), sq_func.count(Retail.CustomerID).label("Frequency"), sq_func.sum(Retail.TotalPrice).label("Monetary")
    ]).group_by(Retail.CustomerID)

    query = query.filter(Retail.CustomerID.isnot(None))
    res = engine.execute(query).fetchall() # RFM

    C_ID = [int(i.CustomerID) for i in res]
    R = [int((end_date - datetime.strptime(i.Recency, "%Y-%m-%d")).days) for i in res]
    F = [int(i.Frequency) for i in res]
    M = [i.Monetary for i in res]
    R_Quant = statistics.quantiles(R, n=4)
    F_Quant = statistics.quantiles(F, n=4)
    M_Quant = statistics.quantiles(M, n=4)

    RSeg = segR(R, R_Quant)
    FSeg = segFM(F, F_Quant)
    MSeg = segFM(M, M_Quant)

    ValRFM = {"CustomerID" : C_ID, "R" : RSeg, "F" : FSeg, "M" : MSeg}
    return ValRFM

print(calcRFM())

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sales/")
def sales():
    total, member, non_member = DailySales()
    return render_template("sales.html", total=total, member=member, non_member=non_member) 

@app.route("/customer/", methods=["GET", "POST"])
def customer():
    rfm_val = calcRFM()
    return render_template("cust.html", rfm_val = rfm_val)

if __name__ == "__main__":
   app.run(debug=True, port="8080")
