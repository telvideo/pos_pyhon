import json
import requests
from copy import copy


def normalizer(invoice):

    alist=list(invoice.keys())
    alist.sort()
    totalList=list()
    for li in alist:
        totalList.append(invoice[li])

    OutputStr=""
    while any(isinstance(x, list) for x in totalList) or any( isinstance(y, dict) for y in totalList):
        for j in range(0,len(totalList)):
            li2=totalList[j]
            if isinstance(li2, list):
                li4=copy(li2)
                li4.reverse()
                del totalList[j]
                for i in li4 :
                    totalList.insert(j,i)
                break
            if isinstance(li2, dict):
                alist2=list(li2.keys())
                alist2.sort()
                dictlist=list()
                for li in alist2:
                    dictlist.append(li2[li])
                dictlist.reverse()
                del totalList[j]
                for i in dictlist:
                    totalList.insert(j,i)
                break

    for obj in totalList :

        if obj==None or obj=="":
            OutputStr+="#"
        else:
            OutputStr+=str(obj)
        OutputStr+="#"

    OutputStr=OutputStr.strip("#")
    x =OutputStr


    return x


