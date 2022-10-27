from utils import timeSeriesData, RFM
from datetime import date, datetime, timedelta
import sqlalchemy as db
from sqlalchemy import func as F
from sqlalchemy import text
from sqlalchemy.sql import column
from sqlalchemy.ext.declarative import declarative_base

end_date = datetime(2011, 12, 10)
#end_date = datetime.now()
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

def getHotProduct():
    query = text("SELECT Description, SUM(Quantity) AS TotQuant, SUM(TotalPrice) AS Sales FROM RetailSales GROUP BY Description ORDER BY TotQuant DESC")
    product, quantity, sales = engine.execute(query).fetchone()
    return product, quantity, sales

def highestCountrySales():
    query = text("SELECT Country, SUM(TotalPrice) as Sales FROM RetailSales GROUP BY Country ORDER BY Sales DESC")
    country, sales = engine.execute(query).fetchone()
    return country, round(sales, 2)

def totalSales():
    query = text(
        """
        SELECT SUM(TotalPrice) AS Sales
        FROM RetailSales
        WHERE Description NOT LIKE '%debt%'
        """
    )
    sales = engine.execute(query).fetchone()
    return sales[0]

def getDebt():
    query = text(
        """
        SELECT SUM(TotalPrice) as Debt
        FROM RetailSales
        WHERE Description LIKE '%debt%'
        """
    )
    debt = engine.execute(query).fetchone()
    return debt[0]

def DailySales():
    query = db.select([
        F.strftime("%Y-%m-%d", Retail.InvoiceDate).label("Date"), 
        Retail.CustomerID, 
        F.sum(Retail.TotalPrice).label("Sales")
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

def queryCountry(data, dates):
    cData = []

    for i in data :
        if i.Date == dates:
            d = {
                "x" : i.Country, "y" : i.Sales
            }
            cData.append(d)

    return cData

# min. date -> 2010-12 
# max. date -> 2011-12
def calcRFM(sq_func = F): 
#    query = text('''
#    SELECT
#        CustomerID,
#        MAX(STRFTIME("%Y-%m", InvoiceDate)) Recency,
#        COUNT(CustomerID) Frequency,
#        SUM(TotalPrice) Monetary
#    FROM RetailSales
#        WHERE CustomerID IS NOT NULL
#        GROUP BY CustomerID
#    ''')

    query = db.select([
        Retail.CustomerID, 
        sq_func.max(sq_func.strftime("%Y-%m-%d", Retail.InvoiceDate)).label("Recency"), 
        sq_func.count(Retail.CustomerID).label("Frequency"), 
        sq_func.sum(Retail.TotalPrice).label("Monetary")
    ]).group_by(Retail.CustomerID).filter(Retail.CustomerID.isnot(None))

    res = engine.execute(query).fetchall() # query for RFM data
    score_key, score_val, class_key, class_val, R_Quant, F_Quant, M_Quant, class_segment = RFM(end_date, res)
    return score_key, score_val, class_key, class_val, R_Quant, F_Quant, M_Quant, class_segment

def getCountrySales():
    query = f'''
        SELECT 
            STRFTIME("%Y-%m", InvoiceDate) DateData,
            Country, 
            SUM(TotalPrice) Sales
        FROM RetailSales
        GROUP BY Country, DateData
        ORDER BY Sales DESC;
    '''
    res = engine.execute(text(query)).fetchall()
    query_date, query_country, query_sales = zip(*res)
    return list(query_date), list(query_country), list(query_sales)

def getTable(num_limit : int = 50):
    query = f'''
        SELECT * FROM RetailSales 
        ORDER BY InvoiceDate ASC LIMIT {num_limit}; 
    '''
    res = engine.execute(text(query)).fetchall()
    return res

def getPagination():
    pass
