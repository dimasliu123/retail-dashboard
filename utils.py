from datetime import datetime

def timeSeriesData(data):
    ts = []

    for i in data :
        d = { 
            "x" : str(datetime.strptime(i.Date, "%Y-%m-%d")), "y" :  i.Sales
        }
        ts.append(d)

    return ts
