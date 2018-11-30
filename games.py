# from pyquery import PyQuery as pq
# import mysql.connector
#
# doc = pq('http://info.win0168.com/jsData/infoHeader.js',encoding='utf-8')
# print(doc)

import request
import dao
import time
def fechCountry():
    url = "http://info.win0168.com/jsData/infoHeader.js"
    html_doc = request.sendRequest(url)
    print(html_doc)
    html_doc = html_doc.replace(' ','')
    data = html_doc.split(";")


    for index in range(len(data)):
        if(index==0):
            continue
        item=data[index];
        itemdata=item.split("=");
        if(len(itemdata)!=2):
            continue
        val=eval(itemdata[1])
        country=val[1];
        image=val[2];
        idx=val[3]
        count=dao.selectOne("select count(id) from games where id=%s",(index,))
        if count[0]==0:
            data1= (index,idx,country,image)
            dao.insert("INSERT INTO games (id,idx,country,image) VALUES (%s,%s,%s,%s)",data1)
        period=val[4];
        for y in range(len(period)):
            valdetail=period[y]
            arr=valdetail.split(",")
            id=arr[0];
            name=arr[1];
            lv=arr[2];
            lv1=arr[3];
            for j in range(len(arr)-4):
                years=arr[j+4]
                count=dao.selectOne("select count(id) from game_pirod where years=%s and bsid=%s",(years,id))
                if count[0]==0:
                    data2=(name,lv,lv1,years,id,index)
                    dao.insert("INSERT INTO game_pirod (name,lv,lv1,years,bsid,game_id) VALUES (%s,%s,%s,%s,%s,%s)",data2)
        print(val[1]+'-'+val[2]+'-'+val[3]+'-')
    return

if __name__=="__main__":
    fechCountry()


