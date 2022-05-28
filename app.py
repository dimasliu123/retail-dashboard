from collections import Counter, OrderedDict
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
#end_date = datetime.now()

engine = db.create_engine("sqlite:///data.db", echo=True)
Base = declarative_base()

"""
SELECT InvoiceDate, InvoiceNo, CustomerID, 
GROUP_CONCAT(Description, ", ") AS "ProductBought", 
SUM(TotalPrice) AS Totals 
FROM RetailSales GROUP BY InvoiceNo 
ORDER BY InvoiceDate;
"""

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

    return TOTAL, MEMBER, NON_MEMBER

def CountrySales():
    query = db.select([
        F.strftime("%Y-%m", Retail.InvoiceDate).label("Date"), Retail.Country.label("Country"), F.sum(Retail.TotalPrice).label("Sales")
    ]).group_by(F.strftime("%Y-%m", Retail.InvoiceDate)).order_by("Date")

    country = query.group_by("Country")
    country_sales = engine.execute(country).fetchall()
    countrySales = {"Dates" : [i.Date for i in country_sales],
                    "Country" : [i.Country for i in country_sales],
                    "Sales" : [i.Sales for i in country_sales]}
    return countrySales

# min -> 2010-12 
# max -> 2011-12

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

def segmentRFMClass(R, F):
    segment = []
    for i in range(len(R)):
        if R[i] == 1 and F[i] == 1:
            segment.append("Hibernating")
        elif (R[i] == 1 and F[i] == 2) or (R[i] == 2 and F[i] == 2) or (R[i] == 2 and F[i] == 1):
            segment.append("At Risk")
        elif R[i] == 1 and F[i] == 4 :
            segment.append("Can't Lose")
        elif R[i] == 2 and F[i] == 2 :
            segment.append("Needs Attention")
        elif (R[i] == 2 and F[i] == 3) or (R[i] == 2 and F[i] == 4):
            segment.append("Potential Loyalist")
        elif (R[i] == 4 and F[i] == 2) or (R[i] == 4 and F[i] == 1):
            segment.append("Promising")
        elif R[i] == 3 and F[i] == 3:
            segment.append("Loyal")
        elif R[i] == 4 and F[i] == 4:
            segment.append("Champion")
        else :
            segment.append("Nothing")
    return segment

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
    R_Quant = [int(i) for i in R_Quant]
    F_Quant = statistics.quantiles(F, n=4)
    F_Quant = [int(i) for i in F_Quant]
    M_Quant = statistics.quantiles(M, n=4)
    M_Quant = [round(i, 2) for i in M_Quant]

    RSeg = segR(R, R_Quant)
    FSeg = segFM(F, F_Quant)
    MSeg = segFM(M, M_Quant)

    RFMScore = list(map(lambda x, y, z : int(x) + int(y) + int(z), RSeg, FSeg, MSeg))
    RFMClass = list(map(lambda x, y, z : str(x) + str(y) + str(z), RSeg, FSeg, MSeg))
    RFMClassSegment = segmentRFMClass(RSeg, FSeg)

    scoreCount = Counter(RFMScore)
    classCount = Counter(RFMClass)

    scoreCount = dict(OrderedDict(sorted(scoreCount.items())))
    classCount = dict(OrderedDict(sorted(classCount.items())))

    score_key, score_val = list(scoreCount.keys()), list(scoreCount.values())
    class_key, class_val = list(classCount.keys()), list(classCount.values())

    return score_key, score_val, class_key, class_val, R_Quant, F_Quant, M_Quant, RFMClassSegment,RSeg, FSeg 

def totalSales():
    quer = db.select([
        F.sum(Retail.TotalPrice).label("Sales")
    ])
    sales = engine.execute(quer).fetchall()
    return list(sales)[0][0]

@app.route("/")
def home():
    sales = totalSales()
    return render_template("index.html", sales=round(sales, 2))

@app.route("/sales/")
def sales():
    total, member, non_member = DailySales()
    return render_template("sales.html", total=total, member=member, non_member=non_member) 

@app.route("/country/")
def country():
    country_sales = CountrySales()
    return render_template("country.html", country_sales=country_sales)

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

if __name__ == "__main__":
    app.run(debug=True, port="8080")
