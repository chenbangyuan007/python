import dao
import request
from pyquery import PyQuery as pq

def fetchPankou(bisaiId):
    dao.delete("delete from  pankou where bisaiId=%s",(bisaiId,))
    print(bisaiId)
    url = 'http://vip.win0168.com/AsianOdds_n.aspx?id='+str(bisaiId)
    html=request.sendRequest(url,"vip.win0168.com")
    document=pq(html)
    # print(document)
    print(str(bisaiId)+"开始")
    pankouLine=document("table").eq(1).find("tr");
    bocaiGs=None;
    for i in range(len(pankouLine)):
        if i<=1 or i>(len(pankouLine)-3):
            continue
        hang=pq(pankouLine[i]).find("td");
        if pq(hang[0]).text()!='':
            bocaiGs=pq(hang[0]).text()
        pankouName=None;
        if pq(hang[1]).text()=='':
            pankouName="盘口1"
        else:
            pankouName=pq(hang[1]).text()
        first_zhudui=pq(hang[2]).html()
        first_pankou=pq(hang[3]).html()
        first_cidui=pq(hang[4]).html()
        finally_zhudui=pq(hang[5]).html()
        finally_pankou=pq(hang[6]).html()
        finally_cidui=pq(hang[7]).html()
        count= dao.selectOne("select count(id) from bocaiGs where bocaiGsName=%s",(bocaiGs,))
        if count[0]<=0:
            dao.insert("insert into bocaiGs(bocaiGsName)"
                       " VALUES (%s) ",(bocaiGs,))
        first_pankou_alias=None;
        if first_pankou!=None:
            first_pankou_alias= dao.selectOne("select alias from pankouLabel where pankou=%s limit 1",(first_pankou,))
            first_pankou_alias=first_pankou_alias[0]
        finally_pankou_alias=None
        if finally_pankou!=None:
            finally_pankou_alias= dao.selectOne("select alias from pankouLabel where pankou=%s limit 1",(finally_pankou,))
            finally_pankou_alias=finally_pankou_alias[0]
        data=(bocaiGs,pankouName,first_zhudui,first_pankou,first_cidui,finally_zhudui,finally_pankou,finally_cidui,bisaiId,first_pankou_alias,finally_pankou_alias)
        dao.insert("insert into pankou(bocaiGs,pankouName,first_zhudui,first_pankou,first_cidui,finally_zhudui,finally_pankou,finally_cidui,bisaiId,first_pankou_alias,finally_pankou_alias)"
                   " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",data)
    print(str(bisaiId)+"结束")

if __name__=="__main__":
    fetchPankou(1552274)

