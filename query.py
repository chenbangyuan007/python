#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pyquery import PyQuery as pq
import  re

# doc = pq('http://info.win0168.com/info/index_cn.htm',encoding='utf-8')
# print(doc)
# doc1 = pq(url='https://www.baidu.com')
# mydb = mysql.connector.connect(
#     host="localhost",       # 数据库主机地址
#     user="root",    # 数据库用户名
#     passwd="123456",   # 数据库密码
#     database="test"
# )
# mycursor = mydb.cursor()
# items=doc('#J_goodsList').children("ul").children("li .p-price i")
# for item in items:
#     data= (doc(item).text(),"2")
#     mycursor.execute("INSERT INTO test (price,id) VALUES (%s,%s)",data)
#     print(doc(item).text())
#
# mydb.commit()    # 数据表内容有更新，必须使用到该语句
# print(mycursor.rowcount, "记录插入成功。")
# findall = re.findall(r"jh\[\"(R_|G)\d{1,}\"\] =(.+?);",
#                      "jh[\"G17129\"] = [[1637449, 177, -1, '2018-10-31 03:45', 3282, 1846, '0-1', '0-0', '', '', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', '', ''], [1637450, 177, -1, '2018-10-31 03:45', 1843, 30079, '0-1', '0-1', '英北超11', '', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', 'ENG-N PR-11', ''], [1637451, 177, -1, '2018-10-31 03:45', 11787, 18245, '3-0', '3-0', '英南超中10', '英南超中6', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', 'ENG-S CE-10', 'ENG-S CE-6'], [1637452, 177, -1, '2018-10-31 03:45', 1861, 3901, '2-1', '2-1', '英依超6', '英依超22', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', 'ENG RYM-6', 'ENG RYM-22'], [1637453, 177, -1, '2018-10-31 03:45', 3757, 22277, '2-2', '1-1', '英南超22', '英依超18', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', 'ENG-S PR-22', 'ENG RYM-18'], [1637454, 177, -1, '2018-10-31 03:45', 3787, 15649, '3-1', '2-1', '英南超5', '', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', 'ENG-S PR-5', ''], [1637455, 177, -1, '2018-10-31 03:45', 3286, 1860, '2-0', '0-0', '英南超18', '英南甲14', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', 'ENG-S PR-18', 'ENG SD1-14'], [1637456, 177, -1, '2018-10-31 03:45', 41264, 3795, '4-1', '2-0', '', '英南甲16', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', '', 'ENG SD1-16'], [1637457, 177, -1, '2018-10-31 03:45', 1452, 18219, '5-1', '4-1', '英南超6', '英南超9', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', 'ENG-S PR-6', 'ENG-S PR-9'], [1637458, 177, -1, '2018-10-31 03:45', 3754, 11120, '2-2', '1-1', '', '英南甲32', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', '', 'ENG SD1-32'], [1637459, 177, -1, '2018-10-31 03:45', 3758, 3751, '3-0', '0-0', '英南超中12', '英南超17', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', 'ENG-S CE-12', 'ENG-S PR-17'], [1637307, 177, -1, '2018-10-31 03:45', 3755, 3900, '3-2', '1-1', '英南甲2', '英依超14', , , '', '', 1, 1, 1, 1, 0, 0, '', '', '', '0', 'ENG SD1-2', 'ENG RYM-14'], [1637308, 177, -1, '2018-10-31 03:45', 3423, 18241, '2-3', '2-1', '英北甲18', '英北甲13', , , '', '', 1, 1, 1, 1, 0, 0, '', '', '', '0', 'ENG UD1-18', 'ENG UD1-13'], [1637309, 177, -1, '2018-10-31 03:45', 3425, 3783, '2-2', '1-2', '英依超4', '', , , '', '', 1, 1, 1, 1, 0, 0, '', '', ';|;|;|90,2-2;;1,2-2;3-2;1', '0', 'ENG RYM-4', ''], [1637310, 177, -1, '2018-10-31 03:45', 1385, 7786, '3-0', '2-0', '英南超中13', '英北超8', , , '', '', 1, 1, 1, 1, 0, 0, '', '', '', '0', 'ENG-S CE-13', 'ENG-N PR-8'], [1637311, 177, -1, '2018-10-31 03:45', 1454, 15641, '2-2', '2-0', '英南超中7', '英南超中11', , , '', '', 1, 1, 1, 1, 0, 0, '', '', ';|;|;|90,2-2;;1,2-3;;2', '0', 'ENG-S CE-7', 'ENG-S CE-11'], [1637460, 177, -1, '2018-11-01 03:45', 3760, 6033, '1-1', '0-1', '英南超中16', '英北超7', , , '', '', 1, 1, 1, 1, 0, 0, '', '', ';|;|;|90,1-1;;1,1-2;;2', '0', 'ENG-S CE-16', 'ENG-N PR-7'], [1637448, 177, -14, '2018-11-07 03:45', 3424, 3890, '推迟|推遲|Delay', '', '英依超9', '英南超13', , , '', '', 1, 1, 0, 0, 0, 0, '', '', '', '0', 'ENG RYM-9', 'ENG-S PR-13']];")
d="[[26, 379, 5, 3, [1486224, 84, -1, '2018-01-10 03:45', 26, 379, '2-1', '0-1', '英超1', '英冠4', 2.5, 1, '3.5', '1.5', 1, 1, 1, 1, 0, 0, '<a href=http://www.310tv.com/video/48024.html target=_blank><font color=\"blue\">赛事集锦</font></a>', '', '', '0', 'ENG PR-1', 'ENG LCH-4'], [1490454, 84, -1, '2018-01-24 03:45', 379, 26, '2-3', '0-1', '英冠5', '英超1', -1.75, -0.75, '3/3.5', '1/1.5', 1, 1, 1, 1, 0, 0, '<a href=http://www.310tv.com/video/48132.html target=_blank><font color=\"blue\">赛事集锦</font></a>', '', '', '0', 'ENG LCH-5', 'ENG PR-1']], [24, 19, 1, 2, [1486223, 84, -1, '2018-01-11 04:00', 24, 19, '0-0', '0-0', '英超3', '英超6', 0.5, 0.25, '2.5/3', '1/1.5', 1, 1, 1, 1, 0, 0, '<a href=http://www.310tv.com/video/48029.html target=_blank><font color=\"blue\">赛事集锦</font></a>', '', '', '0', 'ENG PR-3', 'ENG PR-6'], [1490455, 84, -1, '2018-01-25 04:00', 19, 24, '2-1', '1-1', '英超6', '英超3', 0, 0, '2.5/3', '1/1.5', 1, 1, 1, 1, 0, 0, '', '', ';|2;|;|;;;;', '0', 'ENG PR-6', 'ENG PR-3']]];"

try:
    eval(d)
except:
    dataStr=''
    if d.endswith("]]];"):
        d=re.findall(r"\[{1,2}(.+?)\]\]",d)
        for j in range(len(d)):
            print(d[j]+']')
            dataStr=dataStr+d[j]+']'
    per=re.findall(r"\[{1,2}(.+?)\]{1,2}",dataStr)
    print(per)
    for i in range(len(per)):
        try:
            data=eval(per[i])
            gameData=(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]
                      ,data[9],data[10],data[11],data[12],data[13],1)
        except:
            print(per[i])
            data=per[i].replace("\'","").split(",")
            gameData=(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]
                      ,data[9],data[10],data[11],data[12],data[13],1)
        print(gameData)

