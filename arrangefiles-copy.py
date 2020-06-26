import math
import os
import re
import pandas as pd
from datetime import date, datetime

filePath = './extracted_csv/'
uppar_Limit = 880
lower_Limit = 180
filenamelist = []
phoenationlist = []
patientnamelist = []
timestamplist = []
patientidlist = []
datetimelist = []
f1list = []
f1maxlist = []
H_lalist = []
H_malist = []
H_ralist = []
H_yalist = []
finalcollectionlist = []
finalnamelist = []
finaldatelist = []
finalmlist = []
finalylist = []
finalrlist = []
finalllist = []
finalmylist = []
finalmdylist = []
finalmyrlist = []

# fnamelist = file.split('-')
for f in os.listdir(filePath):
    filenamelist.append(f)

for file in filenamelist:
    splitfilelist = re.split('[- .]', file)

    # for splitfile in splitfilelist:
    phoenationlist.append(splitfilelist[0])
    patientnamelist.append(splitfilelist[1])
    try:
        timestamptodate = datetime.fromtimestamp(
            int(splitfilelist[2])/1000).isoformat()
        datetimelist.append(timestamptodate)
        timestamplist.append(splitfilelist[2])
        patientidlist.append('null')
    except:
        patientidlist.append(splitfilelist[2])
        timestamplist.append(splitfilelist[3])
        timestamptodate = datetime.fromtimestamp(
            int(splitfilelist[3])/1000).isoformat()
        datetimelist.append(timestamptodate)

    cols = ['f1']
    df = pd.read_csv(filePath + file)
    # maxf1 = 0 if (math.isnan(df.f1.max())) else df.f1.max()
    for i in df.f1:
        if math.isnan(i):
            f1maxlist.append(0)
        elif i >= lower_Limit and i <= uppar_Limit:
            f1maxlist.append(i)

        else:
            pass
    f1list.append(max(f1maxlist))

    #  Creating a dataframe of collection
df = pd.DataFrame({'id': patientidlist, 'name': patientnamelist, 'phoenation': phoenationlist,
                   'datetime': datetimelist, 'timestamp': timestamplist, 'f1': f1list})
patientidlist.clear()
patientnamelist.clear()
phoenationlist.clear()
datetimelist.clear()
timestamplist.clear()
f1list.clear()
df['date'] = pd.to_datetime(df['datetime']).dt.normalize()

uniquedatelist = df['date'].dt.strftime('%Y-%m-%d').unique()
uniquenamelist = df['name'].unique()
for uname in uniquenamelist:
    for udate in uniquedatelist:
        filteredlist = df.loc[(df['date'] == udate) & (df['name'] == uname)]
        if(filteredlist.empty != True):
            for ind in filteredlist.index:

                if ((filteredlist['phoenation'][ind]) == 'H_ra' and (filteredlist['f1'][ind]) != 0):
                    H_ralist.append(((filteredlist['name'][ind]), (filteredlist['date'][ind]), (
                        filteredlist['phoenation'][ind]), (filteredlist['f1'][ind])))

                if ((filteredlist['phoenation'][ind]) == 'H_ma' and (filteredlist['f1'][ind]) != 0):
                    H_malist.append(((filteredlist['name'][ind]), (filteredlist['date'][ind]), (
                        filteredlist['phoenation'][ind]), (filteredlist['f1'][ind])))

                if ((filteredlist['phoenation'][ind]) == 'H_la' and (filteredlist['f1'][ind]) != 0):
                    H_lalist.append(((filteredlist['name'][ind]), (filteredlist['date'][ind]), (
                        filteredlist['phoenation'][ind]), (filteredlist['f1'][ind])))

                if((filteredlist['phoenation'][ind]) == 'H_ya' and (filteredlist['f1'][ind]) != 0):
                    H_yalist.append(((filteredlist['name'][ind]), (filteredlist['date'][ind]), (
                        filteredlist['phoenation'][ind]), (filteredlist['f1'][ind])))

            lenlist = [len(H_ralist), len(H_malist),
                       len(H_yalist), len(H_lalist)]

            if(0 in lenlist):
                pass
            else:
                minimum = min(lenlist)
                finalnamelist.append(H_malist[0][0])
                finaldatelist.append(H_malist[0][1])
                for i in range(minimum):
                    m = H_malist[i][3]
                    y = H_yalist[i][3]
                    r = H_ralist[i][3]
                    l = H_lalist[i][3]
                finalmlist.append(m)
                finalylist.append(y)
                finalrlist.append(r)
                finalllist.append(l)
                finalmylist.append(((m + y + r + l) / 400))
                finalmdylist.append((((m/y)+(y/r)+(r/l))/3))
                finalmyrlist.append(
                    ((m + y + r + l) / 400) + ((m/y)+(y/r)+(r/l)) * 20/3)
            finalDataframe = pd.DataFrame({'name': finalnamelist, 'date': finaldatelist, 'm': finalmlist, 'y': finalylist, 'r': finalrlist,
                                           'l': finalllist, '((m + y + r + l ) /400)': finalmylist, '((m/y)+(y/r)+(r/l)/3))': finalmdylist, 'CD': finalmyrlist})
            finalDataframe.to_csv('list.csv')
            H_ralist.clear()
            H_malist.clear()
            H_yalist.clear()
            H_lalist.clear()
            lenlist.clear()
