import statistics
from typing import List, Tuple
from collections import Counter, OrderedDict
from datetime import datetime

def timeSeriesData(data):
    ts = []

    for i in data :
        d = { 
            "x" : str(datetime.strptime(i.Date, "%Y-%m-%d")), "y" :  i.Sales
        }
        ts.append(d)

    return ts

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


def RFM(end_date, query_data : List[ Tuple[float, str, int, float] ]) :
    C_ID, R, F, M = [], [], [], []

    for row in query_data :
        C_ID.append(row.CustomerID)
        R.append(int((end_date - datetime.strptime(row.Recency, "%Y-%m-%d")).days))
        F.append(row.Frequency)
        M.append(row.Monetary)

    R_Quant = statistics.quantiles(R, n=4)
    F_Quant = statistics.quantiles(F, n=4)
    M_Quant = [round(i, 2) for i in statistics.quantiles(M, n=4)]

    RSeg =  segR(R, R_Quant)
    FSeg = segFM(F, F_Quant)
    MSeg = segFM(M, M_Quant)

    RFMScore = list(map(lambda x, y, z : int(x) + int(y) + int(z), RSeg, FSeg, MSeg))
    RFMClass = list(map(lambda x, y, z : str(x) + str(y) + str(z), RSeg, FSeg, MSeg))
    RFMClassSegment = segmentRFMClass(RSeg, FSeg)

    scoreCount = Counter(RFMScore)
    classCount = Counter(RFMClass)

    scoreCount = OrderedDict(sorted(scoreCount.items()))
    classCount = OrderedDict(sorted(classCount.items()))

    score_key, score_val = list(scoreCount.keys()), list(scoreCount.values())
    class_key, class_val = list(classCount.keys()), list(classCount.values())

    return score_key, score_val, class_key, class_val, R_Quant, F_Quant , M_Quant, RFMClassSegment